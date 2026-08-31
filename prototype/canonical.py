# -*- coding: utf-8 -*-
"""Canonical Evidence Object pipeline (Pre-P2 Architecture Refinement).

Implements the three deterministic layers approved in HD-PRE-P2-INPUT and
specified in design/CANONICAL_CONTRACTS.md:

    Layer 1  load_canonical()   — single source of truth (cases/<CASE>/canonical.json)
    Layer 2  derive()           — Deterministic Derived Context (A/R facts, Stable D-ids)
    Layer 3  render_blocks()    — LLM-friendly 9-Block Korean Markdown rendering
             render_supply()    — Candidate Pool cards / Hot Tip originals / Screens
                                   (supply is consumed by the prompt builder, not the
                                    9-block customer context)

Boundaries enforced here (never semantic judgment):
  - Derived text states What happened / What changed only. The forbidden
    vocabulary below must never appear in engine output (unit-tested).
  - Balance-vs-flow linkage goes no further than arithmetic reconciliation
    ("금액 일치") per HD-PRE-P2-INPUT Decision 1-1.
  - Upcoming items carry objective time facts only (Decision 1-2).

Standard library only. Python 3.9+.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent

BLOCK_TITLES = {
    1: "Customer & Retirement Lifecycle",
    2: "Current IRP Snapshot",
    3: "Recent Changes & Money Flow",
    4: "Event Timeline",
    5: "Investment Behavior",
    6: "Digital Behavior & Sequence",
    7: "Wider Financial Context",
    8: "Upcoming Decision Horizon",
    9: "Supplementary Human-authored Context",
}
EVIDENCE_TYPES = {"fact", "arithmetic_derived", "rule_derived", "signal"}
AUTHOR_EVIDENCE_TYPES = {"fact", "signal"}  # derived types are engine-only
SOURCE_TYPES = {"account_system", "transaction", "digital_behavior", "crm",
                "external_account", "rule_engine"}

# Engine output must never assign meaning (HD-PRE-P2-INPUT 1-1; unit-tested).
ENGINE_FORBIDDEN_VOCAB = ("방치", "미운용", "대기성", "남아 있는")

TYPE_LABEL = {"fact": "F", "arithmetic_derived": "A", "rule_derived": "R", "signal": "S"}

BLOCK6_NOTE = ("(경계) 조회·검색·메뉴 진입·클릭 등의 행동은 관심 가능성 또는 행동 Evidence일 뿐, "
               "고객 의사 자체를 의미하지 않는다. 행동 Sequence가 강하더라도 고객 의사로 승격하지 않는다.")
BLOCK9_NOTE = ("(경계) 아래는 사람이 작성한 보조 맥락(Supplementary Human-authored Context)이다. "
               "고객 발화 원문이라고 보장하지 않으며, 현재 고객 의사를 확정하는 근거가 아니다. "
               "작성 경과일과 위 시스템 Evidence(①~⑧)를 함께 읽고 필요하면 현재 의사를 재확인한다.")
RENDER_INTRO = (
    "아래는 Customer Evidence Pack(9-Block)이다. ①~⑧은 시스템 관찰 Evidence, ⑨는 사람이 작성한 보조 맥락이다.\n"
    "각 항목 앞의 [E-/D-번호]는 Evidence ID이며, 판단 근거로 사용한 항목의 ID를 출력의 supporting_evidence_ids에 기재한다.\n"
    "항목 라벨: [F]=시스템 확인 사실, [A]=산술 파생값(시스템 계산), [R]=Rule 판정값(rule_source·rule_as_of 병기), [S]=행동 신호.\n"
    "값 표기: NULL(값 없음)·0(수량 0)·해당없음(대상 아님)은 서로 다른 의미다. 여기에 없는 정보는 제공되지 않은 것이며 임의로 채우지 않는다."
)


@dataclass
class CanonicalItem:
    id: str
    block: int
    evidence_type: str
    source_type: str
    text: str
    as_of: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalCase:
    case_id: str
    base_date: _dt.date
    evidence: List[CanonicalItem]
    supply: Dict[str, Any]
    source_file: str
    source_sha256: str

    def items_of_kind(self, kind: str) -> List[CanonicalItem]:
        return [it for it in self.evidence if it.data.get("kind") == kind]

    def first_of_kind(self, kind: str) -> Optional[CanonicalItem]:
        items = self.items_of_kind(kind)
        return items[0] if items else None


def _to_date(v: Any) -> _dt.date:
    return _dt.date.fromisoformat(str(v))


def load_canonical(case_id: str, root: Optional[Path] = None) -> CanonicalCase:
    """Layer 1: load and validate cases/<CASE>/canonical.json (single source)."""
    path = (root or REPO_ROOT) / "cases" / case_id / "canonical.json"
    if not path.is_file():
        raise FileNotFoundError(f"canonical.json not found: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    errs: List[str] = []
    base_date = _to_date(raw["base_date"])
    items: List[CanonicalItem] = []
    seen = set()
    for i, obj in enumerate(raw.get("evidence") or []):
        eid = str(obj.get("id", ""))
        if not (len(eid) == 4 and eid[0] == "E" and eid[1:].isdigit()):
            errs.append(f"evidence[{i}]: bad id {eid!r} (E+3자리)")
        if eid in seen:
            errs.append(f"duplicate evidence id {eid}")
        seen.add(eid)
        blk = obj.get("block")
        if blk not in BLOCK_TITLES:
            errs.append(f"{eid}: bad block {blk!r}")
        et = obj.get("evidence_type")
        if et not in EVIDENCE_TYPES:
            errs.append(f"{eid}: bad evidence_type {et!r}")
        elif et not in AUTHOR_EVIDENCE_TYPES:
            errs.append(f"{eid}: evidence_type {et!r} is engine-generated; authors write fact/signal only")
        st = obj.get("source_type")
        if st not in SOURCE_TYPES:
            errs.append(f"{eid}: bad source_type {st!r}")
        if st == "crm" and blk != 9:
            errs.append(f"{eid}: source_type=crm must live in block 9")
        if not str(obj.get("text", "")).strip():
            errs.append(f"{eid}: empty text")
        items.append(CanonicalItem(eid, blk, et, st, str(obj.get("text", "")).strip(),
                                   obj.get("as_of"), obj.get("data") or {}))
    supply = raw.get("supply") or {}
    for key, id_field in (("product_candidates", "product_id"), ("hot_tips", "tip_id"), ("screens", "screen_id")):
        ids = [x.get(id_field) for x in supply.get(key) or []]
        if len(ids) != len(set(ids)):
            errs.append(f"supply.{key}: duplicate {id_field}")
    if errs:
        raise ValueError("canonical.json validation failed: " + "; ".join(errs))
    return CanonicalCase(str(raw.get("case_id", case_id)), base_date, items, supply,
                         str(path), hashlib.sha256(path.read_bytes()).hexdigest())


# ---------------------------------------------------------------------------
# Layer 2 — Deterministic Derived Context
# ---------------------------------------------------------------------------
def derive(case: CanonicalCase) -> List[CanonicalItem]:
    """Produce A/R derived items with Stable D-ids.

    Generation order is a deterministic function of canonical evidence order,
    so identical input always yields identical ids (Contract §1.4).
    """
    out: List[CanonicalItem] = []
    counter = 0

    def add(block: int, evidence_type: str, text: str, as_of: Optional[str] = None) -> None:
        nonlocal counter
        counter += 1
        for w in ENGINE_FORBIDDEN_VOCAB:
            if w in text:
                raise AssertionError(f"engine produced forbidden vocab {w!r}: {text}")
        out.append(CanonicalItem(f"D{counter:03d}", block, evidence_type, "rule_engine", text, as_of))

    base = case.base_date

    # 1) deposit elapsed days (A → block 3), canonical order
    for it in case.items_of_kind("deposit"):
        d = it.data
        days = (base - _to_date(d["date"])).days
        amt = f"{int(d['amount']):,}원 " if d.get("amount") is not None else ""
        reason = f"(사유: {d['reason']}) " if d.get("reason") else ""
        add(3, "arithmetic_derived",
            f"입금 경과일: {d['date']} {amt}{reason}→ 기준일까지 {days}일 경과")

    # 2) window balance changes (A → block 3): only for windows actually present
    cur = case.first_of_kind("current_balance")
    for snap in case.items_of_kind("balance_snapshot"):
        if not cur:
            break
        s = snap.data
        days = (base - _to_date(s["date"])).days
        if s.get("cash") is not None and cur.data.get("cash") is not None:
            delta = int(cur.data["cash"]) - int(s["cash"])
            if delta != 0:  # 변화 없음은 스냅샷 자체가 이미 보여준다 — 0원 증감 항목은 만들지 않는다
                add(3, "arithmetic_derived",
                    f"최근 {days}일 현금성자산 증감: {delta:+,}원 ({int(s['cash']):,}원 → {int(cur.data['cash']):,}원)")
        if s.get("total") is not None and cur.data.get("total") is not None:
            delta_t = int(cur.data["total"]) - int(s["total"])
            if delta_t != 0:
                add(3, "arithmetic_derived",
                    f"최근 {days}일 전체 평가금액 증감: {delta_t:+,}원 ({int(s['total']):,}원 → {int(cur.data['total']):,}원)")

    # 3) balance-vs-flow arithmetic reconciliation (A → block 3): exact match only
    if cur and cur.data.get("cash") is not None:
        cash = int(cur.data["cash"])
        for it in case.items_of_kind("deposit"):
            if it.data.get("amount") is not None and int(it.data["amount"]) == cash:
                add(3, "arithmetic_derived",
                    f"현재 현금성자산 {cash:,}원은 {it.data['date']} "
                    f"'{it.data.get('reason', '입금')}' 입금액과 금액이 일치한다 (산술 대조)")

    # 4) maturity D-n (A → block 8), canonical order
    for it in case.items_of_kind("maturity"):
        d = it.data
        dn = (_to_date(d["date"]) - base).days
        amt = f"{int(d['amount']):,}원 " if d.get("amount") is not None else ""
        prod = f"{d['product']} " if d.get("product") else ""
        when = f"D-{dn}" if dn >= 0 else f"만기 경과 {-dn}일"
        add(8, "arithmetic_derived", f"만기 시한: {prod}{amt}만기 {d['date']} → {when}")

    # 5) DO rule clock (R → block 8)
    do = case.first_of_kind("do_registration")
    if do and do.data.get("registered") and do.data.get("trigger_date"):
        weeks = 2 if do.data.get("trigger_type") == "최초입금" else 6
        expected = _to_date(do.data["trigger_date"]) + _dt.timedelta(weeks=weeks)
        delta = (base - expected).days
        if delta > 0:
            status = f", 기준일 대비 {delta}일 경과 — 실제 적용 여부는 별도 확인 필요(적용 여부 원천값 미보유)"
        elif delta < 0:
            status = f", 도래까지 {-delta}일"
        else:
            status = ", 기준일 당일 도래"
        add(8, "rule_derived",
            f"디폴트옵션 적용 예상 기준일: {expected.isoformat()} "
            f"({do.data.get('trigger_type', '만기')} {do.data['trigger_date']} + {weeks}주){status} "
            f"| rule_source=최초입금 2주 / 만기 4+2주 — 행내 기준 | rule_as_of={base.isoformat()} | rule_id=DO-CLOCK-01",
            as_of=base.isoformat())

    # 6) pension-open eligibility (R → block 1)
    age = case.first_of_kind("age")
    join = case.first_of_kind("join_date")
    if age is not None and join is not None:
        years = (base - _to_date(join.data["date"])).days / 365.25
        ret = case.first_of_kind("retirement_benefit")
        has_ret = bool(ret.data.get("included")) if ret else False
        eligible = int(age.data["years"]) >= 55 and (years >= 5 or has_ret)
        add(1, "rule_derived",
            "연금개시요건 충족 여부: {} (만 {}세, 가입 {:.1f}년, 퇴직급여 포함 {}) "
            "| rule_source=만55세 이상 + 가입 5년 이상(퇴직급여 포함 시 55세만) — 행내 공식 기준 "
            "| rule_as_of={} | rule_id=PENSION-OPEN-01".format(
                "충족" if eligible else "미충족", age.data["years"], years,
                "Y" if has_ret else "N", base.isoformat()),
            as_of=base.isoformat())

    return out


# ---------------------------------------------------------------------------
# Layer 3 — 9-Block rendering + supply rendering
# ---------------------------------------------------------------------------
def all_items(case: CanonicalCase, derived: List[CanonicalItem]) -> List[CanonicalItem]:
    return list(case.evidence) + list(derived)


def all_ids(case: CanonicalCase, derived: List[CanonicalItem]) -> List[str]:
    return [it.id for it in all_items(case, derived)]


def render_blocks(case: CanonicalCase, derived: List[CanonicalItem]) -> str:
    """System-observed blocks first (1-8), human-authored context last (9).

    Within a block: authored items in canonical order, then derived items in
    D-id order. Stable ids are printed so provenance survives re-rendering.
    """
    by_block: Dict[int, List[CanonicalItem]] = {n: [] for n in BLOCK_TITLES}
    for it in case.evidence:
        by_block[it.block].append(it)
    for it in derived:
        by_block[it.block].append(it)

    parts = [RENDER_INTRO, ""]
    for n in range(1, 10):
        parts.append(f"### {n}. {BLOCK_TITLES[n]}")
        if n == 6:
            parts.append(BLOCK6_NOTE)
        if n == 9:
            parts.append(BLOCK9_NOTE)
        items = by_block[n]
        if not items:
            parts.append("- (이 블록에 제공된 항목 없음)")
        for it in items:
            parts.append(f"- [{it.id}] [{TYPE_LABEL[it.evidence_type]}] {it.text}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_supply(case: CanonicalCase) -> str:
    """Supply materials for the prompt's knowledge side (Contract §2-§3).

    The model may only REFERENCE these by id; cards/originals/paths are
    restored from here at render time, never re-written by the model.
    """
    s = case.supply
    parts: List[str] = []
    prods = s.get("product_candidates") or []
    if prods:
        parts.append("### Candidate Pool (특정 상품 수준 연결이 허용되는 후보 — 이 밖의 상품명 생성 금지. "
                     "추천 시 product_id로만 참조하고, 추천 사유는 고객 Evidence·관리 방향과 상품 특성의 적합성으로 직접 작성한다)")
        for p in prods:
            grade = (f"위험등급 {p['risk_grade']}등급({p.get('risk_level_label','')})"
                     if p.get("risk_grade") is not None else "위험등급 해당없음(원리금보장)")
            ret = (f"최근 수익률 {p['return_recent']:+.1%} ({p.get('return_period','')}, 기준일 {p.get('return_as_of','')})"
                   if p.get("return_recent") is not None else "수익률 미확인")
            line = (f"- {p['product_id']}: {p['name']} | 유형 {p.get('product_type','')} | "
                    f"{grade} | {ret} | 특징: {p.get('features','')}")
            if p.get("fee_note"):
                line += f" | {p['fee_note']}"
            if p.get("maturity_note"):
                line += f" | {p['maturity_note']}"
            # sellable: True/False = 원천 확인값, None = 미확인 — 판매 가능으로 단정하지 않고
            # '상담 전 확인' 대상으로 전달한다 (HD-P2-GATE2: null을 사실처럼 보완 금지).
            if p.get("sellable") is True:
                sell = "판매 가능"
            elif p.get("sellable") is False:
                sell = "판매 불가"
            else:
                sell = "판매 가능 여부 미확인 (상담 전 확인 필요)"
            line += (f" | {sell}"
                     f" | 채널 {'/'.join(p.get('channels') or []) or '미확인'}")
            parts.append(line)
        parts.append("")
    tips = s.get("hot_tips") or []
    if tips:
        parts.append("### Hot Tip / Guide 원문 (tip_id로만 참조 — 원문을 재작성하지 않는다. "
                     "field_hot_tip은 현장 노하우이며 제도·세제·실행 가능 여부는 official_guide가 우선한다)")
        for t in tips:
            meta = []
            if t.get("author"):
                meta.append(f"작성자 {t['author']}")
            if t.get("written_at"):
                meta.append(f"작성일 {t['written_at']}")
            if t.get("likes") is not None:
                meta.append(f"좋아요 {t['likes']} (현장 공감도 신호 — 공식성 근거 아님)")
            if t.get("source"):
                meta.append(f"출처 {t['source']}")
            parts.append(f"- {t['tip_id']} [{t.get('kind','field_hot_tip')}] 「{t.get('title','')}」: "
                         f"\"{t.get('body','')}\" ({' · '.join(meta)})")
        parts.append("")
    screens = s.get("screens") or []
    if screens:
        parts.append("### 실행 화면 (screen_id로만 참조 — 여기 없는 화면번호·경로를 만들지 않는다)")
        for sc in screens:
            if sc.get("surface") == "staff":
                loc = f"직원 단말 {sc.get('screen_no','')} {sc.get('screen_name','')}"
            else:
                loc = f"고객 StarBanking {sc.get('menu_path','')}"
            parts.append(f"- {sc['screen_id']}: {loc} — {sc.get('actions','')}")
        parts.append("")
    return "\n".join(parts).rstrip() + ("\n" if parts else "")


def supply_ids(case: CanonicalCase) -> Dict[str, set]:
    s = case.supply
    return {
        "products": {p["product_id"] for p in s.get("product_candidates") or []},
        "tips": {t["tip_id"] for t in s.get("hot_tips") or []},
        "screens": {sc["screen_id"] for sc in s.get("screens") or []},
        "unsellable_products": {p["product_id"] for p in s.get("product_candidates") or []
                                if p.get("sellable") is False},
    }
