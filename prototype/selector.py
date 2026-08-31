# -*- coding: utf-8 -*-
"""
P3-A Minimal Knowledge Selection Layer.

Replaces ONLY the Official Knowledge / Knowledge Gap portion of the manual
per-case knowledge_pack. Everything else stays exactly as before:

    load_knowledge_items(case_id)                       (interface unchanged)
      -> P3A_KNOWLEDGE_SELECTION=1 ? this module : Frozen knowledge_pack.md
      -> List[KnowledgeItem] with the same 5-field structure
      -> existing v3 prompt / validators / RUN record (untouched)

What it does (Selection minimal rules — P3-A instruction):
  1. Candidate search by the Human-defined Knowledge Need topic
     (design/P3A_KNOWLEDGE_NEEDS.md — needs are transcribed from K-REQ /
     Frozen pack composition, never generated here).
  2. status gate  : SUPERSEDED excluded (logged); PROVISIONAL / CONFLICT
     selected but explicitly flagged (not silently trusted).
  3. authority gate (by purpose): 제도/세제/eligibility/실행가능성 needs
     require T1/T2 as 판단 근거. T3/Public-only items are still delivered but
     demoted to "확인 필요 상태" — never dropped, never promoted.
  4. Authority and Relevance are NEVER combined into one score. Gates run in
     fixed order (status -> authority); relevance is only a match count kept
     for the log.
  5. If a Knowledge Gap (KG-xxx) matches the need, its consume_text becomes
     the K-item body (knowledge/KNOWLEDGE_GAPS.md contract). If nothing
     matches at all, an explicit synthetic Gap item is generated with the
     epistemic boundary "현재 확인한 Knowledge 범위에서 확인되지 않는다"
     (never "존재하지 않는다").

What it does NOT do: LLM calls, vector/embedding/hybrid search, reranking,
product selection, PRD/HT/TALK/SCR retrieval (those pack items are kept from
the Frozen pack verbatim via `manual_keep`).

Standard library only.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import runtime  # safe: runtime imports this module only lazily inside a function

REPO_ROOT = Path(__file__).resolve().parent.parent
NEEDS_FILE = REPO_ROOT / "design" / "P3A_KNOWLEDGE_NEEDS.md"
OK_FILE = REPO_ROOT / "knowledge" / "OFFICIAL_KNOWLEDGE.md"
KG_FILE = REPO_ROOT / "knowledge" / "KNOWLEDGE_GAPS.md"
OUT_DIR = Path(__file__).resolve().parent / "out"


def _norm(s: str) -> str:
    """Normalization for matching only: drop spaces/brackets, casefold."""
    return re.sub(r"[\s\[\]()]+", "", s).casefold()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Registry parsing (md contract per knowledge/README.md — fields kept verbatim)
# ---------------------------------------------------------------------------
def _parse_table_fields(block: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", block, re.M):
        key = m.group(1).strip().strip("*")
        if key in ("필드", "---"):
            continue
        fields[key] = m.group(2).strip()
    return fields


def _parse_bullet_section(block: str, header: str) -> List[str]:
    """Bullets under a '**Header**' line until the next '**' header or block end."""
    m = re.search(rf"^\*\*{header}\*\*.*$", block, re.M)
    if not m:
        return []
    rest = block[m.end():]
    stop = re.search(r"^\*\*[A-Za-z]", rest, re.M)
    if stop:
        rest = rest[: stop.start()]
    out: List[str] = []
    for ln in rest.splitlines():
        bm = re.match(r"^- (.+)$", ln)
        if bm:
            out.append(bm.group(1).strip())
        elif out and ln.strip():
            out[-1] += "\n" + ln.rstrip()
    return out


def parse_official_knowledge(path: Path = OK_FILE) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    items: List[Dict[str, Any]] = []
    for block in re.split(r"^(?=### OK-\d{3}\. )", text, flags=re.M):
        head = re.match(r"^### (OK-\d{3})\. (.+)$", block, re.M)
        if not head:
            continue
        f = _parse_table_fields(block)
        items.append({
            "id": head.group(1),
            "title": head.group(2).strip(),
            "source": f.get("source", ""),
            "authority": f.get("authority", ""),
            "as_of": f.get("as_of", ""),
            "status": f.get("status", ""),
            "topics": f.get("topics", ""),
            "applicability_tags": f.get("applicability_tags", ""),
            "content": _parse_bullet_section(block, "Content"),
            "limitation": _parse_bullet_section(block, "Limitation"),
        })
    return items


def parse_knowledge_gaps(path: Path = KG_FILE) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    items: List[Dict[str, Any]] = []
    for block in re.split(r"^(?=### KG-\d{3}\. )", text, flags=re.M):
        head = re.match(r"^### (KG-\d{3})\. (.+)$", block, re.M)
        if not head:
            continue
        f = _parse_table_fields(block)
        items.append({
            "id": head.group(1),
            "title": head.group(2).strip(),
            "gap_type": f.get("gap_type", ""),
            "topic": f.get("topic", ""),
            "what_is_missing": f.get("what_is_missing", ""),
            "what_exists_instead": f.get("what_exists_instead", ""),
            "verified_by": f.get("verified_by", ""),
            "consume_text": f.get("consume_text", ""),
            "related": f.get("related", ""),
            "status": f.get("status", ""),
        })
    return items


# ---------------------------------------------------------------------------
# Needs parsing (design/P3A_KNOWLEDGE_NEEDS.md — Human-defined, see file header)
# ---------------------------------------------------------------------------
def load_needs(case_id: str, path: Path = NEEDS_FILE) -> Tuple[List[Dict[str, Any]], List[str]]:
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(case_id)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise ValueError(f"P3A_KNOWLEDGE_NEEDS.md has no section for {case_id}")
    section = m.group(1)
    needs: List[Dict[str, Any]] = []
    for block in re.split(r"^(?=### )", section, flags=re.M):
        head = re.match(r"^### (KN-\d+)", block)
        if head:
            f = _parse_table_fields(block)
            needs.append({
                "need_id": head.group(1),
                "origin": f.get("origin", ""),
                "purpose": f.get("purpose", ""),
                "authority_required": f.get("authority_required", ""),
                "topics": [t.strip() for t in f.get("topic", "").split(";") if t.strip()],
                "need_text": f.get("need_text", ""),
            })
    manual_keep: List[str] = []
    mk = re.search(r"^### manual_keep\s*$(.*?)(?=^### |\Z)", section, re.S | re.M)
    if mk:
        manual_keep = re.findall(r"^- (K-\d{3})", mk.group(1), re.M)
    if not needs:
        raise ValueError(f"{case_id}: no KN- needs found")
    return needs, manual_keep


# ---------------------------------------------------------------------------
# Matching (relevance = candidate topic token contained in a need topic phrase)
# ---------------------------------------------------------------------------
def _match_tokens(entry_csv: str, need_topics: List[str]) -> List[str]:
    matched = []
    norm_topics = [_norm(t) for t in need_topics]
    for tok in [t.strip() for t in entry_csv.split(",") if t.strip()]:
        nt = _norm(tok)
        if nt and any(nt in topic for topic in norm_topics):
            matched.append(tok)
    return matched


def _match_ok(item: Dict[str, Any], need: Dict[str, Any]) -> List[str]:
    return (_match_tokens(item["topics"], need["topics"])
            + _match_tokens(item["applicability_tags"], need["topics"]))


def _match_kg(item: Dict[str, Any], need: Dict[str, Any]) -> List[str]:
    return _match_tokens(item["topic"], need["topics"])


def _has_official_authority(authority: str) -> bool:
    return bool(re.search(r"\bT1\b|T1-|\bT2\b|T2-", authority))


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------
SYNTHETIC_GAP_TEXT = (
    "[확인되지 않음] 이 Knowledge Need에 해당하는 항목이 현재 확인한 Knowledge 범위"
    "(knowledge/ Registry — OFFICIAL_KNOWLEDGE·KNOWLEDGE_GAPS)에서 확인되지 않았다. "
    "[확인된 범위] 위 Registry의 등록 항목까지만 탐색되었다 — 부재는 탐색 범위의 한계일 수 "
    "있으며 제도적 불가·불존재를 의미하지 않는다. "
    "[사용 경계] 이 주제에 대한 업무 사실·제도 규칙·수치·원인 설명을 임의로 생성·단정하지 않는다. "
    "[추가 확인] 필요한 경우 공식 자료·담당 부서·업무 화면 확인으로 연결한다."
)


def select_for_case(case_id: str, needs: Optional[List[Dict[str, Any]]] = None,
                    manual_keep: Optional[List[str]] = None,
                    keep_registry_ids: Optional[set] = None) -> Tuple[List["runtime.KnowledgeItem"], Dict[str, Any]]:
    """Return (K-items in the existing 5-field structure, selection log).

    needs/manual_keep default to the Human-defined file (P3-A path). Callers
    may pass needs programmatically (Hybrid re-assembly, Mock v0) — matching,
    gates and item assembly stay identical.
    keep_registry_ids: optional post-retrieval filter (Hybrid LLM pruning
    result) — only candidates whose registry id is in the set are assembled;
    gates/flags are still applied here (LLM never decides trust level).
    """
    if needs is None:
        needs, manual_keep = load_needs(case_id)
    elif manual_keep is None:
        manual_keep = []
    ok_items = parse_official_knowledge()
    kg_items = parse_knowledge_gaps()

    log: Dict[str, Any] = {"case_id": case_id, "needs": [], "manual_keep": manual_keep,
                           "selected": [], "excluded": []}

    # Pass 1 — match every candidate against every need (topic only; no scoring).
    # A candidate hit by several needs is attributed to the need with the most
    # matched tokens (tie → earlier need): deterministic attribution, so the
    # Case Relevance line names the need the item actually answers.
    per_candidate: Dict[str, Dict[str, Any]] = {}
    need_logs = {n["need_id"]: {"need_id": n["need_id"], "origin": n["origin"],
                                "purpose": n["purpose"], "candidates": []} for n in needs}
    for need in needs:
        for kind, pool, matcher in (("OK", ok_items, _match_ok), ("KG", kg_items, _match_kg)):
            for it in pool:
                matched = matcher(it, need)
                if not matched:
                    continue
                if kind == "OK" and it["status"].startswith("SUPERSEDED"):
                    need_logs[need["need_id"]]["candidates"].append(
                        {"id": it["id"], "matched": matched, "gate": "EXCLUDED (status=SUPERSEDED)"})
                    log["excluded"].append({"need": need["need_id"], "id": it["id"],
                                            "reason": "SUPERSEDED"})
                    continue
                need_logs[need["need_id"]]["candidates"].append(
                    {"id": it["id"], "matched": matched,
                     "gate": "SELECTED" if kind == "OK" else "SELECTED (Knowledge Gap)"})
                cur = per_candidate.get(it["id"])
                if cur is None or len(matched) > len(cur["matched"]):
                    per_candidate[it["id"]] = {"kind": kind, "item": it, "need": need,
                                               "matched": matched}

    # Pass 2 — gates + assembly order: by need (file order), OK before KG,
    # OK sorted by match count desc then id. Gates run status → authority;
    # relevance is never combined with authority into a score.
    picked: List[Tuple[str, Dict[str, Any], Dict[str, Any], List[str], List[str]]] = []
    for need in needs:
        cands = [c for c in per_candidate.values() if c["need"] is need]
        if keep_registry_ids is not None:
            pruned = [c for c in cands if c["item"]["id"] not in keep_registry_ids]
            for c in pruned:
                log["excluded"].append({"need": need["need_id"], "id": c["item"]["id"],
                                        "reason": "LLM_PRUNED"})
            cands = [c for c in cands if c["item"]["id"] in keep_registry_ids]
        ok_matches = sorted((c for c in cands if c["kind"] == "OK"),
                            key=lambda c: (-len(c["matched"]), c["item"]["id"]))
        kg_matches = [c for c in cands if c["kind"] == "KG"]
        for c in ok_matches:
            it = c["item"]
            flags: List[str] = []
            if it["status"].startswith("PROVISIONAL"):
                flags.append("PROVISIONAL — 확정 Fact 아님, 확인 필요 상태로만 사용")
            if it["status"].startswith("CONFLICT"):
                flags.append("CONFLICT — SOURCE_CONFLICTS의 SC 항목 참조, 임의 통합·해소 금지")
            # authority gate by purpose (T1/T2 required for 판단 근거)
            if need["authority_required"].startswith("T1/T2") and not _has_official_authority(it["authority"]):
                flags.append("공식(T1/T2) 근거 미확보 — 판단 근거 아님, 확인 필요 상태로만 전달"
                             " (Operational Check Needed)")
            picked.append(("OK", it, need, c["matched"], flags))
        for c in kg_matches:
            picked.append(("KG", c["item"], need, c["matched"], []))
        if not cands:
            # Gap is a normal outcome, not a failure — deliver it explicitly.
            picked.append(("SYNTH_GAP", {"id": f"GAP({need['need_id']})",
                                         "title": f"Knowledge 미확인 — {need['need_text'][:60]}"},
                           need, [], []))
            need_logs[need["need_id"]]["candidates"].append(
                {"id": None, "gate": "NO_MATCH → explicit synthetic gap"})
    log["needs"] = [need_logs[n["need_id"]] for n in needs]

    # --- assemble K-items (existing 5-field structure) -----------------------
    items: List[runtime.KnowledgeItem] = []

    def relevance_text(need: Dict[str, Any]) -> str:
        return (f"이 Case의 Knowledge Need {need['need_id']} ({need['origin']}) 대응: "
                f"{need['need_text']}")

    for kind, it, need, matched, flags in picked:
        kid = f"K-{len(items) + 1:03d}"
        if kind == "OK":
            authority = it["authority"] + f" / status={it['status']} / as_of={it['as_of']}"
            if flags:
                authority += " / ⚠ " + " · ".join(flags)
            limitation = "\n".join(f"  · {b}" for b in it["limitation"]).lstrip() or "—"
            if flags:
                limitation += "\n  · (Selector 부착) " + " · ".join(flags)
            fields = {
                "Knowledge": "\n".join(f"  · {b}" for b in it["content"]).lstrip(),
                "Case Relevance": relevance_text(need),
                "Limitation": limitation,
                "Authority / Status": authority,
                "Source / Location": f"{it['id']} ({it['source']})",
            }
            items.append(runtime.KnowledgeItem(kid, it["title"], "Source-derived (Registry)", fields))
        elif kind == "KG":
            fields = {
                "Knowledge": it["consume_text"],
                "Case Relevance": relevance_text(need),
                "Limitation": ("Knowledge Gap(부정 확인) 항목 — 본문 [사용 경계]가 Usage Boundary다. "
                               "확인되지 않음(부재)을 '불가'·'불존재'로 승격하지 않는다. "
                               f"인접 확인 자료: {it['what_exists_instead']}"),
                "Authority / Status": (f"Knowledge Gap ({it['gap_type']}) / status={it['status']} "
                                       f"/ verified_by: {it['verified_by']}"),
                "Source / Location": f"{it['id']} (knowledge/KNOWLEDGE_GAPS.md; related: {it['related']})",
            }
            items.append(runtime.KnowledgeItem(kid, it["title"],
                                               "Negative-confirmation (Knowledge Gap)", fields))
        else:  # SYNTH_GAP
            fields = {
                "Knowledge": SYNTHETIC_GAP_TEXT,
                "Case Relevance": relevance_text(need),
                "Limitation": "부재를 '불가'·'불존재'로 승격하지 않는다. 임의의 원인·정의 설명을 생성하지 않는다.",
                "Authority / Status": "Knowledge Gap (selector 탐색 결과 0건) / 조회 시점 Registry 기준",
                "Source / Location": "P3-A Minimal Selector (design/P3A_KNOWLEDGE_NEEDS.md)",
            }
            items.append(runtime.KnowledgeItem(kid, it["title"],
                                               "Negative-confirmation (Knowledge Gap)", fields))
        log["selected"].append({"kid": kid, "kind": kind, "registry_ref": it["id"],
                                "need_ref": need["need_id"], "matched": matched, "flags": flags})

    # --- manual_keep: non-official items from the Frozen pack, verbatim ------
    if manual_keep:
        frozen_items, _, _ = runtime._load_knowledge_items_manual(case_id)
        by_id = {k.kid: k for k in frozen_items}
        for orig_kid in manual_keep:
            src = by_id.get(orig_kid)
            if src is None:
                raise ValueError(f"{case_id}: manual_keep {orig_kid} not in Frozen pack")
            kid = f"K-{len(items) + 1:03d}"
            items.append(runtime.KnowledgeItem(kid, src.title, src.basis_type, dict(src.fields)))
            log["selected"].append({"kid": kid, "kind": "MANUAL_KEEP",
                                    "registry_ref": f"frozen:{orig_kid}", "need_ref": None,
                                    "matched": [], "flags": []})
    return items, log


def load_knowledge_items_selected(case_id: str):
    """Drop-in for runtime.load_knowledge_items — same (items, path, sha) shape."""
    items, log = select_for_case(case_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    log["registry_sha256"] = {"OFFICIAL_KNOWLEDGE.md": _sha256(OK_FILE),
                              "KNOWLEDGE_GAPS.md": _sha256(KG_FILE),
                              "P3A_KNOWLEDGE_NEEDS.md": _sha256(NEEDS_FILE)}
    (OUT_DIR / f"p3a_selection_{case_id}.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return items, f"selector:{NEEDS_FILE.relative_to(REPO_ROOT)}", _sha256(NEEDS_FILE)
