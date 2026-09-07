# -*- coding: utf-8 -*-
"""
demo_isa_brief_pipeline.py
──────────────────────────────────────────────────────────────────────────────
기획자에게 "김서연 고객님 [타행 ISA 만기 D-3] 화면이 어떻게 만들어지는지"를
Python 하나로 끝까지 보여주기 위한 데모.

    DATA  →  CONTEXT  →  KNOWLEDGE 검색  →  LLM 추론  →  후처리/검증  →  화면

같은 고객을 두고 아래 순서로 실행한다.

  0. PURE LLM
     고객 Raw Data만 주고 자유롭게 답변 (비교용 — 왜 이대로는 못 쓰는지)

  1. DATA → CONTEXT (결정론, LLM 없음)
     원천 데이터(계좌·ISA·행동로그)를 Snapshot / Event / Signal / Constraint 로 정리
     D-3, 60일 시한 종료일, 추가공제 상한 300만 같은 값은 여기서 '계산'된다

  2. KNOWLEDGE 검색 (결정론, LLM 없음)
     Context 에서 뽑은 상황 태그로 지식베이스(knowledge/*.md 레지스트리)를 검색
     → 공식 제도(T2) / 현장 Hot Tip(T3) / 화면 / 상품 항목을 권위등급과 함께 선별

  3. LLM 추론 (Gemma 4, 1회 호출)
     Role + Context + Constraint + Knowledge + Workflow + Output Contract
     → 화면 섹션에 1:1 대응하는 JSON 만 받는다

  4. 후처리 / 검증 (결정론, LLM 없음)
     JSON 파싱·스키마 → 투자성향(C1)·금지표현 검사 → T3 단독 사실 ⚠ 경고 자동 부착
     → 화면번호·Hot Tip 카드·상품 후보는 레지스트리에서 '조회'해 결합

  5. 화면 렌더
     기획자가 본 최종 화면 텍스트로 출력 (각 블록의 출처 [DATA]/[KB]/[LLM]/[RULE] 표시)

실행:
    python3 demo_isa_brief_pipeline.py                # GEMINI_API_KEY 있으면 실제 호출
    python3 demo_isa_brief_pipeline.py --mock         # API 없이 전체 흐름 시연 (권장: 발표용)
    python3 demo_isa_brief_pipeline.py --dry-run      # 프롬프트만 구성, 호출 안 함
    python3 demo_isa_brief_pipeline.py --show-prompt  # LLM에 실제 전달되는 프롬프트 전문 출력
    python3 demo_isa_brief_pipeline.py --skip-pure    # STEP 0(Pure LLM 비교) 생략
    python3 demo_isa_brief_pipeline.py --out run.json # 실행 기록 저장

전제:
    - 표준 라이브러리만 사용 (prototype/runtime.py 와 동일한 REST 호출 방식)
    - 실제 호출 시 환경변수 GEMINI_API_KEY 필요 (없으면 자동으로 --mock 으로 진행)
    - 저장소 루트에서 실행하면 knowledge/*.md 에서 원문 발췌를 실제로 읽어온다
      (파일이 없어도 내장 발췌로 동작)
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from textwrap import dedent

ROOT = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(ROOT, "knowledge")

MODEL_ID = os.environ.get("GEMMA_MODEL", "gemma-4-31b-it")
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"
API_KEY_ENV = "GEMINI_API_KEY"

W = 88


# =============================================================================
# 공통 출력
# =============================================================================

def banner(title: str, char: str = "=") -> None:
    print("\n" + char * W)
    print(title)
    print(char * W)


def section(title: str) -> None:
    print("\n" + "─" * W)
    print(title)
    print("─" * W)


def explain(added: str, point: str) -> None:
    section("[개발 관점]")
    print(f"이번 단계에서 한 것   : {added}")
    print(f"기획자가 볼 포인트    : {point}")


def won(n: int) -> str:
    """만원 단위 정수를 '8,000만원' 형태로."""
    return f"{n:,}만원"


def cont(text: str, n: int = 4) -> str:
    """여러 줄 문자열을 dedent 블록 안에 끼워 넣을 때 둘째 줄부터 n칸 들여쓰기."""
    lines = text.splitlines()
    return "\n".join(lines[:1] + [" " * n + ln for ln in lines[1:]])


# =============================================================================
# 1. DATA — 시스템이 보유한 원천 데이터 (실제로는 계정계 / CRM / 채널 로그)
# =============================================================================

RAW_DATA = {
    "analysis": {"date": "2026-09-04", "time": "07:30"},
    "customer": {
        "id": "10274-38562",
        "name": "김서연",
        "age": 44,
        "gender": "여",
        "grade": "VIP",                       # 스타클럽 등급
        "risk_profile": "위험중립형",           # 투자성향 (분석일 2026-06-30)
        "risk_profile_date": "2026-06-30",
    },
    "irp": {
        "open_date": "2019-03-15",
        "default_option": {"registered": True, "portfolio": "뿔려드림2호"},
        "eval_amount": 4500,                  # 만원
        "return_1y": 0.031,
        "tax_credit_remaining": 500,          # 당해 세액공제 잔여한도 (만원)
        "last_product_date": "2026-06-12",
        "holdings": [
            {"name": "KB 정기예금 12M", "type": "원리금보장형", "amount": 2000, "risk_grade": None, "maturity": "2027-06-12"},
            {"name": "수협은행 정기예금 36M", "type": "원리금보장형", "amount": 800, "risk_grade": None, "maturity": "2028-03-20"},
            {"name": "KB 스타 단기국공채 (채권형)", "type": "실적배당형", "amount": 1500, "risk_grade": 5, "maturity": None},
        ],
        "idle_cash": 200,                     # 고유계정대(대기자금)
    },
    "external": {
        "isa": {"bank": "신한은행", "amount": 8000, "open_date": "2023-09-07", "maturity": "2026-09-07"},
    },
    "activity": [
        {"date": "2026-09-02", "channel": "스타뱅킹", "event": "IRP ETF 상품 조회"},
        {"date": "2026-08-30", "channel": "스타뱅킹", "event": "IRP 잔고 조회"},
    ],
    "consult_history": [],
}


def raw_data_block(d: dict) -> str:
    c, irp, isa = d["customer"], d["irp"], d["external"]["isa"]
    holds = "\n".join(
        f"- {h['name']} | {h['type']} | {won(h['amount'])}"
        f" | 위험등급 {h['risk_grade'] or '해당없음'} | 만기 {h['maturity'] or '—'}"
        for h in irp["holdings"]
    )
    acts = "\n".join(f"- {a['date']} {a['channel']} {a['event']}" for a in d["activity"])
    return dedent(f"""
    고객명: {c['name']} ({c['id']}) / {c['age']}세 / {c['gender']} / 스타클럽 {c['grade']}
    투자성향: {c['risk_profile']} (분석일 {c['risk_profile_date']})
    IRP 신규일: {irp['open_date']} / 디폴트옵션: {irp['default_option']['portfolio']} 등록
    IRP 평가금액: {won(irp['eval_amount'])} / 최근 1년 수익률 {irp['return_1y']*100:+.1f}%
    세액공제 잔여한도: {won(irp['tax_credit_remaining'])} / 최근 상품 신규일 {irp['last_product_date']}
    고유계정대(대기자금): {won(irp['idle_cash'])}

    [보유상품]
    {cont(holds)}

    [타행 ISA]
    - {isa['bank']} ISA {won(isa['amount'])} / 가입 {isa['open_date']} / 만기 {isa['maturity']}

    [최근 채널 행동]
    {cont(acts)}
    """).strip()


# =============================================================================
# 1'. DATA → CONTEXT — 결정론 계산 (LLM 이 계산하게 두지 않는다)
# =============================================================================

# 투자성향 → 권유 가능한 펀드 최대 위험등급 (1등급이 가장 위험). prototype/runtime.py C2 와 동일.
PROFILE_MIN_FUND_GRADE = {"안정형": 6, "안정추구형": 5, "위험중립형": 4, "적극투자형": 3, "공격투자형": 1}
GRADE_LABEL = {1: "매우높은위험", 2: "높은위험", 3: "다소높은위험", 4: "보통위험", 5: "낮은위험", 6: "매우낮은위험"}
# 디폴트옵션 위험도 → 허용 최소 투자성향 index (안정형0 … 공격투자형4). prototype/runtime.py C3 와 동일.
PROFILE_SCALE = ["안정형", "안정추구형", "위험중립형", "적극투자형", "공격투자형"]
DO_MIN_PROFILE = {"지켜드림": 0, "알파드림": 1, "뿔려드림": 2, "모두드림": 4}


def d(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def build_context(raw: dict) -> dict:
    c, irp, isa = raw["customer"], raw["irp"], raw["external"]["isa"]
    today = d(raw["analysis"]["date"])
    total = irp["eval_amount"]

    guaranteed = sum(h["amount"] for h in irp["holdings"] if h["type"] == "원리금보장형")
    performance = sum(h["amount"] for h in irp["holdings"] if h["type"] == "실적배당형")
    idle = irp["idle_cash"]
    assert guaranteed + performance + idle == total, "보유상품 합계가 평가금액과 다름"

    maturity = d(isa["maturity"])
    dday = (maturity - today).days
    window_end = maturity + timedelta(days=60)             # OK-001: 만기일 60일 이내
    extra_credit_cap = min(int(isa["amount"] * 0.10), 300)  # OK-001: 전환금 10%, 최대 300만
    isa_hold_years = (maturity - d(isa["open_date"])).days / 365.25

    min_grade = PROFILE_MIN_FUND_GRADE[c["risk_profile"]]
    do_family = re.sub(r"\d+호?$", "", irp["default_option"]["portfolio"])
    do_ok = PROFILE_SCALE.index(c["risk_profile"]) >= DO_MIN_PROFILE.get(do_family, 99)

    etf_views = [a for a in raw["activity"] if "ETF" in a["event"]]

    tags = ["ISA만기", "전환입금", "세액공제", "타행ISA"]
    if guaranteed / total >= 0.5:
        tags.append("원리금보장중심")
    if etf_views:
        tags.append("ETF관심")
    if idle / total > 0.20:
        tags.append("대기자금과다")
    tags.append(c["risk_profile"])

    return {
        "snapshot": {
            "customer": f"{c['name']} / {c['age']}세 / {c['gender']} / {c['grade']} / {c['risk_profile']}",
            "irp_total": total,
            "mix": {
                "원리금보장형": (guaranteed, round(guaranteed / total * 100)),
                "실적배당형": (performance, round(performance / total * 100)),
                "고유계정대": (idle, round(idle / total * 100)),
            },
            "return_1y": irp["return_1y"],
            "tax_credit_remaining": irp["tax_credit_remaining"],
            "default_option": irp["default_option"]["portfolio"],
            "holdings_count": len(irp["holdings"]),
        },
        "event": {
            "isa_bank": isa["bank"],
            "isa_amount": isa["amount"],
            "isa_maturity": isa["maturity"],
            "dday": dday,
            "window_end": window_end.isoformat(),
            "extra_credit_cap": extra_credit_cap,
            "isa_hold_years": round(isa_hold_years, 1),
        },
        "signal": {
            "etf_views": [f"{a['date']} {a['channel']} {a['event']}" for a in etf_views],
            "note": "채널 행동 로그는 시스템 탐지값이며 고객의 의사표현이 아님 (관심 '가능성'으로만 취급)",
        },
        "constraint": {
            "risk_profile": c["risk_profile"],
            "allowed_fund_grades": [g for g in range(min_grade, 7)],
            "allowed_fund_grade_label": f"{min_grade}등급({GRADE_LABEL[min_grade]}) 이하만 권유 가능",
            "default_option_eligible": do_ok,
        },
        "tags": tags,
    }


def context_block(ctx: dict) -> str:
    s, e, sig, con = ctx["snapshot"], ctx["event"], ctx["signal"], ctx["constraint"]
    mix = " / ".join(f"{k} {won(v[0])}({v[1]}%)" for k, v in s["mix"].items())
    etf = cont("\n".join(f"- {x}" for x in sig["etf_views"]) or "- (없음)")
    return dedent(f"""
    [SNAPSHOT]
    - 고객: {s['customer']}
    - IRP 평가금액 {won(s['irp_total'])} : {mix}
    - 최근 1년 수익률 {s['return_1y']*100:+.1f}% / 세액공제 잔여한도 {won(s['tax_credit_remaining'])}
    - 디폴트옵션 {s['default_option']} 등록 / 보유상품 {s['holdings_count']}건

    [EVENT / TIMING]  ← 시스템 계산
    - {e['isa_bank']} ISA {won(e['isa_amount'])} 만기 {e['isa_maturity']} (D-{e['dday']})
    - IRP 전환입금 가능 시한: 만기일로부터 60일 → {e['window_end']} 까지
    - 전환 시 추가 세액공제 상한: min({won(e['isa_amount'])}×10%, 300만원) = {won(e['extra_credit_cap'])}
    - ISA 보유기간 약 {e['isa_hold_years']}년 (의무기간 3년 충족)

    [SYSTEM DETECTED SIGNAL]
    {etf}
    ※ {sig['note']}

    [CONSTRAINT]
    - 투자성향 {con['risk_profile']} → {con['allowed_fund_grade_label']}
    - 디폴트옵션 {s['default_option']} 보유 적격: {'적합' if con['default_option_eligible'] else '부적합'}
    """).strip()


# =============================================================================
# 2. KNOWLEDGE — 지식베이스와 검색
#    실제 저장소의 knowledge/*.md 레지스트리 항목을 그대로 인덱스로 쓴다.
#    (id / 권위등급 / 상황태그 / 원문 위치). 원문 발췌는 파일이 있으면 파일에서 읽는다.
# =============================================================================

KNOWLEDGE_BASE = [
    {
        "id": "OK-001", "kind": "official", "authority": "T2-InternalGuide",
        "title": "ISA 만기자금의 연금계좌 전환입금 — 60일 시한·한도·추가 세액공제",
        "tags": ["ISA만기", "전환입금", "세액공제", "60일", "300만원"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-001.",
        "excerpt": (
            "ISA 계좌 만기일로부터 60일 이내에 만기자금의 전부 또는 일부를 연금계좌로 추가 납입 허용 + 세액공제 혜택. "
            "연간 납입한도 1,800만원과 별도. 추가 세액공제: 전환금액의 10%, 최대 300만원. "
            "확인·처리 위치: [04-10-099] 세금우대관련조회 / 창구 [01-12-213] 입금/입금예약(거래구분 'ISA 만기자금 입금'). "
            "Limitation: 60일 기산 방식(초일 산입 등)은 원천에 없음."
        ),
        "screens": ["01-12-213", "04-10-099"],
    },
    {
        "id": "OK-008", "kind": "official", "authority": "T2-InternalGuide",
        "title": "연금계좌 세액공제 구조 — 한도·구간별 공제율·결정세액 조건",
        "tags": ["세액공제", "공제율", "결정세액"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-008.",
        "excerpt": "공제율: 총급여 5,500만원 이하 16.5% / 초과 13.2%. 결정세액이 공제액보다 적으면 최대 환급을 받지 못함(개별 확인 필요).",
    },
    {
        "id": "OK-009", "kind": "official", "authority": "T2-InternalGuide",
        "title": "IRP 중도해지·연금외수령 과세 구조",
        "tags": ["세액공제", "중도해지", "전환입금"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-009.",
        "excerpt": "중도해지 또는 연금 외 수령 시 세액공제 받은 납입원금·운용수익에 기타소득세 16.5% 부과. 세액공제 받지 않은 원금은 과세 제외.",
        "must_disclose": "중도해지 시 기타소득세 16.5% 부과는 함께 고지",
    },
    {
        "id": "OK-005", "kind": "official", "authority": "T2-InternalGuide",
        "title": "디폴트옵션 적용 시점 규칙(2주/6주) — 입금 후 운용 경로",
        "tags": ["전환입금", "디폴트옵션", "입금예정상품"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-005.",
        "excerpt": "입금 후 운용지시가 없으면 2주(옵트인 6주) 후 등록된 디폴트옵션으로 운용. 입금예정상품을 등록하면 입금 시 자동 매수.",
    },
    {
        "id": "OK-023", "kind": "official", "authority": "T2-InternalGuide",
        "title": "은행 퇴직연금 ETF 매매 체결 구조·라인업",
        "tags": ["ETF관심", "ETF"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-023.",
        "excerpt": "은행 IRP 에서 ETF 매매 가능. 개별 ETF 는 위험등급이 상품별로 다르며 투자성향 범위 내에서만 권유 가능.",
    },
    {
        "id": "HT-004", "kind": "field_hot_tip", "authority": "T3-FieldTip",
        "title": "ISA 만기 자금 개인형IRP 전환 마케팅",
        "tags": ["ISA만기", "전환입금", "세액공제", "마케팅포인트", "타행ISA"],
        "file": "HOTTIP_REGISTRY.md", "heading": "### HT-004.",
        "meta": {"author": "박수연", "branch": "동부산종합금융센터", "role": "팀장",
                 "written_at": "2026-01-31", "views": 727, "likes": 33},
        "excerpt": (
            "ISA 만기자금의 사용계획을 먼저 확인하고, 사용할 자금과 노후자금으로 유지할 자금을 구분해 일부 전환까지 선택지로 활용. "
            "타행 ISA 만기자금 해지 후 당행 입금 시 증빙서류 불필요(전산확인). "
            "전환금액의 10% 추가 세액공제(300만원 한도) → 최대 49.5만원 추가 환급. 입금 횟수 제한 없음(추가 가입 ISA 만기자금도 동일)."
        ),
    },
    {
        "id": "HT-045", "kind": "field_hot_tip", "authority": "T3-FieldTip",
        "title": "IRP에 입금할 수밖에 없도록 상담해 보세요",
        "tags": ["ISA만기", "전환입금", "과세비교"],
        "file": "HOTTIP_REGISTRY.md", "heading": "### HT-045.",
        "excerpt": (
            "ISA 비과세 한도 초과분은 9.9% 분리과세, IRP 로 옮겨 연금으로 받으면 3.3~5.5% 연금소득세. "
            "ISA 가입 후 3년 경과했다면 전액 해지 후 IRP 이동 가능. 해지 후 ISA 재가입 시 3년 뒤 만기 혜택 재활용 가능."
        ),
        # T3 단독 서술 수치 — 최종 화면에서 이 수치가 쓰이면 ⚠ 경고를 자동 부착
        "t3_only_claims": [r"9\.9\s*%", r"3\.3\s*[~∼-]\s*5\.5\s*%"],
    },
    {
        "id": "SCR-014", "kind": "screen", "authority": "T2+T3", "screen_no": "01-12-213",
        "title": "입금/입금예약",
        "tags": ["전환입금", "ISA만기"],
        "file": "SCREEN_REGISTRY.md", "heading": "| SCR-014 |",
        "excerpt": "입금, 입금예약, 입금명부 등록. 거래구분 'ISA 만기자금 입금' 선택 시 입금가능금액 자동 조회.",
        "purpose": "ISA 만기자금의 전환 가능금액 확인 및 IRP 입금 처리",
    },
    {
        "id": "SCR-015", "kind": "screen", "authority": "T2+T3", "screen_no": "04-10-099",
        "title": "세금우대관련조회",
        "tags": ["세액공제", "ISA만기"],
        "file": "SCREEN_REGISTRY.md", "heading": "| SCR-015 |",
        "excerpt": "저축종류 83-만기 ISA 전환으로 전환 가능액 확인, 연금납입현황 확인.",
        "purpose": "전환 가능액·연금납입현황 사전 확인",
    },
    # 검색에서 '걸러져야' 하는 항목 (상황 태그가 안 맞음) — 데모용 대조군
    {
        "id": "OK-013", "kind": "official", "authority": "T2-InternalGuide",
        "title": "연금수령 자격 요건·수령방식·최소 연금수령기간",
        "tags": ["연금수령", "55세", "연금개시"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-013.",
        "excerpt": "연금 개시 요건 만55세 + 가입 5년 …",
    },
    {
        "id": "OK-014", "kind": "official", "authority": "T2-InternalGuide",
        "title": "퇴직급여의 개인형IRP 입금·과세이연 처리 절차",
        "tags": ["퇴직금", "과세이연", "60일"],
        "file": "OFFICIAL_KNOWLEDGE.md", "heading": "### OK-014.",
        "excerpt": "퇴직급여 수령일로부터 60일 이내 IRP 입금 …",
    },
]

# 상품 레지스트리 (knowledge/PRODUCT_REGISTRY.md 형식). 운용안 카드의 '운용 후보 보기'에 들어간다.
# risk_grade: 1=매우높은 … 6=매우낮은. None = 원리금보장(등급 개념 없음).
PRODUCT_REGISTRY = [
    {"id": "PRD-004", "name": "마이다스 기본 TDF 시리즈", "type": "TDF", "risk_grade": 4, "note": "빈티지별 위험자산 비중 상이"},
    {"id": "PRD-001", "name": "KB 온국민 TDF 시리즈", "type": "TDF", "risk_grade": 3, "note": "2030 빈티지 기준 다소높은(3)"},
    {"id": "PRD-017", "name": "KB RISE 미국ETF 모아드림", "type": "ETF", "risk_grade": 2, "note": "미국 대표지수·성장테마 ETF 재간접"},
    {"id": "DEMO-ETF-1", "name": "(예시) 국내 국고채 3년 ETF", "type": "ETF", "risk_grade": 5, "note": "데모용 샘플 — 실제 라인업은 [ETF 조회 화면]에서 확인", "demo": True},
    {"id": "PRD-018", "name": "DB손해보험2 GIC 3년", "type": "정기예금·GIC", "risk_grade": None, "note": "2026-08 특별제공 3년제 4.55% (월 변동)"},
    {"id": "PRD-020", "name": "수협은행 정기예금 (당행 단독)", "type": "정기예금·GIC", "risk_grade": None, "note": "DO 편입 금리 2026-08 3.27%"},
]


def load_registry_excerpt(item: dict, max_chars: int = 420) -> tuple:
    """knowledge/<file> 에서 heading 이 시작되는 블록을 찾아 '원문 발췌' 줄만 뽑는다.
    없으면 내장 excerpt 를 쓴다. → (텍스트, 출처 라벨)"""
    path = os.path.join(KNOWLEDGE_DIR, item["file"])
    if not os.path.exists(path):
        return item["excerpt"], "내장 발췌"
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return item["excerpt"], "내장 발췌"

    start = next((i for i, ln in enumerate(lines) if ln.startswith(item["heading"])), None)
    if start is None:
        return item["excerpt"], "내장 발췌 (레지스트리에서 heading 미발견)"

    if item["kind"] == "screen":                       # 표 한 줄
        return item["excerpt"], f"knowledge/{item['file']} L{start + 1}"

    block = []
    for ln in lines[start + 1:]:
        if ln.startswith("### "):
            break
        block.append(ln)
    if item["kind"] == "official":                     # **Content** ~ **Limitation** 사이 bullet
        picked, inside = [], False
        for ln in block:
            if ln.startswith("**Content**"):
                inside = True
                continue
            if ln.startswith("**Limitation**"):
                break
            if inside and ln.startswith("- "):
                picked.append(ln[2:].strip())
    else:                                              # Hot Tip: 인용(>) 줄
        picked = [ln.lstrip("> ").strip() for ln in block if ln.startswith(">") and ln.strip("> ").strip()]
    text = " ".join(picked).replace("**", "")[:max_chars]
    if len(" ".join(picked)) > max_chars:
        text += " …"
    return (text or item["excerpt"]), f"knowledge/{item['file']} L{start + 1}"


def retrieve(kb: list, tags: list, limit: int = 9) -> list:
    """상황 태그 겹침으로 점수 매겨 상위 항목을 고른다.
    (프로토타입에서는 Case 별 knowledge_pack 을 사람이 고정하지만, 운영에서는 이 자리에
     태그/키워드/임베딩 검색이 들어간다. 여기서는 설명을 위해 가장 단순한 태그 매칭.)"""
    scored = []
    for item in kb:
        hit = sorted(set(item["tags"]) & set(tags))
        score = len(hit)
        if item["kind"] == "official":
            score += 0.5                                # 같은 점수면 공식 지식 우선
        scored.append((score, hit, item))
    scored.sort(key=lambda x: (-x[0], x[2]["id"]))
    selected = [(s, h, it) for s, h, it in scored if h][:limit]
    return scored, selected


def knowledge_block(selected: list) -> str:
    out = []
    for _, hit, it in selected:
        text, src = load_registry_excerpt(it)
        head = f"[{it['id']}] {it['title']}  (권위: {it['authority']})"
        if it["kind"] == "screen":
            head = f"[{it['id']}] 화면 [{it['screen_no']}] {it['title']}  (권위: {it['authority']})"
        out.append(f"{head}\n  원문: {text}\n  출처: {src}")
    return "\n\n".join(out)


def product_candidates(option_type: str, ctx: dict) -> list:
    """운용안 유형 + 투자성향(C1) 으로 상품 레지스트리를 필터링 — LLM 이 아니라 규칙."""
    allowed = set(ctx["constraint"]["allowed_fund_grades"])
    rows = []
    for p in PRODUCT_REGISTRY:
        if p["type"] != option_type:
            continue
        ok = p["risk_grade"] is None or p["risk_grade"] in allowed
        rows.append({**p, "eligible": ok})
    return rows


# =============================================================================
# 3. LLM — 프롬프트 (STEP 0 Pure 와 STEP 3 Agent)
# =============================================================================

PURE_SYSTEM = "당신은 퇴직연금 상담을 도와주는 AI입니다. 고객 정보를 보고 어떻게 관리하면 좋을지 답변하세요."


def pure_prompt(raw: dict) -> str:
    return f"{PURE_SYSTEM}\n\n아래 고객의 IRP를 어떻게 관리하면 좋을까요?\n\n{raw_data_block(raw)}"


AGENT_ROLE = dedent("""
당신은 KB국민은행 개인형IRP 담당 직원의 사후관리 판단을 지원하는 의사결정 지원 Agent다.
직원이 상담 직전에 읽는 Brief 를 만든다. 고객에게 직접 말하는 것이 아니라 '직원에게' 제공한다.

[원칙]
- 제공된 고객 Context 와 Knowledge 에 없는 사실·수치를 새로 만들지 않는다.
- SYSTEM DETECTED SIGNAL(채널 행동)은 고객의 의사가 아니다. '관심 가능성'으로만 다룬다.
- 투자성향(CONSTRAINT)을 벗어나는 상품군·위험등급을 제안하지 않는다.
- 수익률·환급을 보장하는 표현을 쓰지 않는다. 실적배당형 언급 시 원금손실 가능성을 전제한다.
- 권위 T3(현장 Hot Tip) 단독 사실을 화법에 쓸 때는 '확인 필요'를 전제한다.
- 상품 이름을 특정하지 않는다. 상품 후보는 시스템이 투자성향 규칙으로 별도 조회한다.
""").strip()

AGENT_WORKFLOW = dedent("""
[판단 순서 — 이 순서로 생각하고, 결론만 JSON 에 담는다]
1. Evidence        : 고객 데이터에서 확인되는 사실
2. Interpretation  : 그 사실이 지금 관리 관점에서 뜻하는 것
3. Opportunity     : 지금 다뤄야 할 이유 (시한·한도)
4. Confirmation    : 시스템만으로 확정할 수 없어 고객에게 물어야 하는 것
5. Strategy        : 확인 결과에 따라 달라지는 관리 방향 (확정 추천 아님)
""").strip()

OUTPUT_CONTRACT = dedent("""
[출력 형식] 아래 JSON 객체 하나만 출력한다. 앞뒤에 설명·코드펜스를 붙이지 않는다. 모든 값은 한국어.
{
  "analysis": {
    "findings": ["사실 1", "사실 2", "사실 3"],          // 고객의 최근 금융상황 3줄 (Evidence)
    "focus": "이번 상담에서 확인할 점 한 문장"
  },
  "why_now": "지금 연락해야 하는 제도적 이유 한 문장 (시한·한도 근거는 Knowledge 에서만)",
  "confirm_with_customer": ["확인 질문 1", "확인 질문 2", "확인 질문 3"],
  "direction": {
    "summary": "관리 방향 한 문장",
    "options": [
      {"type": "TDF", "reason": "이 유형을 후보로 두는 이유"},
      {"type": "ETF", "reason": "..."},
      {"type": "정기예금·GIC", "reason": "..."}
    ]
  },
  "talk": {
    "opener": "직원이 고객에게 전화로 시작하는 첫 마디 (구어체, 1~2문장)",
    "branches": [
      {"condition": "고객 반응 유형", "script": "그 경우 이어갈 말 (구어체)"}
    ]
  },
  "knowledge_used": ["사용한 Knowledge id"]
}
""").strip()


def agent_prompt(ctx: dict, knowledge: str) -> str:
    return "\n\n".join([
        AGENT_ROLE,
        "[고객 Context]\n" + context_block(ctx),
        "[Retrieved Knowledge — 상황 태그 " + ", ".join(ctx["tags"]) + " 로 검색됨]\n" + knowledge,
        AGENT_WORKFLOW,
        OUTPUT_CONTRACT,
    ])


# =============================================================================
# 3'. LLM 호출 — prototype/runtime.py 의 call_gemma 와 같은 방식 (표준 라이브러리, REST)
# =============================================================================

def call_gemma(prompt_text: str, timeout: int = 300) -> dict:
    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        return {"status": "CONFIG_ERROR", "error": f"{API_KEY_ENV} is not set"}
    body = {"contents": [{"parts": [{"text": prompt_text}]}]}
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"status": "HTTP_ERROR", "error": f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:800]}"}
    except Exception as e:  # URLError, timeout ...
        return {"status": "HTTP_ERROR", "error": f"{type(e).__name__}: {e}"}
    if "error" in payload:
        return {"status": "API_ERROR", "error": json.dumps(payload["error"], ensure_ascii=False)[:800]}
    cands = payload.get("candidates") or []
    parts = (cands[0].get("content") or {}).get("parts") if cands else []
    text = "".join(p.get("text", "") for p in (parts or []) if "text" in p and not p.get("thought")).strip()
    if not text:
        return {"status": "EMPTY_RESPONSE", "error": "no text part"}
    return {"status": "SUCCESS", "text": text, "usage": payload.get("usageMetadata", {})}


# --mock : API 없이 흐름을 보여주기 위한 고정 응답 (기획자가 본 화면과 동일한 내용)
MOCK_PURE = dedent("""
김서연 고객님의 IRP는 원리금보장형 비중이 높아 안정적으로 운용되고 있습니다. 44세로 은퇴까지 기간이
충분하므로 TDF나 ETF 같은 실적배당형 상품 비중을 점차 늘리는 것을 고려해 보시기 바랍니다. 또한 타행 ISA가
곧 만기되므로 해당 자금을 IRP에 추가 납입하면 세액공제 혜택을 받을 수 있습니다. 세액공제 한도는 연 900만원이며,
납입 시 최대 148.5만원까지 환급받을 수 있습니다. 고유계정대 자금도 수익률이 낮으므로 투자상품으로 전환하는
것이 좋습니다. 장기적으로 연 5~7% 수익률을 목표로 분산투자하시면 안정적인 노후 준비가 가능합니다.
""").strip()

MOCK_AGENT = {
    "analysis": {
        "findings": [
            "신한은행 ISA 약 8,000만원이 9월 7일 만기 예정입니다.",
            "당행 IRP 4,500만원은 정기예금·채권형 펀드 중심으로 운용 중입니다.",
            "최근에는 스타뱅킹에서 IRP ETF 상품을 조회했습니다.",
        ],
        "focus": "ISA 만기자금 8,000만원의 사용계획을 확인하고, 남는 자금의 IRP 전환 여부와 향후 운용방향을 함께 점검합니다.",
    },
    "why_now": "ISA 만기 후 60일 이내에만 IRP로 전환할 수 있으며, 전환금액의 10% 범위에서 최대 300만원의 추가 세액공제 한도가 적용됩니다.",
    "confirm_with_customer": [
        "가까운 시일 내 사용할 금액이 있는지",
        "남는 자금을 노후자금으로 계속 운용할 의향이 있는지",
        "예금 중심 운용 외에 투자상품도 함께 검토할 의향이 있는지",
    ],
    "direction": {
        "summary": "현재의 안정적 운용을 유지하면서, 최근 ETF 조회 이력을 고려해 일부 자금은 TDF·ETF 등으로 분산 운용하는 방향을 제안합니다.",
        "options": [
            {"type": "TDF", "reason": "은퇴까지의 운용기간을 고려한 장기 분산운용"},
            {"type": "ETF", "reason": "실제 관심이 확인되는 경우 투자성향 범위 내에서 활용"},
            {"type": "정기예금·GIC", "reason": "안정적으로 유지할 자금은 원리금보장 중심으로 운용"},
        ],
    },
    "talk": {
        "opener": "김서연 고객님, 신한은행 ISA가 이달 7일에 만기더라고요. 만기 지나면 60일 안에만 쓸 수 있는 세금 혜택이 하나 있어서, 놓치시기 전에 미리 전화드렸어요.",
        "branches": [
            {
                "condition": "당장 사용할 계획이 없는 경우",
                "script": (
                    "그러시면 IRP 전환을 꼭 한 번 보셔야 해요. 세 가지가 달라지는데요. 첫째, 전환금액의 10%, 최대 300만 원이 "
                    "세액공제 한도로 추가돼요 — 이것만으로 환급이 최대 49.5만 원이고, 고객님은 올해 기본 한도도 500만 원 남아 있어요. "
                    "둘째, ISA에서 비과세 한도 넘은 수익은 9.9% 분리과세지만, IRP로 옮겨 연금으로 받으면 3.3~5.5%로 끝나요. "
                    "셋째, 전부 옮기실 필요 없이 안 쓰실 금액만 일부 전환하셔도 됩니다. "
                    "그리고 ISA는 해지하셔도 새로 하나 더 만드시면 3년 뒤에 이 혜택을 또 쓰실 수 있어요. "
                    "만기금은 IRP에서 공제 받고, 새 ISA로 비과세 한도는 다시 쓰는 거죠."
                ),
            },
            {
                "condition": "투자상품도 함께 검토하는 경우",
                "script": "지금 IRP는 예금하고 채권형으로만 되어 있는데, 최근에 ETF도 보셨더라고요. 원금 손실 가능성은 있지만 고객님 성향 안에서 TDF나 ETF로 일부만 나눠보는 것도 같이 보여드릴게요.",
            },
            {
                "condition": "안정적인 운용을 원하는 경우",
                "script": "그럼 지금처럼 원리금보장 중심으로 가시되, 전환하시는 금액은 정기예금이나 GIC 쪽으로 넣어두시는 걸로 보시면 돼요. 세액공제는 그대로 받으시고요.",
            },
        ],
    },
    "knowledge_used": ["OK-001", "OK-008", "OK-009", "HT-004", "HT-045", "SCR-014"],
}


def run_llm(prompt: str, label: str, mock_value, mode: str) -> tuple:
    """→ (text, status). mode: live | mock | dry"""
    if mode == "dry":
        print(f"\n▶ LLM 호출 생략 (--dry-run): {label}")
        return "", "DRY_RUN"
    if mode == "mock":
        print(f"\n▶ LLM 호출 (mock): {label}  → 고정 응답 사용")
        text = mock_value if isinstance(mock_value, str) else json.dumps(mock_value, ensure_ascii=False, indent=2)
        return text, "MOCK"
    t0 = time.time()
    print(f"\n▶ LLM 호출: {label} ({MODEL_ID})", end="", flush=True)
    r = call_gemma(prompt)
    if r["status"] != "SUCCESS":
        print(f"\n[호출 실패] {r['status']}: {r.get('error')}")
        return "", r["status"]
    print(f"  → 완료 ({time.time() - t0:.1f}초, {len(r['text']):,}자, usage={r.get('usage', {})})")
    return r["text"], "SUCCESS"


# =============================================================================
# 4. 후처리 / 검증 — LLM 결과를 그대로 화면에 내보내지 않는다
# =============================================================================

REQUIRED_KEYS = ["analysis", "why_now", "confirm_with_customer", "direction", "talk", "knowledge_used"]
BANNED_PHRASES = ["무조건", "확실히 수익", "수익을 보장", "보장됩니다", "손해 볼 일 없", "원금이 보장되는 실적배당"]


def parse_json(text: str) -> tuple:
    """코드펜스 제거 → json.loads. 실패 시 첫 '{' ~ 마지막 '}' 로 재시도."""
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    try:
        return json.loads(t), []
    except json.JSONDecodeError as e:
        i, j = t.find("{"), t.rfind("}")
        if i >= 0 and j > i:
            try:
                return json.loads(t[i:j + 1]), [f"JSON 정규화 적용 ({e.msg})"]
            except json.JSONDecodeError as e2:
                return None, [f"JSON 파싱 실패: {e2}"]
        return None, [f"JSON 파싱 실패: {e}"]


def all_text(obj) -> str:
    if isinstance(obj, dict):
        return " ".join(all_text(v) for v in obj.values())
    if isinstance(obj, list):
        return " ".join(all_text(v) for v in obj)
    return str(obj)


def validate(out: dict, ctx: dict, selected: list) -> dict:
    issues, cautions = [], []

    # (1) 스키마
    for k in REQUIRED_KEYS:
        if k not in out:
            issues.append(f"필수 키 누락: {k}")
    if len((out.get("analysis") or {}).get("findings", [])) != 3:
        issues.append("analysis.findings 는 3개여야 함")

    text = all_text(out)

    # (2) 금지 표현
    for p in BANNED_PHRASES:
        if p in text:
            issues.append(f"금지 표현: '{p}'")

    # (3) C1 — 투자성향 밖 위험등급 언급
    allowed = set(ctx["constraint"]["allowed_fund_grades"])
    for g, label in GRADE_LABEL.items():
        if g not in allowed and label in text:
            issues.append(f"C1 위반 가능: 투자성향 밖 등급 '{label}' 언급")

    # (4) Signal 을 의사로 단정했는지 (간단 휴리스틱)
    if re.search(r"ETF[^.。]{0,12}(원하|희망|하고 싶)", text):
        issues.append("Signal 단정 의심: ETF 조회를 고객 의사로 표현")

    # (5) knowledge_used 가 실제 검색된 id 인지 (환각 id 방지)
    known = {it["id"] for _, _, it in selected}
    for kid in out.get("knowledge_used", []):
        if kid not in known:
            issues.append(f"검색되지 않은 Knowledge id 인용: {kid}")

    # (6) T3 단독 사실이 화법에 쓰였으면 ⚠ 경고 자동 부착 (LLM 이 아니라 규칙이 붙인다)
    talk_text = all_text(out.get("talk", {}))
    t3_hits = []
    for _, _, it in selected:
        for pat in it.get("t3_only_claims", []):
            m = re.search(pat, talk_text)
            if m:
                t3_hits.append(m.group(0).replace(" ", ""))
    if t3_hits:
        cautions.append(f"{'·'.join(t3_hits)} 세율은 현장 팁 출처 — 안내 전 공식 기준 확인.")

    # (7) 전환을 권하면 반드시 붙는 고지 (OK-009 must_disclose)
    if "전환" in talk_text:
        for _, _, it in selected:
            if it.get("must_disclose"):
                cautions.append(it["must_disclose"] + ".")

    return {"issues": issues, "cautions": cautions}


def assemble_screen(out: dict, raw: dict, ctx: dict, selected: list, checks: dict) -> dict:
    """LLM JSON + 결정론 조회 결과를 화면 모델로 합친다."""
    by_id = {it["id"]: it for _, _, it in selected}

    # Hot Tip 카드: LLM 이 인용한 field_hot_tip 중 첫 항목의 레지스트리 메타를 그대로
    tip = next((by_id[k] for k in out.get("knowledge_used", []) if by_id.get(k, {}).get("kind") == "field_hot_tip" and by_id[k].get("meta")), None)

    # 실행 화면: OK-001 의 처리 위치 → SCR 항목
    screen = None
    for _, _, it in selected:
        if it["kind"] == "screen" and it["screen_no"] == "01-12-213":
            screen = it
            break

    options = []
    for op in out["direction"]["options"]:
        options.append({**op, "candidates": product_candidates(op["type"], ctx)})

    return {
        "header": {
            "name": raw["customer"]["name"], "id": raw["customer"]["id"],
            "event": f"타행 ISA 만기 D-{ctx['event']['dday']}",
            "signal": "ETF 조회" if ctx["signal"]["etf_views"] else "",
            "time": f"오전 {raw['analysis']['time']} 분석",
        },
        "customer": ctx["snapshot"],
        "raw": raw,
        "analysis_date": raw["analysis"]["date"].replace("-", "."),
        "llm": out,
        "options": options,
        "cautions": checks["cautions"],
        "tip": tip,
        "screen": screen,
    }


# =============================================================================
# 5. 렌더 — 기획자가 본 화면 (블록마다 출처 표시)
# =============================================================================

def render(screen: dict) -> str:
    h, s, raw, llm = screen["header"], screen["customer"], screen["raw"], screen["llm"]
    c, irp = raw["customer"], raw["irp"]
    L = []
    P = L.append

    P(f"┌ {h['name']} 고객님 [ {h['id']} ]                                  [DATA]")
    P(f"│ {h['event']}  ·  {h['signal']}  ·  {h['time']}")
    P("└" + "─" * 60)
    P("고객 정보                                                          [DATA]")
    P(f"  나이·성별 {c['age']}세 · {c['gender']}   스타클럽 {c['grade']}   투자성향 {c['risk_profile']}")
    P(f"  IRP 계좌 신규일 {irp['open_date'].replace('-', '.')}   디폴트옵션 등록 · {s['default_option']}")
    P("IRP 계좌현황                                                       [DATA]")
    P(f"  평가금액 {won(s['irp_total'])}")
    for k, (amt, pct) in s["mix"].items():
        P(f"    {k:<7} {won(amt):>9}  {pct:>2}%")
    P(f"  수익률 ({s['return_1y']*100:+.1f}%)   세액공제 잔여한도 ({won(s['tax_credit_remaining'])})")
    P(f"  최근 상품 신규일 {irp['last_product_date'].replace('-', '.')}   운용 현황 자세히 · 보유상품 {s['holdings_count']}건")
    P("")
    P(f"✦ AI 분석   {screen['analysis_date']} 기준 분석                                [LLM]")
    P(f"  {c['name']} 고객님의 최근 금융상황을 분석했습니다.")
    for i, f in enumerate(llm["analysis"]["findings"], 1):
        P(f"  {i}  {f}")
    P("  이번 상담에서 확인할 점")
    P(f"    {llm['analysis']['focus']}")
    P("  💡 왜 지금?                                                       [LLM ← KB OK-001]")
    P(f"    {llm['why_now']}")
    P("  고객과 확인                                                        [LLM]")
    for q in llm["confirm_with_customer"]:
        P(f"    · {q}")
    P("")
    P("관리 방향 및 제안                                                   [LLM]")
    P(f"  {llm['direction']['summary']}")
    for op in screen["options"]:
        P(f"  ▸ {op['type']} — {op['reason']}")
        P(f"      운용 후보 보기 ({c['risk_profile']} · C1 필터)                     [RULE ← 상품 레지스트리]")
        for p in op["candidates"]:
            grade = f"{p['risk_grade']}등급 {GRADE_LABEL[p['risk_grade']]}" if p["risk_grade"] else "원리금보장"
            mark = "✓" if p["eligible"] else "✗ 성향 초과"
            P(f"        {mark:<8} {p['name']} [{p['id']}] · {grade} · {p['note']}")
    P("  ※ 각 운용안을 선택하면 고객의 투자성향에 적합한 구체적인 상품 후보와 위험등급·수익률·금리 등 상세정보를 확인할 수 있습니다.")
    P("")
    P("상담 Point                                                          [LLM]")
    P("  💬 이렇게 시작해보세요")
    P(f"    “{llm['talk']['opener']}”")
    P("  고객 반응에 따라")
    for b in llm["talk"]["branches"]:
        P(f"    ▾ {b['condition']}")
        P(f"      “{b['script']}”")
    for ctn in screen["cautions"]:
        P(f"  ⚠ {ctn}                                   [RULE ← 권위등급·고지 규칙]")
    P("")
    P("TIP & 실행")
    tip = screen["tip"]
    if tip:
        m = tip["meta"]
        P(f"  📌 현장 TIP  {tip['title']}                                    [KB {tip['id']}]")
        P(f"     {tip['excerpt'].split('. ')[0]}.")
        P(f"     {m['branch']} {m['author']} {m['role']} · {m['written_at'].replace('-', '.')}   조회 {m['views']} · 좋아요 {m['likes']}   바로가기")
    sc = screen["screen"]
    if sc:
        P(f"  ↗ 실행 화면  {sc['screen_no']}                                           [KB {sc['id']} ← OK-001 처리위치]")
        P(f"     {sc['title']} — {sc['purpose']}    화면 열기 →")
    return "\n".join(L)


# =============================================================================
# 데모 실행
# =============================================================================

def main() -> None:
    args = set(sys.argv[1:])
    dry_run = "--dry-run" in args
    show_prompts = "--show-prompt" in args
    skip_pure = "--skip-pure" in args
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]

    if dry_run:
        mode = "dry"
    elif "--mock" in args:
        mode = "mock"
    elif os.environ.get(API_KEY_ENV, "").strip():
        mode = "live"
    else:
        mode = "mock"
        print(f"※ {API_KEY_ENV} 가 없어 --mock 모드로 진행합니다 (LLM 응답은 고정값, 나머지 단계는 실제 실행).")

    record = {"mode": mode, "model": MODEL_ID, "started_at": datetime.now().isoformat(timespec="seconds")}

    banner("DATA → LLM 추론 → 최종 화면 : 김서연(타행 ISA 만기 D-3) 화면은 어떻게 만들어지는가")
    print(f"MODE   : {mode}    MODEL: {MODEL_ID}")
    print(f"KB DIR : {KNOWLEDGE_DIR} ({'있음 — 원문 발췌를 파일에서 읽음' if os.path.isdir(KNOWLEDGE_DIR) else '없음 — 내장 발췌 사용'})")

    # ------------------------------------------------------------------ STEP 0
    if not skip_pure:
        banner("STEP 0. PURE LLM — 고객 Raw Data 만 주고 물어본다")
        prompt0 = pure_prompt(RAW_DATA)
        if show_prompts or dry_run:
            section("[PROMPT]"); print(prompt0)
        text0, st0 = run_llm(prompt0, "Pure LLM", MOCK_PURE, mode)
        section("[OUTPUT]"); print(text0 or "(출력 없음)")
        record["step0_pure"] = {"status": st0, "output": text0}
        explain(
            "아무것도 안 붙임 — 데이터만 던짐",
            "그럴듯하지만 (1) 60일·300만 같은 제도 근거가 없거나 틀리고 (2) 성향 확인 없이 상품을 권하고 "
            "(3) 'ETF 조회'를 관심으로 단정하고 (4) 수익률을 약속한다. 화면에 넣을 형태도 아니다.",
        )

    # ------------------------------------------------------------------ STEP 1
    banner("STEP 1. DATA → CONTEXT  (결정론 · LLM 없음)")
    section("[원천 데이터]"); print(raw_data_block(RAW_DATA))
    ctx = build_context(RAW_DATA)
    section("[Context]"); print(context_block(ctx))
    section("[검색용 상황 태그]"); print(", ".join(ctx["tags"]))
    record["step1_context"] = ctx
    explain(
        "Snapshot / Event / Signal / Constraint 로 구조화. D-3·60일 종료일·추가공제 300만·비중 62/33/4% 는 코드가 계산",
        "숫자 계산과 시한은 LLM 에 맡기지 않는다. 화면 상단 '고객 정보 / IRP 계좌현황' 블록은 이 단계에서 이미 완성된다.",
    )

    # ------------------------------------------------------------------ STEP 2
    banner("STEP 2. KNOWLEDGE 검색  (결정론 · LLM 없음)")
    scored, selected = retrieve(KNOWLEDGE_BASE, ctx["tags"])
    section("[검색 결과 — 상황 태그 겹침 점수]")
    print(f"{'id':<8} {'권위':<18} {'점수':>4}  선택  일치 태그 / 제목")
    sel_ids = {it["id"] for _, _, it in selected}
    for score, hit, it in scored:
        mark = "✓" if it["id"] in sel_ids else "-"
        print(f"{it['id']:<8} {it['authority']:<18} {score:>4}   {mark}   {', '.join(hit) or '(없음)'}  |  {it['title']}")
    knowledge = knowledge_block(selected)
    section("[LLM 에 전달되는 Knowledge 블록]"); print(knowledge)
    record["step2_knowledge"] = {"selected": [it["id"] for _, _, it in selected]}
    explain(
        "상황 태그로 레지스트리를 검색해 공식 제도(T2) + 현장 Hot Tip(T3) + 화면 + 처리위치를 권위등급과 함께 선별",
        "모델을 학습시키지 않는다. '왜 지금?'의 60일·300만은 OK-001 원문에서, 현장 TIP 카드는 HT-004 메타에서 온다. "
        "연금수령(OK-013)·퇴직금 과세이연(OK-014)처럼 태그가 안 맞는 지식은 걸러진다.",
    )

    # ------------------------------------------------------------------ STEP 3
    banner("STEP 3. LLM 추론  (Gemma 4 · 1회 호출)")
    prompt3 = agent_prompt(ctx, knowledge)
    if show_prompts or dry_run:
        section("[PROMPT — 실제 전달 전문]"); print(prompt3)
    else:
        section("[PROMPT 구성]")
        print("Role/원칙  +  고객 Context  +  Retrieved Knowledge  +  Workflow(5단계)  +  Output Contract(JSON)")
        print(f"(총 {len(prompt3):,}자 — --show-prompt 로 전문 확인)")
    text3, st3 = run_llm(prompt3, "Agent 판단 → JSON", MOCK_AGENT, mode)
    section("[RAW OUTPUT]"); print(text3 or "(출력 없음)")
    record["step3_llm"] = {"status": st3, "prompt_chars": len(prompt3), "raw_output": text3}
    explain(
        "역할·원칙 + Context + Knowledge + 판단 순서 + 출력 계약을 한 프롬프트로. 화면 섹션과 1:1 인 JSON 만 받음",
        "LLM 이 하는 일은 '해석·확인질문·방향·화법 문장 만들기'로 좁혀진다. 제도 수치는 Knowledge 에서만 가져오게 하고, "
        "상품명은 못 쓰게 한다(상품은 규칙이 조회).",
    )

    if dry_run or not text3:
        banner("종료 (LLM 출력이 없어 STEP 4~5 생략)")
        return

    # ------------------------------------------------------------------ STEP 4
    banner("STEP 4. 후처리 / 검증  (결정론 · LLM 없음)")
    out, norm = parse_json(text3)
    section("[JSON 파싱]")
    print("✓ 파싱 성공" + (f" ({'; '.join(norm)})" if norm else "") if out else f"✗ {norm}")
    if not out:
        return
    checks = validate(out, ctx, selected)
    section("[검증 결과]")
    if checks["issues"]:
        print("⚠ 검토 필요")
        for x in checks["issues"]:
            print(f"  - {x}")
    else:
        print("✓ 스키마 · 금지표현 · C1(투자성향) · Signal 단정 · Knowledge id 검사 통과")
    section("[규칙이 자동으로 붙인 고지]")
    for x in checks["cautions"] or ["(없음)"]:
        print(f"  ⚠ {x}")
    section("[레지스트리 조회로 채우는 블록]")
    for op in out["direction"]["options"]:
        cands = product_candidates(op["type"], ctx)
        ok = [p["name"] for p in cands if p["eligible"]]
        ng = [p["name"] for p in cands if not p["eligible"]]
        print(f"  {op['type']:<8} 후보 {len(ok)}건 적합 / {len(ng)}건 성향 초과 제외 → {', '.join(ok) or '-'}")
    print("  현장 TIP 카드 ← HT-004 (author/written_at/views/likes)   실행 화면 ← OK-001 처리위치 → SCR-014 [01-12-213]")
    screen = assemble_screen(out, RAW_DATA, ctx, selected, checks)
    record["step4_validation"] = checks
    explain(
        "JSON 스키마·금지표현·투자성향(C1)·환각 id 검사 → T3 단독 수치(9.9%·3.3~5.5%)에 ⚠ 자동 부착 → 상품·화면·Tip 은 조회로 결합",
        "화면의 ⚠ 경고문, '운용 후보 보기' 상품 목록, TIP 카드의 조회수·작성자, 실행 화면번호는 전부 LLM 이 쓴 게 아니라 "
        "규칙과 레지스트리에서 온다. LLM 이 틀려도 여기서 걸린다.",
    )

    # ------------------------------------------------------------------ STEP 5
    banner("STEP 5. 최종 화면  (직원용 Brief)")
    print(render(screen))
    section("[출처 범례]")
    print("  [DATA] 계정계·CRM 값 그대로   [RULE] 코드가 계산·검증·조회   [KB] 지식베이스 레지스트리 항목   [LLM] 모델이 생성한 문장")

    banner("DEMO SUMMARY")
    print(dedent("""
        원천 데이터 (계좌 · 타행 ISA · 채널 로그)
          ↓ 결정론   D-3 · 60일 시한 · 300만 상한 · 비중 % · 투자성향 한도 계산        → 화면 상단 고객/계좌 블록
        Context + 상황 태그
          ↓ 검색     지식베이스(OK/HT/SCR/PRD)에서 태그 매칭 · 권위등급 부착          → '왜 지금?' 근거 · TIP · 화면번호
        Role + Context + Knowledge + Workflow + Output Contract
          ↓ LLM 1회  해석 · 확인질문 · 관리방향 · 화법을 화면 섹션 JSON 으로            → AI 분석 · 관리 방향 · 상담 Point
          ↓ 검증     스키마 · 금지표현 · C1 · T3 단독수치 ⚠ · 상품 후보 C1 필터        → ⚠ 고지 · 운용 후보 보기
        직원 화면

        → LLM 은 전체 화면의 '문장' 부분만 만든다. 숫자·시한·근거·상품·화면번호·경고는 데이터와 규칙이 만든다.
    """).strip())

    if out_path:
        record["screen"] = {k: v for k, v in screen.items() if k != "raw"}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n실행 기록 저장: {out_path}")


if __name__ == "__main__":
    main()
