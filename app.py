import streamlit as st
import itertools
import json
from math import factorial, comb, perm
import os

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Discrete Structures: The Architecture of Logic",
    page_icon="∀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #050505; color: #e8eaf0; }

/* ── Kill all Streamlit chrome ─────────────────────────── */
header[data-testid="stHeader"],
header[data-testid="stHeader"] > *,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu,
footer { display: none !important; height: 0 !important; }

/* ── Hide native sidebar entirely ─────────────────────── */
section[data-testid="stSidebar"],
button[data-testid="collapsedControl"],
div[data-testid="collapsedControl"] { display: none !important; }

/* push content — leave room for the hamburger button */
.main .block-container {
  padding-top: 1.5rem !important;
  padding-left: 4rem !important;
  padding-right: 2rem !important;
  max-width: 1200px !important;
}

/* ── Hamburger label ──────────────────────────────────── */
#_nav_chk { display: none; }
#_nav_btn {
  position: fixed; top: 16px; left: 16px; z-index: 9999;
  width: 40px; height: 40px;
  background: #07070f;
  border: 1px solid #2a2d4a;
  border-radius: 6px;
  cursor: pointer;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 5px;
  transition: border-color 0.2s, background 0.2s;
}
#_nav_btn:hover { background: #0d0d1a; border-color: #4ECCA3; }
#_nav_btn span {
  display: block; width: 18px; height: 2px;
  background: #4ECCA3; border-radius: 2px;
  transition: transform 0.25s, opacity 0.2s;
  pointer-events: none;
}
#_nav_chk:checked ~ #_nav_btn span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
#_nav_chk:checked ~ #_nav_btn span:nth-child(2) { opacity: 0; }
#_nav_chk:checked ~ #_nav_btn span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* ── Overlay backdrop ─────────────────────────────────── */
#_nav_bd {
  display: none; position: fixed; inset: 0; z-index: 9000;
  background: rgba(0,0,0,0.55);
}
#_nav_chk:checked ~ #_nav_bd { display: block; }

/* ── Slide-in panel ──────────────────────────────────────  */
#_nav_panel {
  position: fixed; top: 0; left: 0; height: 100vh; width: 290px;
  background: #07070f; border-right: 1px solid #131526;
  z-index: 9100; overflow-y: auto;
  transform: translateX(-100%);
  transition: transform 0.28s cubic-bezier(.4,0,.2,1);
}
#_nav_chk:checked ~ #_nav_panel { transform: translateX(0); }

/* ── Sidebar header ──────────────────────────────────── */
.sb-head {
  padding: 1.2rem 1.2rem 1rem;
  border-bottom: 1px solid #131526;
}
.sb-wordmark {
  font-family: 'JetBrains Mono', monospace; font-size: 0.56rem;
  letter-spacing: 0.22em; color: #333a52; text-transform: uppercase;
  margin-bottom: 0.28rem;
}
.sb-brand {
  font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
  font-weight: 700; color: #4ECCA3; letter-spacing: 0.04em;
}
.sb-brand span { color: #2a3040; font-weight: 300; }
.sb-section {
  font-family: 'JetBrains Mono', monospace; font-size: 0.56rem;
  letter-spacing: 0.22em; color: #2a3040; text-transform: uppercase;
  padding: 1rem 1.2rem 0.4rem;
}
.sb-list { padding: 0 0.5rem 2rem; }

/* Nav items */
a.sb-item {
  display: flex !important; align-items: center !important;
  gap: 0.75rem !important; padding: 0.65rem 0.8rem !important;
  text-decoration: none !important; border-radius: 6px !important;
  border: 1px solid transparent !important; margin-bottom: 1px !important;
  transition: background 0.15s, border-color 0.15s !important;
  color: inherit !important;
}
a.sb-item:hover { background: rgba(78,204,163,0.05) !important; }
a.sb-item.sb-active {
  background: rgba(78,204,163,0.09) !important;
  border-color: rgba(78,204,163,0.18) !important;
}
.sb-icon {
  font-size: 0.95rem; width: 20px; text-align: center;
  flex-shrink: 0; color: #2e3448; line-height: 1;
}
a.sb-item.sb-active .sb-icon { color: #4ECCA3 !important; }
.sb-text { flex: 1; min-width: 0; }
a.sb-item .sb-label {
  font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important;
  font-weight: 600 !important; color: #5a6478 !important;
  display: block !important; white-space: nowrap !important;
  overflow: hidden !important; text-overflow: ellipsis !important;
  line-height: 1.3 !important;
}
a.sb-item.sb-active .sb-label { color: #e8eaf0 !important; }
a.sb-item:hover .sb-label { color: #b8c4d4 !important; }
a.sb-item .sb-sub {
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.58rem !important;
  color: #2e3448 !important; display: block !important;
  white-space: nowrap !important; overflow: hidden !important;
  text-overflow: ellipsis !important; margin-top: 0.1rem !important;
}
a.sb-item.sb-active .sb-sub { color: #3d6060 !important; }
a.sb-item:hover .sb-sub { color: #3d4a5a !important; }
a.sb-item .sb-badge {
  font-family: 'JetBrains Mono', monospace; font-size: 0.55rem;
  color: #2e3448; background: rgba(20,22,40,0.9);
  border: 1px solid #1a1d30; border-radius: 3px;
  padding: 0.08rem 0.38rem; flex-shrink: 0; line-height: 1.7;
}
a.sb-item.sb-active .sb-badge {
  color: #4ECCA3 !important;
  background: rgba(78,204,163,0.08) !important;
  border-color: rgba(78,204,163,0.22) !important;
}

/* Headers */
h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; color: #e8eaf0; }
.hero-title { font-size: 2.6rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; }
.hero-title em { color: #4ECCA3; font-style: normal; }
.cyan { color: #4ECCA3; }
.mono { font-family: 'JetBrains Mono', monospace; }

/* Cards */
.card {
  background: rgba(27,27,47,0.7);
  border: 1px solid #2a2d4a;
  border-radius: 4px;
  padding: 1.4rem;
  margin-bottom: 1rem;
  position: relative;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 3px; height: 100%;
  background: #4ECCA3;
  border-radius: 4px 0 0 4px;
}

/* Formula box */
.formula {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  background: rgba(78,204,163,0.08);
  border: 1px solid #2a8a6b;
  padding: 0.4rem 0.8rem;
  color: #4ECCA3;
  border-radius: 2px;
  margin: 0.6rem 0;
  display: inline-block;
}

/* Result box */
.result-box {
  background: #0a0a14;
  border: 1px solid #2a2d4a;
  border-radius: 4px;
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  color: #b8c4d4;
  margin-top: 0.8rem;
  white-space: pre-wrap;
  max-height: 400px;
  overflow-y: auto;
}
.result-box .highlight { color: #4ECCA3; font-weight: 600; }
.result-box .err { color: #ff6b6b; }

/* Team cards */
.team-grid { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1.5rem 0; }
.team-card {
  background: rgba(27,27,47,0.7);
  border: 1px solid #2a2d4a;
  padding: 0.9rem 1.2rem;
  min-width: 180px;
  border-left: 3px solid #4ECCA3;
  border-radius: 2px;
}
.team-id { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #4ECCA3; }
.team-name { font-size: 0.9rem; font-weight: 500; color: #e8eaf0; margin-top: 0.2rem; }
.team-num { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8892a4; }

/* ── Input & Form Fields ────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextInput input, .stNumberInput input,
input[type="text"], input[type="number"] {
  background: #0d0d22 !important; color: #e8eaf0 !important;
  border: 1px solid #2a2d4a !important; border-radius: 3px !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important; caret-color: #4ECCA3 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
input[type="text"]:focus, input[type="number"]:focus {
  border-color: #4ECCA3 !important; box-shadow: 0 0 0 2px rgba(78,204,163,0.12) !important;
  outline: none !important;
}
textarea {
  background: #0d0d22 !important; color: #e8eaf0 !important;
  border: 1px solid #2a2d4a !important; border-radius: 3px !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important; caret-color: #4ECCA3 !important;
  line-height: 1.7 !important;
}
textarea:focus {
  border-color: #4ECCA3 !important; box-shadow: 0 0 0 2px rgba(78,204,163,0.12) !important;
  outline: none !important;
}
input::placeholder, textarea::placeholder { color: #4a5568 !important; }

/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
  background: #0d0d22 !important; border: 1px solid #2a2d4a !important;
  color: #e8eaf0 !important; border-radius: 3px !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: #4ECCA3 !important; box-shadow: 0 0 0 2px rgba(78,204,163,0.12) !important;
}

/* Password input */
div[data-testid="stTextInput"] input[type="password"] {
  background: #0d0d22 !important; border: 1px solid #2a2d4a !important;
  color: #e8eaf0 !important; border-radius: 3px !important; caret-color: #4ECCA3 !important;
}

/* Tabs */
div[data-testid="stTabs"] button[role="tab"] {
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important;
  letter-spacing: 0.06em !important; color: #8892a4 !important;
  border-bottom: 2px solid transparent !important; transition: all 0.2s !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color: #4ECCA3 !important; border-bottom-color: #4ECCA3 !important;
  background: transparent !important;
}
div[data-testid="stTabs"] button[role="tab"]:hover { color: #4ECCA3 !important; }

/* Buttons */
.stButton > button {
  font-family: 'JetBrains Mono', monospace;
  background: #4ECCA3;
  color: #050505;
  border: none;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 0.5rem 1.4rem;
  border-radius: 2px;
  transition: background 0.2s;
}
.stButton > button:hover { background: #3db88f; }

/* Tab styling */
div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

/* Truth table */
.tt { border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; width: 100%; margin-top: 0.6rem; }
.tt th { color: #4ECCA3; text-align: center; padding: 0.4rem 0.7rem; border-bottom: 1px solid #2a2d4a; }
.tt td { text-align: center; padding: 0.3rem 0.7rem; border-bottom: 1px solid rgba(30,32,53,0.5); }
.tt .T { color: #4ECCA3; font-weight: 600; }
.tt .F { color: #ff6b6b; }

/* Divider */
.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #2a2d4a 30%, #2a8a6b 50%, #2a2d4a 70%, transparent);
  margin: 2rem 0;
}

/* Section tag */
.sec-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #4ECCA3;
  letter-spacing: 0.15em;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #4ECCA3;
  border: 1px solid #2a8a6b;
  padding: 0.2rem 0.8rem;
  border-radius: 2px;
  background: rgba(78,204,163,0.05);
  display: inline-block;
  margin-bottom: 1.2rem;
  letter-spacing: 0.15em;
}

/* ── Study Hub ──────────────────────────────────────────── */
.sh-stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin: 1.2rem 0; }
.sh-stat {
  background: rgba(27,27,47,0.7); border: 1px solid #2a2d4a;
  border-radius: 6px; padding: 1.2rem; text-align: center;
}
.sh-stat-val {
  font-family: 'JetBrains Mono', monospace; font-size: 1.8rem;
  font-weight: 700; color: #4ECCA3; line-height: 1;
}
.sh-stat-lbl { font-size: 0.75rem; color: #8892a4; margin-top: 0.4rem; }
.sh-bar-wrap { background: rgba(42,45,74,0.5); border-radius: 4px; height: 6px; margin: 0.3rem 0 0; overflow: hidden; }
.sh-bar-fill { height: 100%; background: linear-gradient(90deg,#2a8a6b,#4ECCA3); border-radius: 4px; transition: width 0.4s; }
.sh-topic-row {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.75rem 1rem; border: 1px solid #2a2d4a;
  border-left: 3px solid #4ECCA3; border-radius: 4px;
  background: rgba(27,27,47,0.5); margin-bottom: 0.5rem;
}
.sh-topic-name { flex: 1; font-size: 0.88rem; font-weight: 600; color: #e8eaf0; }
.sh-topic-pills { display: flex; gap: 0.4rem; }
.sh-pill {
  font-family: 'JetBrains Mono', monospace; font-size: 0.58rem;
  padding: 0.18rem 0.55rem; border-radius: 3px; border: 1px solid;
  letter-spacing: 0.05em;
}
.sh-pill.done { color: #4ECCA3; border-color: rgba(78,204,163,0.4); background: rgba(78,204,163,0.08); }
.sh-pill.todo { color: #2e3448; border-color: #1a1d30; background: rgba(20,22,40,0.6); }
.sh-ach-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 0.6rem 0 1.5rem; }
.sh-ach {
  font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  padding: 0.3rem 0.9rem; border-radius: 20px; border: 1px solid;
  display: flex; align-items: center; gap: 0.4rem;
}
.sh-ach.earned { color: #4ECCA3; border-color: rgba(78,204,163,0.4); background: rgba(78,204,163,0.08); }
.sh-ach.locked { color: #2e3448; border-color: #1a1d30; background: rgba(15,16,28,0.8); }
.sh-road-group { margin-bottom: 2rem; }
.sh-road-label {
  font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
  letter-spacing: 0.2em; color: #4ECCA3; text-align: center;
  margin-bottom: 0.8rem; opacity: 0.7;
}
.sh-road-row { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
.sh-road-node {
  background: rgba(27,27,47,0.8); border: 1px solid #2a2d4a;
  border-radius: 8px; padding: 1rem 1.2rem; width: 200px;
  text-align: center; position: relative;
}
.sh-road-node:hover { border-color: rgba(78,204,163,0.3); }
.sh-road-icon { font-size: 1.2rem; margin-bottom: 0.4rem; color: #4ECCA3; }
.sh-road-name { font-size: 0.85rem; font-weight: 700; color: #e8eaf0; }
.sh-road-week { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #2e3448; margin-top: 0.2rem; }
.sh-road-prog { margin-top: 0.6rem; }
.sh-arrow { text-align: center; color: #2e3448; font-size: 1.2rem; margin: 0.4rem 0; }
.sh-concept-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin: 1rem 0; }
.sh-concept-card {
  background: rgba(13,13,34,0.7); border: 1px solid #2a2d4a;
  border-left: 3px solid #4ECCA3; border-radius: 4px; padding: 0.8rem 1rem;
}
.sh-concept-title { font-size: 0.75rem; font-weight: 700; color: #4ECCA3; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 0.08em; }
.sh-concept-body { font-size: 0.82rem; color: #b8c4d4; }
.sh-quiz-q { background: rgba(27,27,47,0.7); border: 1px solid #2a2d4a; border-radius: 6px; padding: 1rem 1.2rem; margin-bottom: 1rem; }
.sh-quiz-num { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #4ECCA3; margin-bottom: 0.4rem; }
.sh-quiz-text { font-size: 0.88rem; color: #e8eaf0; font-weight: 500; }
.sh-practice-card { background: rgba(27,27,47,0.5); border: 1px solid #2a2d4a; border-radius: 6px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
.sh-practice-q { font-size: 0.88rem; color: #e8eaf0; font-weight: 500; margin-bottom: 0.5rem; }
.sh-practice-sol { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #4ECCA3; background: rgba(78,204,163,0.06); border: 1px solid rgba(78,204,163,0.15); border-radius: 4px; padding: 0.6rem 0.8rem; margin-top: 0.4rem; }
.sh-overview { border-left: 3px solid #4ECCA3; background: rgba(13,13,34,0.7); border-radius: 4px; padding: 0.9rem 1.1rem; margin-bottom: 1.2rem; }
.sh-overview-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em; color: #4ECCA3; margin-bottom: 0.3rem; }
.sh-overview-text { font-size: 0.88rem; color: #b8c4d4; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def parse_set(s: str) -> list:
    return list(dict.fromkeys([x.strip() for x in s.split(",") if x.strip()]))

def fmt_set(lst: list) -> str:
    return "{" + ", ".join(str(x) for x in lst) + "}" if lst else "∅"

def eval_proposition(expr: str, vals: dict) -> bool | None:
    """Safely evaluate a propositional logic expression."""
    try:
        safe = expr.strip()
        safe = safe.replace("<->", " __bic__ ").replace("->", " __imp__ ")
        safe = safe.replace("XOR", " __xor__ ").replace("xor", " __xor__ ")
        for var, val in vals.items():
            safe = safe.replace(var, "True" if val else "False")
        # Operators
        safe = safe.replace("&&", " and ").replace("||", " or ").replace("!", " not ")
        # Handle custom operators with simple sequential replacement
        # __imp__: a -> b  ==  (not a) or b
        # We build a small evaluator
        def replace_custom(s):
            # biconditional
            while "__bic__" in s:
                idx = s.index("__bic__")
                # find left operand (last True/False before idx)
                left_part = s[:idx].rstrip()
                right_part = s[idx+7:].lstrip()
                # wrap in (left == right)
                # find balanced tokens - simple approach: split at __bic__
                s = "(" + left_part + ") == (" + right_part + ")"
                break
            while "__imp__" in s:
                idx = s.index("__imp__")
                left_part = s[:idx].rstrip()
                right_part = s[idx+7:].lstrip()
                s = "(not (" + left_part + ") or (" + right_part + "))"
                break
            while "__xor__" in s:
                idx = s.index("__xor__")
                left_part = s[:idx].rstrip()
                right_part = s[idx+7:].lstrip()
                s = "(" + left_part + ") != (" + right_part + ")"
                break
            return s
        safe = replace_custom(safe)
        # Disallow anything dangerous
        allowed = {"True", "False", "and", "or", "not", "(", ")", "!", "=", "<", ">", " "}
        import re
        if re.search(r'(__import__|exec|eval|open|os|sys|subprocess)', safe):
            return None
        return bool(eval(safe))  # noqa: S307 – restricted above
    except Exception:
        return None

def gen_truth_table(expr: str):
    """Return HTML truth table for expression."""
    import re
    vars_found = sorted(set(re.findall(r'\b([a-z])\b', expr)))
    if not vars_found:
        return "<span class='err'>// ERROR: no single-letter variables found</span>", []
    if len(vars_found) > 5:
        return "<span class='err'>// ERROR: max 5 variables</span>", []
    rows_data = []
    html = "<table class='tt'><thead><tr>"
    for v in vars_found:
        html += f"<th>{v}</th>"
    html += "<th>Result</th></tr></thead><tbody>"
    n = len(vars_found)
    for i in range(1 << n):
        vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(vars_found)}
        res = eval_proposition(expr, vals)
        html += "<tr>"
        for v in vars_found:
            cl = "T" if vals[v] else "F"
            html += f"<td class='{cl}'>{'T' if vals[v] else 'F'}</td>"
        if res is None:
            html += "<td class='err'>ERR</td>"
        else:
            cl = "T" if res else "F"
            html += f"<td class='{cl}'>{'T' if res else 'F'}</td>"
        html += "</tr>"
        rows_data.append((vals, res))
    html += "</tbody></table>"
    return html, rows_data

def check_tautology(rows_data):
    if not rows_data:
        return None
    results = [r for _, r in rows_data]
    if all(r is True for r in results):
        return "TAUTOLOGY — true for all assignments"
    if all(r is False for r in results):
        return "CONTRADICTION — false for all assignments"
    return "CONTINGENCY — neither tautology nor contradiction"

def relation_properties(n: int, pairs: list[tuple]) -> dict:
    """Check reflexive, irreflexive, symmetric, antisymmetric, transitive."""
    pair_set = set(pairs)
    diag = {(i, i) for i in range(n)}

    reflexive = all((i, i) in pair_set for i in range(n))
    irreflexive = all((i, i) not in pair_set for i in range(n))
    symmetric = all((b, a) in pair_set for (a, b) in pair_set)
    antisymmetric = all(
        not ((b, a) in pair_set and a != b) for (a, b) in pair_set
    )
    # Transitive: for all (a,b) and (b,c) in R -> (a,c) in R
    transitive = all(
        (a, c) in pair_set
        for (a, b) in pair_set
        for (b2, c) in pair_set
        if b == b2
    )
    return {
        "Reflexive": reflexive,
        "Irreflexive": irreflexive,
        "Symmetric": symmetric,
        "Antisymmetric": antisymmetric,
        "Transitive": transitive,
    }

def matrix_to_pairs(matrix: list[list[int]]) -> list[tuple]:
    n = len(matrix)
    return [(i, j) for i in range(n) for j in range(n) if matrix[i][j]]

def reflexive_closure(n: int, pairs: list[tuple]) -> list[tuple]:
    s = set(pairs)
    s |= {(i, i) for i in range(n)}
    return sorted(s)

def symmetric_closure(pairs: list[tuple]) -> list[tuple]:
    s = set(pairs)
    s |= {(b, a) for (a, b) in pairs}
    return sorted(s)

def transitive_closure(n: int, pairs: list[tuple]) -> list[tuple]:
    """Warshall's algorithm."""
    reach = [[False] * n for _ in range(n)]
    for (a, b) in pairs:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return [(i, j) for i in range(n) for j in range(n) if reach[i][j]]

def draw_venn_matplotlib(set_a_items: list, set_b_items: list, operation: str):
    """Draw a Venn diagram using matplotlib and return the figure."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    As = set(str(x) for x in set_a_items)
    Bs = set(str(x) for x in set_b_items)
    only_a  = sorted(As - Bs)
    both_ab = sorted(As & Bs)
    only_b  = sorted(Bs - As)

    CYAN   = '#4ECCA3'
    PURPLE = '#AFA9EC'
    ORANGE = '#ff9f4a'
    BG     = '#0a0a14'

    hl_map = {
        'union':        (True,  True,  True ),
        'intersection': (False, True,  False),
        'diff_ab':      (True,  False, False),
        'diff_ba':      (False, False, True ),
    }
    hl_a, hl_ab, hl_b = hl_map.get(operation, (False, False, False))

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.1, 2.1)
    ax.set_aspect('equal')
    ax.axis('off')

    cx_a, cx_b, cy, r = -0.78, 0.78, 0.0, 1.48

    # Filled regions
    ax.add_patch(Circle((cx_a, cy), r, color=CYAN,   alpha=0.38 if hl_a  else 0.06, linewidth=0, zorder=2))
    ax.add_patch(Circle((cx_b, cy), r, color=PURPLE, alpha=0.38 if hl_b  else 0.06, linewidth=0, zorder=2))

    # Intersection highlight via clip path
    if hl_ab:
        clip_circle = Circle((cx_b, cy), r, transform=ax.transData)
        inter = Circle((cx_a, cy), r, color=ORANGE, alpha=0.58, linewidth=0, zorder=3)
        inter.set_clip_path(clip_circle)
        ax.add_patch(inter)

    # Outlines
    ax.add_patch(Circle((cx_a, cy), r, fill=False, edgecolor=CYAN,   linewidth=2.5, zorder=5))
    ax.add_patch(Circle((cx_b, cy), r, fill=False, edgecolor=PURPLE, linewidth=2.5, zorder=5))

    # Circle labels
    ax.text(cx_a - 0.9, cy + r + 0.22, 'A', color=CYAN,   fontsize=20,
            fontweight='bold', fontfamily='monospace', ha='center', va='center')
    ax.text(cx_b + 0.9, cy + r + 0.22, 'B', color=PURPLE, fontsize=20,
            fontweight='bold', fontfamily='monospace', ha='center', va='center')

    def region_text(items, limit=5):
        if not items:
            return '∅'
        s = '\n'.join(items[:limit])
        if len(items) > limit:
            s += f'\n+{len(items) - limit} more'
        return s

    col_a  = CYAN   if hl_a  else '#4a5568'
    col_ab = ORANGE if hl_ab else '#4a5568'
    col_b  = PURPLE if hl_b  else '#4a5568'

    # Region element text
    ax.text(cx_a - 0.68, cy + 0.15, region_text(only_a),  color=col_a,  fontsize=8.5,
            fontfamily='monospace', ha='center', va='center', linespacing=1.7, zorder=6)
    ax.text(0.0,          cy + 0.15, region_text(both_ab), color=col_ab, fontsize=8.5,
            fontfamily='monospace', ha='center', va='center', linespacing=1.7, zorder=6)
    ax.text(cx_b + 0.68,  cy + 0.15, region_text(only_b),  color=col_b,  fontsize=8.5,
            fontfamily='monospace', ha='center', va='center', linespacing=1.7, zorder=6)

    # Sub-region labels
    ax.text(cx_a - 0.68, cy - r + 0.38, 'A − B', color=col_a,  fontsize=7.5,
            alpha=0.75, fontfamily='monospace', ha='center', va='center', style='italic')
    ax.text(0.0,          cy - r + 0.38, 'A ∩ B', color=col_ab, fontsize=7.5,
            alpha=0.75, fontfamily='monospace', ha='center', va='center', style='italic')
    ax.text(cx_b + 0.68,  cy - r + 0.38, 'B − A', color=col_b,  fontsize=7.5,
            alpha=0.75, fontfamily='monospace', ha='center', va='center', style='italic')

    op_titles = {
        'union':        'Highlighted: A ∪ B  (Union)',
        'intersection': 'Highlighted: A ∩ B  (Intersection)',
        'diff_ab':      'Highlighted: A − B  (Difference)',
        'diff_ba':      'Highlighted: B − A  (Difference)',
    }
    ax.set_title(op_titles.get(operation, 'Venn Diagram'),
                 color='#e8eaf0', fontsize=11, pad=10, fontfamily='monospace')

    plt.tight_layout(pad=0.4)
    return fig


def compose_relations(r1: list[tuple], r2: list[tuple]) -> list[tuple]:
    """R1 ∘ R2 = {(a,c) | ∃b: (a,b) ∈ R1 ∧ (b,c) ∈ R2}"""
    r2_dict: dict[int, list] = {}
    for (b, c) in r2:
        r2_dict.setdefault(b, []).append(c)
    result = set()
    for (a, b) in r1:
        for c in r2_dict.get(b, []):
            result.add((a, c))
    return sorted(result)

def is_equivalence(n: int, pairs: list[tuple]) -> bool:
    props = relation_properties(n, pairs)
    return props["Reflexive"] and props["Symmetric"] and props["Transitive"]

def equivalence_classes(n: int, pairs: list[tuple]) -> dict[int, list[int]]:
    """Find equivalence classes using Union-Find."""
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    for (a, b) in pairs:
        if a != b:
            union(a, b)
    classes: dict[int, list[int]] = {}
    for i in range(n):
        root = find(i)
        classes.setdefault(root, []).append(i)
    return classes

def is_partial_order(n: int, pairs: list[tuple]) -> bool:
    props = relation_properties(n, pairs)
    return props["Reflexive"] and props["Antisymmetric"] and props["Transitive"]

def graph_analyze(adj: list[list[int]]) -> dict:
    n = len(adj)
    degrees = [sum(row) for row in adj]
    total_deg = sum(degrees)
    edges = total_deg // 2
    odd = sum(1 for d in degrees if d % 2 != 0)
    # BFS connectivity
    visited = [False] * n
    queue = [0]
    visited[0] = True
    cnt = 1
    while queue:
        u = queue.pop(0)
        for v in range(n):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                cnt += 1
                queue.append(v)
    return {
        "vertices": n,
        "edges": edges,
        "degrees": degrees,
        "total_degree": total_deg,
        "connected": cnt == n,
        "odd_degree_count": odd,
        "eulerian": (
            "Eulerian Circuit exists (all even degrees)"
            if odd == 0
            else ("Eulerian Path exists (exactly 2 odd-degree vertices)" if odd == 2
                  else f"No Eulerian path/circuit ({odd} odd-degree vertices)")
        ),
    }

def induction_checker(formula_type: str, n_val: int) -> str:
    """Check specific induction formulae."""
    if formula_type == "sum_natural":
        lhs = sum(range(1, n_val + 1))
        rhs = n_val * (n_val + 1) // 2
        return f"Base case (n=1): 1 = 1·2/2 = 1 ✓\nInductive hypothesis: Assume true for k.\nInductive step: sum(1..{n_val}) = {lhs}, formula = {n_val}·{n_val+1}/2 = {rhs}\n{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}"
    elif formula_type == "sum_squares":
        lhs = sum(i * i for i in range(1, n_val + 1))
        rhs = n_val * (n_val + 1) * (2 * n_val + 1) // 6
        return f"Base case (n=1): 1² = 1·2·3/6 = 1 ✓\nInductive step: Σi²(1..{n_val}) = {lhs}, formula = {n_val}·{n_val+1}·{2*n_val+1}/6 = {rhs}\n{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}"
    elif formula_type == "geometric":
        r = 2
        lhs = sum(r**i for i in range(n_val + 1))
        rhs = r**(n_val + 1) - 1
        return f"Geometric sum Σ 2^i (i=0..{n_val}):\nBase (n=0): 1 = 2^1-1 = 1 ✓\nStep: sum = {lhs}, 2^({n_val}+1)-1 = {rhs}\n{'✓ Holds!' if lhs == rhs else '✗ Mismatch'}"
    elif formula_type == "power_of_2":
        lhs = 2**n_val
        rhs = 2**n_val
        return f"Claim: 2^n divisible by 2 for n≥1\n2^{n_val} = {lhs}\nBase (n=1): 2^1=2, divisible by 2 ✓\nInductive step: if 2^k is divisible by 2, then 2^(k+1)=2·2^k also divisible by 2 ✓"
    return "Formula not recognized."

def compute_sequence_summation(seq_type: str, n_val: int) -> str:
    if seq_type == "arithmetic":
        d = 3
        terms = [1 + (i * d) for i in range(n_val)]
        s = sum(terms)
        return (f"Arithmetic sequence (a=1, d={d}):\n"
                f"Terms: {terms}\n"
                f"S_n = n/2·(2a+(n-1)d) = {n_val}/2·(2+{(n_val-1)*d}) = {s}")
    elif seq_type == "geometric":
        r = 2
        terms = [r**i for i in range(n_val)]
        s = sum(terms)
        return (f"Geometric sequence (a=1, r={r}):\n"
                f"Terms: {terms}\n"
                f"S_n = a·(r^n - 1)/(r-1) = ({r**n_val}-1)/({r}-1) = {s}")
    elif seq_type == "fibonacci":
        fibs = [1, 1]
        for _ in range(n_val - 2):
            fibs.append(fibs[-1] + fibs[-2])
        fibs = fibs[:n_val]
        return (f"Fibonacci sequence (F_1=1, F_2=1):\n"
                f"Terms: {fibs}\n"
                f"F_{n_val} = {fibs[-1]}")
    return ""

def call_groq_nlp(user_statement: str) -> str:
    """Call Groq API to parse and solve natural language discrete math problems."""
    try:
        from groq import Groq  # type: ignore
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        system_prompt = """You are an expert in Discrete Mathematics. 
The user will give you a problem in plain English. 
Parse it and solve it step-by-step. Topics covered:
- Set Theory: union, intersection, difference, symmetric difference, Venn diagrams, set identities, Cartesian product
- Relations: ordered pairs, properties (reflexive/irreflexive/symmetric/antisymmetric/transitive), arrow diagrams, matrix representation, domain, range, composition, closures, equivalence classes, partial orderings
- Propositional Logic: truth tables, tautology/contradiction, propositional equivalences, predicates, quantifiers
- Rules of Inference: modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism, addition, simplification, conjunction, resolution
- Proof Methods: direct proof, proof by contradiction, proof by contrapositive, proof by cases
- Mathematical Induction: base case, inductive step
- Sequences and Summations: arithmetic, geometric, Fibonacci, summation formulas
- Combinatorics: permutations, combinations, pigeonhole principle
- Graph Theory basics: vertices, edges, degree, connectivity, Eulerian paths

Respond with:
1. Problem interpretation
2. Mathematical formulation  
3. Step-by-step solution
4. Final answer

Keep it clear and educational."""
        
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_statement},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            temperature=0.3,
        )
        return chat.choices[0].message.content
    except ImportError:
        return "❌ groq package not installed. Run: pip install groq"
    except KeyError:
        return "❌ GROQ_API_KEY environment variable not set."
    except Exception as e:
        return f"❌ Groq API error: {str(e)}"


def call_notation_converter(statement: str) -> dict:
    """Convert an English statement into discrete math notation using Groq."""
    system_prompt = """You are an expert in Discrete Mathematics and Propositional Logic.
Convert the given English statement(s) into formal discrete mathematical notation.

Instructions:
1. Identify each atomic proposition and assign short variable names (p, q, r, s, ...).
2. Identify the logical connective(s): → (if-then), ∧ (and), ∨ (or), ¬ (not), ↔ (iff).
3. Write the complete formal notation.
4. If the input contains multiple statements forming an argument (premises + conclusion), also write the argument form.
5. Name the argument form if applicable (e.g., Modus Ponens, Modus Tollens, Hypothetical Syllogism).

Respond in this EXACT JSON format — pure JSON only, no markdown fences:
{
  "variables": [
    {"symbol": "p", "meaning": "..."},
    {"symbol": "q", "meaning": "..."}
  ],
  "notation": "p → q",
  "argument_form": "p → q\\np\\n∴ q",
  "form_name": "Modus Ponens",
  "explanation": "Short explanation of the conversion",
  "truth_condition": "This is true when ..."
}
If there is no multi-statement argument, set "argument_form" and "form_name" to empty strings."""

    raw = ""
    try:
        from groq import Groq  # type: ignore
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert to discrete math notation:\n{statement}"},
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=700,
            temperature=0.1,
        )
        raw = resp.choices[0].message.content.strip()
        import json as _json, re as _re
        cleaned = _re.sub(r'```(?:json)?\s*|\s*```', '', raw).strip()
        data = _json.loads(cleaned)
        return {"success": True, "data": data}
    except KeyError:
        return {"success": False, "error": "GROQ_API_KEY environment variable not set."}
    except ImportError as e:
        return {"success": False, "error": f"Package not installed: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e), "raw": raw}


# ═══════════════════════════════════════════════════════════
# NAVIGATION (query-param based, top navbar)
# ═══════════════════════════════════════════════════════════

# ── Overlay navigation ──────────────────────────────────────────────
NAV_META = [
    ("home",          "Home",                  "△",  "Overview · Team",                ""),
    ("sets",          "Set Theory",            "∩",  "Sets · Venn · Identities",       "W2-3"),
    ("relations",     "Relations",             "↔",  "Properties · Closures · Posets", "W4-8"),
    ("logic",         "Propositional Logic",   "∧",  "Truth Tables · Predicates",      "W9-11"),
    ("inference",     "Rules of Inference",    "∴",  "Modus Ponens · Arguments",       "W12-13"),
    ("proofs",        "Proof Methods",         "□",  "Direct · Contradiction",         "W14-15"),
    ("induction",     "Mathematical Induction","Σ",  "Base Case · Inductive Step",     "W16"),
    ("sequences",     "Sequences",             "∿",  "Arithmetic · Fibonacci",         "W8"),
    ("combinatorics", "Combinatorics",         "⊕",  "Perms · Combinations",           ""),
    ("graphs",        "Graph Theory",          "◇",  "Vertices · Eulerian Paths",      ""),
    ("ai",            "AI Problem Solver",     "⚡", "Ask Anything",                    ""),
    ("studyhub",      "Study Hub",             "◎",  "Progress · Roadmap · Session",   "NEW"),
]

section = st.query_params.get("page", "home")
if section not in [m[0] for m in NAV_META]:
    section = "home"

def build_overlay_nav(current: str) -> None:
    items = ""
    for key, label, icon, sub, badge in NAV_META:
        active_cls = "sb-active" if current == key else ""
        badge_html = f'<span class="sb-badge">{badge}</span>' if badge else ""
        items += f"""
<a href="?page={key}" target="_top" class="sb-item {active_cls}">
  <span class="sb-icon">{icon}</span>
  <span class="sb-text">
    <span class="sb-label">{label}</span>
    <span class="sb-sub">{sub}</span>
  </span>
  {badge_html}
</a>"""

    html = f"""
<!-- Hidden checkbox drives open/close via CSS -->
<input type="checkbox" id="_nav_chk">

<!-- Hamburger label -->
<label for="_nav_chk" id="_nav_btn" title="Navigation">
  <span></span><span></span><span></span>
</label>

<!-- Backdrop: clicking it unchecks the checkbox -->
<label for="_nav_chk" id="_nav_bd"></label>

<!-- Slide-in panel -->
<div id="_nav_panel">
  <div class="sb-head" style="display:flex;align-items:center;justify-content:space-between;">
    <div>
      <div class="sb-wordmark">Master Discrete Mathematics</div>
      <div class="sb-brand">DS<span>://</span>logic.arc</div>
    </div>
    <label for="_nav_chk" style="background:none;border:none;color:#4a5568;cursor:pointer;font-size:1.1rem;padding:0 4px;line-height:1;">✕</label>
  </div>
  <div class="sb-section">// Course Modules</div>
  <div class="sb-list">{items}
  </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

build_overlay_nav(section)

# ── Footer HTML (shared across all pages) ─────────────────
FOOTER_HTML = """
<div style='text-align:center;padding:2rem 0 1rem;'>
  <div style='font-family:"JetBrains Mono",monospace;font-size:0.72rem;color:#4ECCA3;letter-spacing:0.05em;'>
    DISCRETE STRUCTURES: THE ARCHITECTURE OF LOGIC
  </div>
  <div style='font-family:"JetBrains Mono",monospace;font-size:0.65rem;color:#4a5568;margin-top:0.6rem;'>
    <span style='color:#8892a4;'>Farhan Haroon</span> \u00b7 FA25-BSAI-0060 &nbsp;|&nbsp;
    <span style='color:#8892a4;'>Huzaifa Zaki</span> \u00b7 FA25-BSAI-0051 &nbsp;|&nbsp;
    <span style='color:#8892a4;'>Bissam ul Haq</span> \u00b7 FA25-BSAI-0076 &nbsp;|&nbsp;
    <span style='color:#8892a4;'>Aaleen</span> \u00b7 FA25-BSAI-0077
  </div>
  <div style='margin-top:0.8rem;font-size:0.65rem;color:#2a2d4a;'>\u2200x [ Discrete(x) \u2192 Beautiful(x) ] \u2014 BSAI \u00b7 CS Department</div>
</div>
"""

# ═══════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════
if section == "home":
    st.markdown("""
    <div style='text-align:center;padding:3rem 0 2rem;'>
      <div class='badge'>∀x ∈ 𝕌 : P(x) ⟹ Q(x)</div>
      <div class='hero-title'>Discrete Structures:<br><em>The Architecture of Logic</em></div>
      <p style='font-family:"JetBrains Mono",monospace;color:#8892a4;margin-top:1rem;font-size:0.9rem;line-height:1.8;'>
        Where mathematics meets engineering.<br>
        Set algebra. Relations. Propositional logic. Proof methods. Induction.<br>
        The formal language of computation.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='sec-tag'>// COURSE_OUTLINE — TOPICS</div>
    <h3 style='color:#e8eaf0;margin-bottom:1.2rem;'>What You'll Explore</h3>
    """, unsafe_allow_html=True)

    topics = [
        ("2", "Set Operations Theory", "Venn Diagrams, Set identities, Exercises"),
        ("3", "Application of Venn Diagram", "Set identities, Exercises"),
        ("4", "Relations on Sets", "Ordered pairs, Cartesian product, Binary relation, Domain"),
        ("5", "Range & Representations", "Arrow diagram, Directed graph, Matrix representation"),
        ("6", "Types of Relations I", "Reflexive, Irreflexive, Symmetric, Antisymmetric"),
        ("7", "Types of Relations II", "Transitive, Combining, Composition"),
        ("8", "Closures & Equivalences", "Closures, Equivalence classes, Partial Orderings, Sequences"),
        ("9", "Logic Foundations", "Propositional Logic, Applications"),
        ("10", "Propositional Equivalences", "Predicates and Quantifiers"),
        ("11", "Predicates & Quantifiers", "Exercises"),
        ("12", "Rules of Inference", "Propositional Logic inference rules"),
        ("13", "Building Arguments", "Using rules of inference"),
        ("14", "Introduction to Proof", "Proof methods overview"),
        ("15", "Proof Methods", "Direct, Contradiction, Contrapositive"),
        ("16", "Mathematical Induction", "Base case, Inductive step"),
    ]

    cols = st.columns(3)
    for idx, (week, title, desc) in enumerate(topics):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='card'>
              <div style='font-family:"JetBrains Mono",monospace;font-size:0.65rem;color:#4ECCA3;margin-bottom:0.3rem;'>WEEK_{week}</div>
              <div style='font-size:0.9rem;font-weight:600;color:#e8eaf0;margin-bottom:0.3rem;'>{title}</div>
              <div style='font-size:0.78rem;color:#8892a4;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-tag'>// TEAM_MEMBERS</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='team-grid'>
      <div class='team-card'><div class='team-id'>MEMBER_01</div><div class='team-name'>Farhan Haroon</div><div class='team-num'>FA25-BSAI-0060</div></div>
      <div class='team-card'><div class='team-id'>MEMBER_02</div><div class='team-name'>Huzaifa Zaki</div><div class='team-num'>FA25-BSAI-0051</div></div>
      <div class='team-card'><div class='team-id'>MEMBER_03</div><div class='team-name'>Bissam ul Haq</div><div class='team-num'>FA25-BSAI-0076</div></div>
      <div class='team-card'><div class='team-id'>MEMBER_04</div><div class='team-name'>Aaleen</div><div class='team-num'>FA25-BSAI-0077</div></div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# SET THEORY
# ═══════════════════════════════════════════════════════════
elif section == "sets":
    st.markdown("<div class='sec-tag'>// WEEK_02-03 · SET_THEORY</div>", unsafe_allow_html=True)
    st.markdown("## Set Theory & Venn Diagrams")
    st.markdown("""
    <p style='color:#8892a4;'>
    A <b style='color:#b8c4d4;'>set</b> is an unordered collection of distinct objects.
    Set operations are the foundation of logic, databases, and AI.
    </p>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚙️ Set Calculator", "🔵 Venn Visualizer", "📖 Set Identities"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            set_a_raw = st.text_input("Set A (comma-separated)", "1, 2, 3, 4, 5", key="sa")
            set_b_raw = st.text_input("Set B (comma-separated)", "3, 4, 5, 6, 7", key="sb")
            set_c_raw = st.text_input("Set C (optional, for 3-set ops)", "", key="sc")
        with col2:
            universe_raw = st.text_input("Universal Set U (optional, for complement)", "1,2,3,4,5,6,7,8,9,10", key="su")
        
        if st.button("🔢 Compute All Set Operations", key="set_run"):
            A = parse_set(set_a_raw)
            B = parse_set(set_b_raw)
            U = parse_set(universe_raw) if universe_raw.strip() else list(set(A + B))
            As, Bs = set(A), set(B)
            union = list(dict.fromkeys(A + [x for x in B if x not in As]))
            inter = [x for x in A if x in Bs]
            diff_ab = [x for x in A if x not in Bs]
            diff_ba = [x for x in B if x not in As]
            sym_diff = diff_ab + diff_ba
            comp_a = [x for x in U if x not in As]
            comp_b = [x for x in U if x not in Bs]
            cart = [(a, b) for a in A for b in B]

            results = [
                ("A", fmt_set(A), f"|A| = {len(A)}"),
                ("B", fmt_set(B), f"|B| = {len(B)}"),
                ("A ∪ B", fmt_set(union), f"|A ∪ B| = {len(union)}"),
                ("A ∩ B", fmt_set(inter), f"|A ∩ B| = {len(inter)}"),
                ("A − B", fmt_set(diff_ab), f"|A − B| = {len(diff_ab)}"),
                ("B − A", fmt_set(diff_ba), f"|B − A| = {len(diff_ba)}"),
                ("A △ B", fmt_set(sym_diff), f"Symmetric difference"),
                ("Ā (comp. of A)", fmt_set(comp_a), f"Elements in U but not A"),
                ("B̄ (comp. of B)", fmt_set(comp_b), f"Elements in U but not B"),
                ("A × B", str(cart[:10]) + ("..." if len(cart) > 10 else ""), f"|A × B| = {len(cart)}"),
            ]
            # Inclusion-exclusion
            ie = len(inter)
            st.markdown(f"<div class='formula'>|A ∪ B| = |A| + |B| − |A ∩ B| = {len(A)} + {len(B)} − {ie} = {len(union)}</div>", unsafe_allow_html=True)

            html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Operation</th><th style='text-align:left'>Result</th><th style='text-align:left'>Note</th></tr></thead><tbody>"
            for op, res, note in results:
                html += f"<tr><td class='T' style='text-align:left;padding-right:1rem'>{op}</td><td style='color:#b8c4d4'>{res}</td><td style='color:#4a5568;font-size:0.72rem'>{note}</td></tr>"
            html += "</tbody></table>"
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

            # 3-set if C provided
            if set_c_raw.strip():
                C = parse_set(set_c_raw)
                Cs = set(C)
                inter3 = [x for x in inter if x in Cs]
                union3 = list(set(A + B + C))
                st.info(f"**3-Set:** A ∩ B ∩ C = {fmt_set(inter3)} | A ∪ B ∪ C = {fmt_set(union3)}")

    with tab2:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>VENN_DIAGRAM · INTERACTIVE VISUALIZER</div>
          <p style='color:#8892a4;font-size:0.85rem;'>
          Enter sets A and B, choose an operation, and click <b style='color:#4ECCA3;'>Visualize</b>
          to see a colour-coded Venn diagram with your actual elements placed in each region.
          </p>
          <ul style='color:#8892a4;font-size:0.85rem;margin-left:1.2rem;line-height:2;'>
            <li><span style='color:#4ECCA3;'>Green region</span> — Only in A (A − B)</li>
            <li><span style='color:#ff9f4a;'>Orange region</span> — In both A and B (A ∩ B)</li>
            <li><span style='color:#AFA9EC;'>Purple region</span> — Only in B (B − A)</li>
          </ul>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            set_a_v = st.text_input("Set A", "Ali, Sara, Huzaifa, Farhan", key="va")
            set_b_v = st.text_input("Set B", "Sara, Ahmed, Bilal, Huzaifa", key="vb")
        with col2:
            op_v = st.selectbox("Operation to highlight", ["Union (A ∪ B)", "Intersection (A ∩ B)", "Difference (A − B)", "Complement region (B − A)"])

        if st.button("🔵 Visualize Venn Diagram", key="venn_run"):
            A = parse_set(set_a_v)
            B = parse_set(set_b_v)
            As, Bs = set(A), set(B)
            only_a = [x for x in A if x not in Bs]
            both   = [x for x in A if x in Bs]
            only_b = [x for x in B if x not in As]

            op_key_map = {
                "Union (A ∪ B)":          "union",
                "Intersection (A ∩ B)":   "intersection",
                "Difference (A − B)":     "diff_ab",
                "Complement region (B − A)": "diff_ba",
            }
            op_result_map = {
                "Union (A ∪ B)":          only_a + both + only_b,
                "Intersection (A ∩ B)":   both,
                "Difference (A − B)":     only_a,
                "Complement region (B − A)": only_b,
            }
            op_key     = op_key_map[op_v]
            highlighted = op_result_map[op_v]

            # ── Matplotlib Venn diagram ────────────────────────
            import matplotlib.pyplot as plt
            fig = draw_venn_matplotlib(A, B, op_key)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            # ── Text region summary ────────────────────────────
            st.markdown(f"""
            <div class='result-box' style='margin-top:0.8rem;'>
              <div style='color:#4ECCA3;margin-bottom:0.5rem;'>Region I — Only in A (A − B):</div>
              <div style='margin-bottom:0.8rem;'>{fmt_set(only_a)}</div>
              <div style='color:#ff9f4a;margin-bottom:0.5rem;'>Region II — In both (A ∩ B):</div>
              <div style='margin-bottom:0.8rem;'>{fmt_set(both)}</div>
              <div style='color:#AFA9EC;margin-bottom:0.5rem;'>Region III — Only in B (B − A):</div>
              <div style='margin-bottom:0.8rem;'>{fmt_set(only_b)}</div>
              <hr style='border-color:#2a2d4a;margin:0.6rem 0;'/>
              <div style='color:#e8eaf0;margin-bottom:0.3rem;font-weight:600;'>Highlighted ({op_v}):</div>
              <div style='font-weight:700;font-size:1rem;color:#e8eaf0;'>{fmt_set(highlighted)}</div>
              <div style='color:#4a5568;margin-top:0.5rem;'>|result| = {len(highlighted)}</div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class='sec-tag'>SET_IDENTITIES</div>
        <h4 style='color:#e8eaf0;margin-bottom:1rem;'>Fundamental Set Laws</h4>
        """, unsafe_allow_html=True)
        identities = [
            ("Commutative", "A ∪ B = B ∪ A", "A ∩ B = B ∩ A"),
            ("Associative", "A ∪ (B ∪ C) = (A ∪ B) ∪ C", "A ∩ (B ∩ C) = (A ∩ B) ∩ C"),
            ("Distributive", "A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)", "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)"),
            ("Identity", "A ∪ ∅ = A", "A ∩ U = A"),
            ("Complement", "A ∪ Ā = U", "A ∩ Ā = ∅"),
            ("De Morgan's", "A ∪ B̄ = Ā ∩ B̄", "A ∩ B̄ = Ā ∪ B̄"),
            ("Idempotent", "A ∪ A = A", "A ∩ A = A"),
            ("Double Complement", "Ā̄ = A", "—"),
            ("Domination", "A ∪ U = U", "A ∩ ∅ = ∅"),
            ("Absorption", "A ∪ (A ∩ B) = A", "A ∩ (A ∪ B) = A"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th>Law</th><th>Union Form</th><th>Intersection Form</th></tr></thead><tbody>"
        for law, f1, f2 in identities:
            html += f"<tr><td class='T' style='text-align:left'>{law}</td><td style='color:#b8c4d4'>{f1}</td><td style='color:#AFA9EC'>{f2}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# RELATIONS
# ═══════════════════════════════════════════════════════════
elif section == "relations":
    st.markdown("<div class='sec-tag'>// WEEK_04-08 · RELATIONS</div>", unsafe_allow_html=True)
    st.markdown("## Relations on Sets")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Property Checker",
        "🔀 Closures",
        "🔁 Composition",
        "≡ Equivalence Classes",
        "≤ Partial Orderings",
    ])

    with tab1:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>ORDERED_PAIRS · MATRIX_REPRESENTATION</div>
          <p style='color:#8892a4;font-size:0.85rem;'>
          A <b style='color:#b8c4d4;'>binary relation</b> R on set A is a subset of A × A.
          Enter a <b style='color:#b8c4d4;'>relation matrix</b> (0/1) to check all five properties.
          </p>
        </div>""", unsafe_allow_html=True)

        n_rel = st.slider("Set size n (elements: 0 to n-1)", 2, 6, 3, key="nrel")
        st.markdown(f"<div class='formula'>Relation R ⊆ {{{', '.join(str(i) for i in range(n_rel))}}} × {{{', '.join(str(i) for i in range(n_rel))}}}</div>", unsafe_allow_html=True)
        st.markdown("**Enter relation matrix (row i, col j = 1 means (i,j) ∈ R):**")

        matrix = []
        for i in range(n_rel):
            cols = st.columns(n_rel)
            row = []
            for j in range(n_rel):
                val = cols[j].selectbox(f"({i},{j})", [0, 1], key=f"rel_{i}_{j}")
                row.append(val)
            matrix.append(row)

        if st.button("🔍 Analyze Relation Properties", key="rel_run"):
            pairs = matrix_to_pairs(matrix)
            props = relation_properties(n_rel, pairs)

            # Arrow diagram representation
            st.markdown("**Pairs in R:** " + (str(pairs) if pairs else "∅ (empty relation)"))
            st.markdown("<div class='formula'>Domain: {" + ", ".join(str(a) for a, _ in pairs) + "} | Range: {" + ", ".join(str(b) for _, b in pairs) + "}</div>", unsafe_allow_html=True)

            html = "<table class='tt'><thead><tr><th>Property</th><th>Status</th><th>Explanation</th></tr></thead><tbody>"
            explanations = {
                "Reflexive": "∀a ∈ A: (a,a) ∈ R — every element relates to itself",
                "Irreflexive": "∀a ∈ A: (a,a) ∉ R — no element relates to itself",
                "Symmetric": "∀a,b: (a,b) ∈ R → (b,a) ∈ R",
                "Antisymmetric": "∀a≠b: (a,b) ∈ R → (b,a) ∉ R",
                "Transitive": "∀a,b,c: (a,b),(b,c) ∈ R → (a,c) ∈ R",
            }
            for prop, val in props.items():
                status = "✓ YES" if val else "✗ NO"
                cl = "T" if val else "F"
                html += f"<tr><td style='text-align:left;color:#e8eaf0;'>{prop}</td><td class='{cl}'>{status}</td><td style='color:#8892a4;font-size:0.72rem;text-align:left;'>{explanations[prop]}</td></tr>"
            html += "</tbody></table>"
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

            # Relation type summary
            is_eq = is_equivalence(n_rel, pairs)
            is_po = is_partial_order(n_rel, pairs)
            summary = []
            if is_eq:
                summary.append("✓ This is an EQUIVALENCE RELATION (reflexive + symmetric + transitive)")
            if is_po:
                summary.append("✓ This is a PARTIAL ORDER (reflexive + antisymmetric + transitive)")
            if props["Symmetric"] and props["Transitive"] and not props["Reflexive"]:
                summary.append("⚠ Symmetric + Transitive but not Reflexive → not equivalence")
            if not summary:
                summary.append("No special classification")
            for s in summary:
                st.info(s)

    with tab2:
        st.markdown("<div class='sec-tag'>CLOSURES · WARSHALL'S ALGORITHM</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color:#8892a4;'>
        The <b style='color:#b8c4d4;'>closure</b> of a relation is the smallest relation with a given property
        that contains the original relation.
        </p>""", unsafe_allow_html=True)

        n_cl = st.slider("Set size", 2, 5, 3, key="ncl")
        pairs_raw = st.text_input("Enter pairs as (i,j) comma-separated", "0,1 | 1,2 | 2,0", key="clpairs")

        def parse_pairs(s, n):
            result = []
            try:
                for token in s.split("|"):
                    token = token.strip()
                    if not token:
                        continue
                    parts = token.replace("(", "").replace(")", "").split(",")
                    a, b = int(parts[0].strip()), int(parts[1].strip())
                    if 0 <= a < n and 0 <= b < n:
                        result.append((a, b))
            except Exception:
                pass
            return result

        if st.button("Compute Closures", key="cl_run"):
            pairs = parse_pairs(pairs_raw, n_cl)
            rc = reflexive_closure(n_cl, pairs)
            sc = symmetric_closure(pairs)
            tc = transitive_closure(n_cl, pairs)

            st.markdown(f"**Original R:** {pairs}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>REFLEXIVE CLOSURE</div>
                  <div style='color:#4ECCA3;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{rc}</div>
                  <div style='color:#8892a4;font-size:0.75rem;margin-top:0.5rem;'>Added: {set(rc) - set(pairs)}</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>SYMMETRIC CLOSURE</div>
                  <div style='color:#AFA9EC;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{sc}</div>
                  <div style='color:#8892a4;font-size:0.75rem;margin-top:0.5rem;'>Added: {set(sc) - set(pairs)}</div>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>TRANSITIVE CLOSURE (Warshall)</div>
                  <div style='color:#ff9f4a;font-family:"JetBrains Mono",monospace;font-size:0.85rem;'>{tc}</div>
                  <div style='color:#8892a4;font-size:0.75rem;margin-top:0.5rem;'>Added: {set(tc) - set(pairs)}</div>
                </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='sec-tag'>COMPOSITION OF RELATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='formula'>R₁ ∘ R₂ = {(a,c) | ∃b: (a,b) ∈ R₁ ∧ (b,c) ∈ R₂}</div>", unsafe_allow_html=True)

        n_comp = st.slider("Set size", 2, 5, 3, key="ncomp")
        r1_raw = st.text_input("Relation R₁ (pairs: a,b | a,b ...)", "0,1 | 1,2 | 0,2", key="r1raw")
        r2_raw = st.text_input("Relation R₂ (pairs: a,b | a,b ...)", "1,0 | 2,1", key="r2raw")

        if st.button("Compose R₁ ∘ R₂", key="comp_run"):
            r1 = parse_pairs(r1_raw, n_comp)
            r2 = parse_pairs(r2_raw, n_comp)
            composed = compose_relations(r1, r2)
            st.markdown(f"**R₁:** {r1}")
            st.markdown(f"**R₂:** {r2}")
            st.markdown(f"<div class='result-box'><span style='color:#4ECCA3;'>R₁ ∘ R₂ = </span>{composed}</div>", unsafe_allow_html=True)
            # Show step-by-step
            steps = []
            for (a, b) in r1:
                for (b2, c) in r2:
                    if b == b2:
                        steps.append(f"({a},{b}) ∈ R₁ and ({b},{c}) ∈ R₂  →  ({a},{c}) ∈ R₁∘R₂")
            st.markdown("**Steps:**")
            for s in steps:
                st.markdown(f"- {s}")

    with tab4:
        st.markdown("<div class='sec-tag'>EQUIVALENCE CLASSES</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color:#8892a4;'>
        An <b style='color:#b8c4d4;'>equivalence relation</b> is reflexive, symmetric, and transitive.
        It partitions the set into disjoint <b style='color:#4ECCA3;'>equivalence classes</b>.
        </p>""", unsafe_allow_html=True)
        st.markdown("<div class='formula'>A / R = {[a] | a ∈ A} where [a] = {b ∈ A | aRb}</div>", unsafe_allow_html=True)

        n_eq = st.slider("Set size", 2, 8, 4, key="neq")
        eq_raw = st.text_input("Relation R (pairs: a,b | ...)", "0,0 | 1,1 | 2,2 | 3,3 | 0,1 | 1,0 | 2,3 | 3,2", key="eqraw")

        if st.button("Find Equivalence Classes", key="eq_run"):
            pairs = parse_pairs(eq_raw, n_eq)
            props = relation_properties(n_eq, pairs)
            is_eq = is_equivalence(n_eq, pairs)
            if is_eq:
                classes = equivalence_classes(n_eq, pairs)
                st.success("✓ This IS an equivalence relation")
                html = f"<div style='color:#4ECCA3;margin-bottom:0.6rem;font-size:0.75rem;'>A/R has {len(classes)} equivalence class(es):</div>"
                for root, members in classes.items():
                    rep = members[0]
                    html += f"<div style='margin-bottom:0.4rem;'><span style='color:#4ECCA3;'>[{rep}]</span> = {{{', '.join(str(m) for m in members)}}}</div>"
                st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)
                st.info(f"The {n_eq} elements are partitioned into {len(classes)} equivalence class(es). Each class is mutually exclusive and collectively exhaustive.")
            else:
                missing = [k for k, v in props.items() if not v and k in ("Reflexive", "Symmetric", "Transitive")]
                st.error(f"✗ NOT an equivalence relation. Missing: {', '.join(missing)}")

    with tab5:
        st.markdown("<div class='sec-tag'>PARTIAL ORDERINGS (POSET)</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color:#8892a4;'>
        A <b style='color:#b8c4d4;'>partial order</b> is a relation that is reflexive, antisymmetric, and transitive.
        The pair (A, R) is called a <b style='color:#4ECCA3;'>partially ordered set (POSET)</b>.
        </p>""", unsafe_allow_html=True)
        st.markdown("<div class='formula'>Poset (A, ≤) satisfies: reflexive + antisymmetric + transitive</div>", unsafe_allow_html=True)

        n_po = st.slider("Set size", 2, 6, 4, key="npo")
        po_raw = st.text_input("Relation R", "0,0 | 1,1 | 2,2 | 3,3 | 0,1 | 0,2 | 0,3 | 1,3 | 2,3", key="poraw")

        if st.button("Check Partial Order", key="po_run"):
            pairs = parse_pairs(po_raw, n_po)
            props = relation_properties(n_po, pairs)
            is_po = is_partial_order(n_po, pairs)
            if is_po:
                st.success("✓ This IS a Partial Order (POSET)")
                # Find minimal/maximal elements
                elements = list(range(n_po))
                has_predecessor = {b for (a, b) in pairs if a != b}
                has_successor = {a for (a, b) in pairs if a != b}
                minimal = [e for e in elements if e not in has_predecessor]
                maximal = [e for e in elements if e not in has_successor]
                st.markdown(f"""
                <div class='result-box'>
                  <div style='color:#4ECCA3;'>Minimal elements (no predecessors): {minimal}</div>
                  <div style='color:#AFA9EC;margin-top:0.4rem;'>Maximal elements (no successors): {maximal}</div>
                  <div style='color:#8892a4;margin-top:0.4rem;font-size:0.72rem;'>
                  Comparable pairs: {[(a,b) for (a,b) in pairs if a != b]}
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                missing = [k for k, v in props.items() if not v and k in ("Reflexive", "Antisymmetric", "Transitive")]
                st.error(f"✗ NOT a partial order. Missing: {', '.join(missing)}")
                for k, v in props.items():
                    if k in ("Reflexive", "Antisymmetric", "Transitive"):
                        st.markdown(f"- **{k}**: {'✓' if v else '✗'}")


# ═══════════════════════════════════════════════════════════
# PROPOSITIONAL LOGIC
# ═══════════════════════════════════════════════════════════
elif section == "logic":
    st.markdown("<div class='sec-tag'>// WEEK_09-11 · PROPOSITIONAL_LOGIC</div>", unsafe_allow_html=True)
    st.markdown("## Propositional Logic & Truth Tables")

    tab1, tab2, tab3 = st.tabs(["📊 Truth Table Generator", "≡ Equivalence Checker", "∀ Predicates & Quantifiers"])

    with tab1:
        st.markdown("""
        <div class='card'>
          <p style='color:#8892a4;font-size:0.85rem;'>
          Enter a logical expression using single lowercase letters as variables.
          Operators: <code>&amp;&amp;</code> (AND), <code>||</code> (OR), <code>!</code> (NOT),
          <code>-&gt;</code> (implication), <code>&lt;-&gt;</code> (biconditional), <code>XOR</code>
          </p>
        </div>""", unsafe_allow_html=True)

        expr = st.text_input("Logical expression", "(p && q) -> r", key="tt_expr")
        if st.button("Generate Truth Table", key="tt_run"):
            html, rows = gen_truth_table(expr)
            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)
            if rows:
                classification = check_tautology(rows)
                cl_color = "#4ECCA3" if "TAUTOLOGY" in classification else ("#ff6b6b" if "CONTRADICTION" in classification else "#ff9f4a")
                st.markdown(f"<div class='formula' style='color:{cl_color};border-color:{cl_color};'>Classification: {classification}</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:1.5rem;'>
        <div class='sec-tag'>COMMON EXPRESSIONS TO TRY</div>
        </div>""", unsafe_allow_html=True)
        examples = [
            "p -> p", "p || !p", "p && !p",
            "(p -> q) && (q -> r) -> (p -> r)",
            "(p && q) -> p", "p <-> p",
            "!(p && q) <-> (!p || !q)",
        ]
        for ex in examples:
            st.code(ex, language=None)

    with tab2:
        st.markdown("<div class='sec-tag'>PROPOSITIONAL_EQUIVALENCES</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            expr1 = st.text_input("Expression 1", "!(p && q)", key="eq1")
        with col2:
            expr2 = st.text_input("Expression 2", "!p || !q", key="eq2")

        if st.button("Check Logical Equivalence", key="eqchk"):
            import re
            vars1 = set(re.findall(r'\b([a-z])\b', expr1))
            vars2 = set(re.findall(r'\b([a-z])\b', expr2))
            all_vars = sorted(vars1 | vars2)
            if len(all_vars) > 5:
                st.error("Too many variables (max 5)")
            else:
                n = len(all_vars)
                equivalent = True
                diffs = []
                for i in range(1 << n):
                    vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(all_vars)}
                    r1 = eval_proposition(expr1, vals)
                    r2 = eval_proposition(expr2, vals)
                    if r1 != r2:
                        equivalent = False
                        diffs.append({v: vals[v] for v in all_vars})
                if equivalent:
                    st.success(f"✓ **LOGICALLY EQUIVALENT** — {expr1} ≡ {expr2}")
                    st.markdown("<div class='formula'>These two expressions have identical truth values for all assignments</div>", unsafe_allow_html=True)
                else:
                    st.error(f"✗ **NOT EQUIVALENT** — Counterexample found")
                    st.json(diffs[0])

        # Common equivalences table
        st.markdown("""
        <div style='margin-top:1.5rem;'>
        <div class='sec-tag'>IMPORTANT LOGICAL EQUIVALENCES</div>
        </div>""", unsafe_allow_html=True)
        equiv_laws = [
            ("De Morgan's 1", "¬(p ∧ q) ≡ ¬p ∨ ¬q"),
            ("De Morgan's 2", "¬(p ∨ q) ≡ ¬p ∧ ¬q"),
            ("Double Negation", "¬¬p ≡ p"),
            ("Implication", "p → q ≡ ¬p ∨ q"),
            ("Contrapositive", "p → q ≡ ¬q → ¬p"),
            ("Biconditional", "p ↔ q ≡ (p → q) ∧ (q → p)"),
            ("Absorption", "p ∨ (p ∧ q) ≡ p"),
            ("Distributive", "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)"),
            ("Tautology", "p ∨ ¬p ≡ T"),
            ("Contradiction", "p ∧ ¬p ≡ F"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Law</th><th style='text-align:left'>Equivalence</th></tr></thead><tbody>"
        for law, eq in equiv_laws:
            html += f"<tr><td class='T' style='text-align:left'>{law}</td><td style='color:#b8c4d4'>{eq}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='sec-tag'>PREDICATES & QUANTIFIERS</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='card'>
          <div class='formula'>∀x P(x) — For all x, P(x) is true</div>
          <div class='formula'>∃x P(x) — There exists an x such that P(x) is true</div>
          <p style='color:#8892a4;font-size:0.85rem;margin-top:0.8rem;'>
          A <b style='color:#b8c4d4;'>predicate</b> P(x) becomes a proposition when x is assigned a value from the domain.
          </p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            domain_raw = st.text_input("Domain (comma-separated)", "1, 2, 3, 4, 5", key="dom")
            predicate_type = st.selectbox("Predicate P(x)", [
                "x > 2 (greater than 2)",
                "x is even",
                "x is odd",
                "x is prime",
                "x² < 20",
                "x > 0 (positive)",
            ])
        with col2:
            st.markdown("")

        if st.button("Evaluate Quantifiers", key="quant_run"):
            domain = [int(x.strip()) for x in domain_raw.split(",") if x.strip().lstrip("-").isdigit()]
            pred_map = {
                "x > 2 (greater than 2)": lambda x: x > 2,
                "x is even": lambda x: x % 2 == 0,
                "x is odd": lambda x: x % 2 != 0,
                "x is prime": lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5)+1)),
                "x² < 20": lambda x: x*x < 20,
                "x > 0 (positive)": lambda x: x > 0,
            }
            pred = pred_map[predicate_type]
            results = {x: pred(x) for x in domain}
            for_all = all(results.values())
            exists = any(results.values())
            true_elems = [x for x, v in results.items() if v]
            false_elems = [x for x, v in results.items() if not v]

            st.markdown(f"""
            <div class='result-box'>
              <div style='margin-bottom:0.5rem;'><span style='color:#4ECCA3;'>Domain:</span> {{{', '.join(str(x) for x in domain)}}}</div>
              <div style='margin-bottom:0.5rem;'><span style='color:#4ECCA3;'>P(x) true for:</span> {fmt_set([str(x) for x in true_elems])}</div>
              <div style='margin-bottom:0.5rem;'><span style='color:#AFA9EC;'>P(x) false for:</span> {fmt_set([str(x) for x in false_elems])}</div>
              <hr style='border-color:#2a2d4a;margin:0.8rem 0;'/>
              <div style='margin-bottom:0.4rem;'><span class='{"T" if for_all else "F"}'>∀x P(x): {"TRUE ✓" if for_all else "FALSE ✗"}</span>
              {f"<span style='color:#8892a4;font-size:0.72rem;'> — counterexample: x={false_elems[0]}</span>" if not for_all and false_elems else ""}</div>
              <div><span class='{"T" if exists else "F"}'>∃x P(x): {"TRUE ✓" if exists else "FALSE ✗"}</span>
              {f"<span style='color:#8892a4;font-size:0.72rem;'> — witness: x={true_elems[0]}</span>" if exists and true_elems else ""}</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# RULES OF INFERENCE
# ═══════════════════════════════════════════════════════════
elif section == "inference":
    st.markdown("<div class='sec-tag'>// WEEK_12-13 · RULES_OF_INFERENCE</div>", unsafe_allow_html=True)
    st.markdown("## Rules of Inference")
    st.markdown("""
    <p style='color:#8892a4;'>
    A <b style='color:#b8c4d4;'>rule of inference</b> is a valid argument form that allows us to derive new propositions
    from existing ones. These are the building blocks of logical proofs.
    </p>""", unsafe_allow_html=True)

    rules = [
        {
            "name": "Modus Ponens",
            "form": "p → q\np\n∴ q",
            "formula": "(p ∧ (p → q)) → q",
            "example": "If it rains, the ground gets wet. It is raining. ∴ The ground is wet.",
            "premises": ["p", "p -> q"],
            "conclusion": "q",
        },
        {
            "name": "Modus Tollens",
            "form": "p → q\n¬q\n∴ ¬p",
            "formula": "(¬q ∧ (p → q)) → ¬p",
            "example": "If it rains, the ground gets wet. The ground is NOT wet. ∴ It did NOT rain.",
            "premises": ["!q", "p -> q"],
            "conclusion": "!p",
        },
        {
            "name": "Hypothetical Syllogism",
            "form": "p → q\nq → r\n∴ p → r",
            "formula": "((p → q) ∧ (q → r)) → (p → r)",
            "example": "If it rains, streets flood. If streets flood, traffic stops. ∴ If it rains, traffic stops.",
            "premises": ["p -> q", "q -> r"],
            "conclusion": "p -> r",
        },
        {
            "name": "Disjunctive Syllogism",
            "form": "p ∨ q\n¬p\n∴ q",
            "formula": "((p ∨ q) ∧ ¬p) → q",
            "example": "Either Ali or Sara wrote the code. Ali did not write it. ∴ Sara wrote it.",
            "premises": ["p || q", "!p"],
            "conclusion": "q",
        },
        {
            "name": "Addition",
            "form": "p\n∴ p ∨ q",
            "formula": "p → (p ∨ q)",
            "example": "It is raining. ∴ It is raining OR snowing.",
            "premises": ["p"],
            "conclusion": "p || q",
        },
        {
            "name": "Simplification",
            "form": "p ∧ q\n∴ p",
            "formula": "(p ∧ q) → p",
            "example": "It is cold AND raining. ∴ It is cold.",
            "premises": ["p && q"],
            "conclusion": "p",
        },
        {
            "name": "Conjunction",
            "form": "p\nq\n∴ p ∧ q",
            "formula": "(p ∧ q) → (p ∧ q)",
            "example": "It is cold. It is raining. ∴ It is cold AND raining.",
            "premises": ["p", "q"],
            "conclusion": "p && q",
        },
        {
            "name": "Resolution",
            "form": "p ∨ q\n¬p ∨ r\n∴ q ∨ r",
            "formula": "((p ∨ q) ∧ (¬p ∨ r)) → (q ∨ r)",
            "example": "Ali passed OR Sara passed. Ali did not pass OR Huzaifa cheered. ∴ Sara passed OR Huzaifa cheered.",
            "premises": ["p || q", "!p || r"],
            "conclusion": "q || r",
        },
    ]

    tab1, tab2 = st.tabs(["📋 All Rules", "🧪 Argument Validator"])

    with tab1:
        cols = st.columns(2)
        for idx, rule in enumerate(rules):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>{rule['name'].upper()}</div>
                  <div class='formula'>{rule['formula']}</div>
                  <pre style='color:#4ECCA3;font-family:"JetBrains Mono",monospace;font-size:0.8rem;
                  background:rgba(78,204,163,0.05);padding:0.6rem;border:1px solid #2a2d4a;
                  border-radius:2px;margin:0.6rem 0;'>{rule['form']}</pre>
                  <p style='color:#8892a4;font-size:0.8rem;'><b style='color:#b8c4d4;'>Example:</b> {rule['example']}</p>
                </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='sec-tag'>ARGUMENT_VALIDATOR</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color:#8892a4;font-size:0.85rem;'>
        Enter premises and a conclusion. The validator checks if the argument is valid
        (conclusion is a tautological consequence of the premises).
        </p>""", unsafe_allow_html=True)

        premises_raw = st.text_area(
            "Premises (one per line, use p,q,r as variables)",
            "p -> q\np",
            key="premises_input",
        )
        conclusion_raw = st.text_input("Conclusion", "q", key="conc_input")

        if st.button("Validate Argument", key="arg_val"):
            premises_list = [p.strip() for p in premises_raw.strip().split("\n") if p.strip()]
            import re
            all_vars = sorted(set(re.findall(r'\b([a-z])\b', premises_raw + " " + conclusion_raw)))

            if len(all_vars) > 5:
                st.error("Too many variables (max 5)")
            elif not all_vars:
                st.error("No variables found")
            else:
                n = len(all_vars)
                valid = True
                counterexample = None
                for i in range(1 << n):
                    vals = {v: bool(i & (1 << (n - 1 - j))) for j, v in enumerate(all_vars)}
                    all_premises_true = all(eval_proposition(p, vals) for p in premises_list)
                    if all_premises_true:
                        conclusion_true = eval_proposition(conclusion_raw, vals)
                        if not conclusion_true:
                            valid = False
                            counterexample = vals
                            break

                if valid:
                    st.success("✓ VALID ARGUMENT — The conclusion follows logically from the premises")
                    # Try to identify the rule used
                    combined = " ∧ ".join(f"({p})" for p in premises_list)
                    st.markdown(f"<div class='formula'>({combined}) → ({conclusion_raw}) is a tautology</div>", unsafe_allow_html=True)
                else:
                    st.error("✗ INVALID ARGUMENT — Counterexample found")
                    st.json(counterexample)


# ═══════════════════════════════════════════════════════════
# PROOF METHODS
# ═══════════════════════════════════════════════════════════
elif section == "proofs":
    st.markdown("<div class='sec-tag'>// WEEK_14-15 · PROOF_METHODS</div>", unsafe_allow_html=True)
    st.markdown("## Methods of Proving")

    proof_methods = {
        "Direct Proof": {
            "description": "Assume the hypothesis p is true, and use logical steps to show q must be true.",
            "structure": "Assume p.\nStep 1: ...\nStep 2: ...\n∴ q  □",
            "example_claim": "If n is even, then n² is even.",
            "example_proof": """Assume n is even.
→ n = 2k for some integer k  [definition of even]
→ n² = (2k)² = 4k² = 2(2k²)  [algebra]
→ n² = 2m where m = 2k²  [m is an integer]
→ n² is even  [definition of even]  □""",
        },
        "Proof by Contradiction": {
            "description": "Assume p ∧ ¬q is true. Derive a contradiction, proving p → q.",
            "structure": "Assume p and ¬q.\nDerive a contradiction C (something both true and false).\n∴ Our assumption was wrong, so p → q  □",
            "example_claim": "√2 is irrational.",
            "example_proof": """Assume √2 is rational (negation).
→ √2 = a/b where gcd(a,b)=1 (fully reduced)
→ 2 = a²/b²  →  a² = 2b²
→ a² is even  →  a is even
→ a = 2k for some integer k
→ a² = 4k² = 2b²  →  b² = 2k²
→ b² is even  →  b is even
→ Both a and b are even → gcd(a,b) ≥ 2
→ CONTRADICTION with gcd(a,b) = 1  □
∴ √2 is irrational""",
        },
        "Proof by Contrapositive": {
            "description": "To prove p → q, instead prove its contrapositive ¬q → ¬p.",
            "structure": "Assume ¬q.\nStep 1...\n∴ ¬p  □",
            "example_claim": "If n² is odd, then n is odd.",
            "example_proof": """We prove the contrapositive: if n is even, then n² is even.

Assume n is even.
→ n = 2k for some integer k
→ n² = 4k² = 2(2k²)
→ n² is even  □

Since ¬q → ¬p is proven, p → q holds by contrapositive.""",
        },
        "Proof by Cases": {
            "description": "Divide the domain into cases and prove the claim for each case.",
            "structure": "Case 1: ..., Case 2: ..., ...\nEach case leads to conclusion.\n∴ Conclusion holds for all cases  □",
            "example_claim": "For any integer n, n² + n is even.",
            "example_proof": """Case 1: n is even.
  n = 2k  →  n² + n = 4k² + 2k = 2(2k² + k)  →  even ✓

Case 2: n is odd.
  n = 2k+1  →  n² + n = (2k+1)² + (2k+1)
  = 4k²+4k+1+2k+1 = 4k²+6k+2 = 2(2k²+3k+1)  →  even ✓

In both cases n² + n is even.  □""",
        },
    }

    for method, content in proof_methods.items():
        with st.expander(f"📘 {method}", expanded=(method == "Direct Proof")):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>STRATEGY</div>
                  <p style='color:#8892a4;font-size:0.85rem;'>{content['description']}</p>
                  <div class='sec-tag' style='margin-top:0.8rem;'>STRUCTURE</div>
                  <pre style='color:#4ECCA3;font-family:"JetBrains Mono",monospace;font-size:0.78rem;
                  background:rgba(78,204,163,0.05);padding:0.7rem;border:1px solid #2a2d4a;border-radius:2px;'>{content['structure']}</pre>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card'>
                  <div class='sec-tag'>WORKED EXAMPLE</div>
                  <div style='color:#e8eaf0;font-weight:600;margin-bottom:0.5rem;font-size:0.9rem;'>Claim: {content['example_claim']}</div>
                  <pre style='color:#b8c4d4;font-family:"JetBrains Mono",monospace;font-size:0.75rem;
                  background:#0a0a14;padding:0.7rem;border:1px solid #2a2d4a;border-radius:2px;
                  white-space:pre-wrap;'>{content['example_proof']}</pre>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# MATHEMATICAL INDUCTION
# ═══════════════════════════════════════════════════════════
elif section == "induction":
    st.markdown("<div class='sec-tag'>// WEEK_16 · MATHEMATICAL_INDUCTION</div>", unsafe_allow_html=True)
    st.markdown("## Mathematical Induction")
    st.markdown("""
    <div class='card'>
      <div class='formula'>Base Case: P(1) is true</div>
      <div class='formula'>Inductive Step: P(k) true → P(k+1) true</div>
      <div class='formula'>Conclusion: P(n) is true for all n ≥ 1</div>
      <p style='color:#8892a4;font-size:0.85rem;margin-top:0.8rem;'>
      Mathematical induction is like a chain of dominoes: prove the first falls, and prove each one
      knocks the next. Then all of them fall.
      </p>
    </div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🧮 Formula Verifier", "📋 Classic Proofs"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            formula_type = st.selectbox("Choose formula to verify", [
                "sum_natural — Σi = n(n+1)/2",
                "sum_squares — Σi² = n(n+1)(2n+1)/6",
                "geometric — Σ2^i = 2^(n+1)-1",
                "power_of_2 — 2^n divisible by 2",
            ])
            n_val = st.number_input("Check for n =", min_value=1, max_value=30, value=5, key="ind_n")
        with col2:
            ft = formula_type.split(" — ")[0]

        if st.button("Verify by Induction", key="ind_run"):
            result = induction_checker(ft, int(n_val))
            st.markdown(f"""
            <div class='result-box'>
            <pre style='white-space:pre-wrap;margin:0;font-family:"JetBrains Mono",monospace;font-size:0.82rem;'>{result}</pre>
            </div>""", unsafe_allow_html=True)

        # Interactive: show step-by-step for sum 1..n
        st.markdown("---")
        st.markdown("#### Step-by-step: Prove Σi = n(n+1)/2")
        n_demo = st.slider("n", 1, 15, 4, key="ind_demo")
        actual = sum(range(1, n_demo + 1))
        formula_val = n_demo * (n_demo + 1) // 2
        steps_html = ""
        running = 0
        for i in range(1, n_demo + 1):
            running += i
            steps_html += f"<div style='color:#8892a4;'> + {i} = {running}</div>"
        st.markdown(f"""
        <div class='result-box'>
          <div style='color:#4ECCA3;margin-bottom:0.5rem;'>Base case (n=1): 1 = 1·2/2 = 1 ✓</div>
          <div style='color:#b8c4d4;margin-bottom:0.4rem;'>Running sum 1 to {n_demo}:</div>
          {steps_html}
          <hr style='border-color:#2a2d4a;margin:0.6rem 0;'/>
          <div style='color:#4ECCA3;font-weight:600;'>Σ(1..{n_demo}) = {actual}</div>
          <div style='color:#b8c4d4;'>Formula: {n_demo}·{n_demo+1}/2 = {formula_val}</div>
          <div style='color:{"#4ECCA3" if actual == formula_val else "#ff6b6b"};margin-top:0.3rem;'>
          {"✓ Match! Induction holds." if actual == formula_val else "✗ Mismatch!"}
          </div>
        </div>""", unsafe_allow_html=True)

    with tab2:
        proofs = [
            {
                "title": "Sum of First n Natural Numbers",
                "claim": "For all n ≥ 1: 1 + 2 + 3 + ... + n = n(n+1)/2",
                "base": "P(1): LHS = 1, RHS = 1·2/2 = 1. ✓",
                "hyp": "P(k): Assume 1 + 2 + ... + k = k(k+1)/2",
                "step": "P(k+1): 1 + 2 + ... + k + (k+1)\n= k(k+1)/2 + (k+1)\n= (k+1)[k/2 + 1]\n= (k+1)(k+2)/2 ✓",
            },
            {
                "title": "Sum of First n Odd Numbers",
                "claim": "For all n ≥ 1: 1 + 3 + 5 + ... + (2n-1) = n²",
                "base": "P(1): LHS = 1, RHS = 1² = 1. ✓",
                "hyp": "P(k): Assume 1 + 3 + ... + (2k-1) = k²",
                "step": "P(k+1): k² + (2k+1) = k² + 2k + 1 = (k+1)² ✓",
            },
            {
                "title": "Power of 2 Inequality",
                "claim": "For all n ≥ 1: 2ⁿ > n",
                "base": "P(1): 2¹ = 2 > 1. ✓",
                "hyp": "P(k): Assume 2ᵏ > k",
                "step": "P(k+1): 2^(k+1) = 2·2ᵏ > 2k (by I.H.) ≥ k+1 for k≥1 ✓",
            },
        ]
        for proof in proofs:
            with st.expander(f"📗 {proof['title']}"):
                st.markdown(f"""
                <div class='card'>
                  <div style='color:#e8eaf0;font-weight:600;margin-bottom:0.8rem;'>{proof['claim']}</div>
                  <div style='margin-bottom:0.6rem;'><span style='color:#4ECCA3;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>BASE CASE:</span><br>
                  <span style='color:#b8c4d4;font-size:0.85rem;'>{proof['base']}</span></div>
                  <div style='margin-bottom:0.6rem;'><span style='color:#AFA9EC;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>INDUCTIVE HYPOTHESIS:</span><br>
                  <span style='color:#b8c4d4;font-size:0.85rem;'>{proof['hyp']}</span></div>
                  <div><span style='color:#ff9f4a;font-family:"JetBrains Mono",monospace;font-size:0.75rem;'>INDUCTIVE STEP:</span><br>
                  <pre style='color:#b8c4d4;font-size:0.83rem;background:#0a0a14;padding:0.6rem;border:1px solid #2a2d4a;
                  border-radius:2px;white-space:pre-wrap;margin-top:0.3rem;'>{proof['step']}</pre></div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# SEQUENCES & SUMMATIONS
# ═══════════════════════════════════════════════════════════
elif section == "sequences":
    st.markdown("<div class='sec-tag'>// WEEK_08 · SEQUENCES_AND_SUMMATIONS</div>", unsafe_allow_html=True)
    st.markdown("## Sequences & Summations")

    tab1, tab2 = st.tabs(["📊 Sequence Generator", "∑ Summation Formulas"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            seq_type = st.selectbox("Sequence type", ["arithmetic", "geometric", "fibonacci"])
            n_terms = st.number_input("Number of terms (n)", min_value=1, max_value=25, value=8, key="seq_n")
        with col2:
            if seq_type == "arithmetic":
                a0 = st.number_input("First term a₁", value=1, key="ar_a")
                d = st.number_input("Common difference d", value=3, key="ar_d")
            elif seq_type == "geometric":
                a0 = st.number_input("First term a₁", value=1, key="ge_a")
                r = st.number_input("Common ratio r", value=2, key="ge_r")

        if st.button("Generate Sequence", key="seq_run"):
            n = int(n_terms)
            if seq_type == "arithmetic":
                terms = [int(a0) + i * int(d) for i in range(n)]
                s = sum(terms)
                formula = f"S_n = n/2·(2a+(n-1)d) = {n}/2·(2·{int(a0)}+{n-1}·{int(d)}) = {s}"
                nth = f"a_n = {int(a0)} + (n-1)·{int(d)}"
            elif seq_type == "geometric":
                terms = [int(a0) * (int(r) ** i) for i in range(n)]
                s = sum(terms)
                formula = f"S_n = a(rⁿ-1)/(r-1) = {int(a0)}·({int(r)}^{n}-1)/({int(r)}-1) = {s}" if int(r) != 1 else f"S_n = n·a = {n}·{int(a0)} = {s}"
                nth = f"a_n = {int(a0)}·{int(r)}^(n-1)"
            else:
                fibs = [1, 1]
                while len(fibs) < n:
                    fibs.append(fibs[-1] + fibs[-2])
                terms = fibs[:n]
                s = sum(terms)
                formula = f"S_{n} = F_{n+2} - 1 = {fibs[n+1] if n+1 < len(fibs) else '...'} - 1" if n < len(fibs) else f"Sum = {s}"
                nth = "F_n = F_(n-1) + F_(n-2)"

            st.markdown(f"<div class='formula'>{nth}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='result-box'>
              <div style='color:#4ECCA3;margin-bottom:0.4rem;'>Terms:</div>
              <div style='color:#b8c4d4;margin-bottom:0.8rem;word-break:break-all;'>{', '.join(str(t) for t in terms)}</div>
              <div style='color:#4ECCA3;margin-bottom:0.4rem;'>Sum:</div>
              <div style='color:#e8eaf0;font-size:1rem;font-weight:700;margin-bottom:0.4rem;'>{s}</div>
              <div style='color:#8892a4;font-size:0.78rem;'>{formula}</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        formulas = [
            ("Sum of 1 to n", "Σᵢ₌₁ⁿ i", "n(n+1)/2", "10 → 55"),
            ("Sum of squares", "Σᵢ₌₁ⁿ i²", "n(n+1)(2n+1)/6", "5 → 55"),
            ("Sum of cubes", "Σᵢ₌₁ⁿ i³", "[n(n+1)/2]²", "4 → 100"),
            ("Sum of odd numbers", "Σᵢ₌₁ⁿ (2i-1)", "n²", "5 → 25"),
            ("Geometric series", "Σᵢ₌₀ⁿ rⁱ", "(r^(n+1) - 1)/(r-1)", "r=2,n=4 → 31"),
            ("Infinite geometric", "Σᵢ₌₀^∞ rⁱ  |r|<1", "1/(1-r)", "r=0.5 → 2"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th>Name</th><th>Notation</th><th>Formula</th><th>Example</th></tr></thead><tbody>"
        for name, notation, formula, example in formulas:
            html += f"<tr><td class='T' style='text-align:left'>{name}</td><td style='color:#b8c4d4'>{notation}</td><td style='color:#4ECCA3'>{formula}</td><td style='color:#8892a4'>{example}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

        # Interactive: compute any summation
        st.markdown("---")
        st.markdown("#### Compute Σᵢ₌₁ⁿ iᵏ")
        col1, col2 = st.columns(2)
        with col1:
            sum_n = st.number_input("n (upper limit)", 1, 100, 10, key="sumn")
        with col2:
            sum_k = st.number_input("k (power)", 0, 5, 1, key="sumk")
        if st.button("Compute", key="sum_run"):
            result = sum(i ** int(sum_k) for i in range(1, int(sum_n) + 1))
            st.markdown(f"<div class='formula'>Σᵢ₌₁^{int(sum_n)} i^{int(sum_k)} = {result}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# COMBINATORICS
# ═══════════════════════════════════════════════════════════
elif section == "combinatorics":
    st.markdown("<div class='sec-tag'>// COMBINATORICS</div>", unsafe_allow_html=True)
    st.markdown("## Combinatorics & Counting")
    st.markdown("""
    <p style='color:#8892a4;'>Counting is the foundation of algorithm analysis and probability theory.</p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["P(n,r) & C(n,r)", "🕊️ Pigeonhole", "📋 Counting Principles"])

    with tab1:
        st.markdown("<div class='formula'>P(n,r) = n! / (n-r)! &nbsp;&nbsp;&nbsp; C(n,r) = n! / (r!(n-r)!)</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            n_c = st.number_input("n (total items)", min_value=0, max_value=20, value=10, key="cn")
        with col2:
            r_c = st.number_input("r (chosen items)", min_value=0, max_value=20, value=3, key="cr")

        if st.button("Calculate", key="comb_run"):
            n_v, r_v = int(n_c), int(r_c)
            if r_v > n_v:
                st.error("r cannot exceed n")
            else:
                perm_val = perm(n_v, r_v)
                comb_val = comb(n_v, r_v)
                nf = factorial(n_v)
                rf = factorial(r_v)
                nrf = factorial(n_v - r_v)
                st.markdown(f"""
                <div class='result-box'>
                  <div style='margin-bottom:0.5rem;'><span style='color:#4ECCA3;'>n! = {n_v}! = </span>{nf}</div>
                  <div style='margin-bottom:0.5rem;'><span style='color:#AFA9EC;'>r! = {r_v}! = </span>{rf}</div>
                  <div style='margin-bottom:0.5rem;'><span style='color:#8892a4;'>(n-r)! = {n_v-r_v}! = </span>{nrf}</div>
                  <hr style='border-color:#2a2d4a;margin:0.6rem 0;'/>
                  <div style='font-size:1.1rem;margin-bottom:0.5rem;'>
                    <span style='color:#4ECCA3;font-weight:700;'>P({n_v},{r_v}) = </span>
                    <span style='color:#e8eaf0;font-size:1.3rem;font-weight:800;'>{perm_val}</span>
                    <span style='color:#4a5568;font-size:0.75rem;'>&nbsp;ordered arrangements</span>
                  </div>
                  <div style='font-size:1.1rem;'>
                    <span style='color:#AFA9EC;font-weight:700;'>C({n_v},{r_v}) = </span>
                    <span style='color:#e8eaf0;font-size:1.3rem;font-weight:800;'>{comb_val}</span>
                    <span style='color:#4a5568;font-size:0.75rem;'>&nbsp;unordered selections</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>PIGEONHOLE PRINCIPLE</div>
          <div class='formula'>If n+1 objects placed in n boxes, at least one box contains ≥ 2 objects</div>
          <p style='color:#8892a4;font-size:0.85rem;margin-top:0.8rem;'>
          <b>Generalized:</b> If N objects placed in k boxes, then some box contains ≥ ⌈N/k⌉ objects.
          </p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            n_obj = st.number_input("Number of objects (N)", min_value=1, max_value=1000, value=13, key="ph_n")
        with col2:
            k_box = st.number_input("Number of boxes (k)", min_value=1, max_value=100, value=12, key="ph_k")

        if st.button("Apply Pigeonhole", key="ph_run"):
            import math
            N, k = int(n_obj), int(k_box)
            guaranteed = math.ceil(N / k)
            st.markdown(f"""
            <div class='result-box'>
              <div style='margin-bottom:0.5rem;'>{N} objects into {k} boxes</div>
              <div style='color:#4ECCA3;font-size:1.1rem;font-weight:700;'>At least one box contains ≥ ⌈{N}/{k}⌉ = <b>{guaranteed}</b> objects</div>
              <div style='color:#8892a4;margin-top:0.5rem;font-size:0.8rem;'>
              {"Example: With 13 cards from a standard deck into 12 months, at least 2 cards share a birth month." if N==13 and k==12 else
               f"With {N} items in {k} containers, by pigeonhole at least {guaranteed} items share a container."}
              </div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class='sec-tag'>COUNTING PRINCIPLES</div>
        <h4 style='color:#e8eaf0;margin-bottom:1rem;'>Fundamental Rules</h4>
        """, unsafe_allow_html=True)
        principles = [
            ("Product Rule", "If task 1 has m ways and task 2 has n ways (independently), then both = m×n ways", "Choose shirt (5 types) AND pants (3 types) = 5×3 = 15 outfits"),
            ("Sum Rule", "If task 1 has m ways OR task 2 has n ways (mutually exclusive), then = m+n ways", "Choose from 5 shirts OR 3 hats = 8 choices"),
            ("Inclusion-Exclusion", "|A ∪ B| = |A| + |B| − |A ∩ B|", "|{even}∪{prime}| = |{even}|+|{prime}|−|{even∩prime}|"),
            ("Permutation", "P(n,r) = ordered selection of r from n", "Top 3 finishers from 8 runners = P(8,3) = 336"),
            ("Combination", "C(n,r) = unordered selection of r from n", "Choose 3 from 8 students = C(8,3) = 56"),
            ("Stars and Bars", "C(n+r-1, r) ways to place r indistinct balls in n bins", "Distribute 5 cookies to 3 kids = C(7,5) = 21"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Principle</th><th style='text-align:left'>Rule</th><th style='text-align:left'>Example</th></tr></thead><tbody>"
        for principle, rule, example in principles:
            html += f"<tr><td class='T' style='text-align:left;white-space:nowrap'>{principle}</td><td style='color:#b8c4d4;text-align:left'>{rule}</td><td style='color:#8892a4;font-size:0.75rem;text-align:left'>{example}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# GRAPH THEORY
# ═══════════════════════════════════════════════════════════
elif section == "graphs":
    st.markdown("<div class='sec-tag'>// GRAPH_THEORY · BASICS</div>", unsafe_allow_html=True)
    st.markdown("## Graph Theory")
    st.markdown("""
    <p style='color:#8892a4;'>
    A <b style='color:#b8c4d4;'>graph</b> G = (V, E) consists of a set of vertices V and edges E.
    Graph theory models networks, relations, and computational structures.
    </p>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 Graph Analyzer", "📚 Graph Concepts"])

    with tab1:
        n_g = st.slider("Number of vertices (n)", 2, 7, 4, key="gn")
        st.markdown(f"<div class='formula'>G = (V, E) where V = {{v₀, v₁, ..., v_{n_g-1}}}</div>", unsafe_allow_html=True)
        st.markdown("**Adjacency Matrix (0=no edge, 1=edge):**")

        adj_matrix = []
        for i in range(n_g):
            cols = st.columns(n_g)
            row = []
            for j in range(n_g):
                default = 1 if abs(i - j) == 1 else 0
                val = cols[j].selectbox(f"({i},{j})", [0, 1], index=default, key=f"g_{i}_{j}")
                row.append(val)
            adj_matrix.append(row)

        if st.button("Analyze Graph", key="graph_run"):
            # Symmetrize
            for i in range(n_g):
                for j in range(n_g):
                    if adj_matrix[i][j]:
                        adj_matrix[j][i] = 1

            info = graph_analyze(adj_matrix)
            degrees = info["degrees"]

            # Check for simple graph
            self_loops = any(adj_matrix[i][i] for i in range(n_g))

            html = f"""
            <div style='margin-bottom:0.4rem;'><span style='color:#4ECCA3;'>Vertices |V| = </span>{info['vertices']}</div>
            <div style='margin-bottom:0.4rem;'><span style='color:#4ECCA3;'>Edges |E| = </span>{info['edges']}</div>
            <div style='margin-bottom:0.4rem;'><span style='color:#4ECCA3;'>Self-loops = </span>{'Yes' if self_loops else 'No'}</div>
            <div style='margin-bottom:0.8rem;'><span style='color:{"#4ECCA3" if info["connected"] else "#ff6b6b"};'>
              Connectivity: {'CONNECTED ✓' if info['connected'] else 'DISCONNECTED ✗'}
            </span></div>
            <div style='margin-bottom:0.4rem;color:#b8c4d4;'>Degree sequence: {sorted(degrees, reverse=True)}</div>
            <div style='margin-bottom:0.4rem;'><span style='color:#AFA9EC;'>Handshaking Lemma: Σdeg = </span>{info['total_degree']} = 2|E| = {2*info['edges']} ✓</div>
            <div style='margin-bottom:0.8rem;'><span style='color:#ff9f4a;'>Eulerian: </span>{info['eulerian']}</div>
            """
            for i, d in enumerate(degrees):
                parity = "even" if d % 2 == 0 else "odd"
                color = "#4ECCA3" if d % 2 == 0 else "#ff9f4a"
                html += f"<div style='color:#8892a4;'>deg(v{i}) = <span style='color:{color};'>{d} [{parity}]</span></div>"

            st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)

    with tab2:
        concepts = [
            ("Vertex (Node)", "A fundamental point v ∈ V in graph G=(V,E)", "People in a social network"),
            ("Edge", "A connection {u,v} ∈ E between two vertices", "Friendships in a social network"),
            ("Degree deg(v)", "Number of edges incident to vertex v", "Number of friends a person has"),
            ("Path", "A sequence of vertices connected by edges (no repeats)", "Route from city A to city B"),
            ("Cycle", "A path that starts and ends at the same vertex", "A circular route"),
            ("Connected Graph", "There exists a path between every pair of vertices", "All cities reachable from any city"),
            ("Tree", "A connected acyclic graph with |V|-1 edges", "File system directory structure"),
            ("Eulerian Path", "A path that visits every EDGE exactly once", "Königsberg bridge problem"),
            ("Eulerian Circuit", "An Eulerian path that starts and ends at same vertex", "Requires all vertices to have even degree"),
            ("Hamiltonian Path", "A path that visits every VERTEX exactly once", "Traveling salesman problem"),
            ("Complete Graph Kₙ", "Every pair of vertices is connected by an edge", "All-pairs communication network"),
            ("Bipartite Graph", "Vertices split into 2 sets, edges only cross between them", "Job assignment (workers ↔ tasks)"),
            ("Handshaking Lemma", "Σ deg(v) = 2|E| — sum of degrees = twice edge count", "Total handshakes = 2 × pairs"),
            ("Isomorphism", "A structure-preserving bijection φ: G → H", "Two different drawings of same graph"),
        ]
        html = "<table class='tt' style='width:100%;'><thead><tr><th style='text-align:left'>Concept</th><th style='text-align:left'>Definition</th><th style='text-align:left'>Example</th></tr></thead><tbody>"
        for concept, defn, example in concepts:
            html += f"<tr><td class='T' style='text-align:left;white-space:nowrap'>{concept}</td><td style='color:#b8c4d4;text-align:left'>{defn}</td><td style='color:#8892a4;font-size:0.75rem;text-align:left'>{example}</td></tr>"
        html += "</tbody></table>"
        st.markdown(f"<div class='result-box'>{html}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# NLP SOLVER
# ═══════════════════════════════════════════════════════════
elif section == "ai":
    st.markdown("<div class='sec-tag'>// AI_POWERED · NATURAL_LANGUAGE_SOLVER</div>", unsafe_allow_html=True)
    st.markdown("## AI Discrete Math Tools")

    # ── Tabs ────────────────────────────────────────────────
    tab_chat, tab_notation = st.tabs(["💬  Problem Solver (Chatbot)", "🔣  English → Notation Converter"])

    # ── TAB 1 : Chatbot ─────────────────────────────────────
    with tab_chat:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>DISCRETE_MATH_CHATBOT</div>
          <p style='color:#8892a4;font-size:0.85rem;margin-top:0.4rem;'>
          Type any discrete mathematics problem <b style='color:#b8c4d4;'>in plain English</b> and the AI will:
          interpret it, formulate it mathematically, solve it step-by-step, and give a clear final answer.
          </p>
        </div>""", unsafe_allow_html=True)

        user_problem = st.text_area(
            "Your problem in plain English",
            placeholder="""Examples:
• "How many ways can we choose 3 students from a class of 10 if order doesn't matter?"
• "If all cats are animals, and Whiskers is a cat, what can we conclude?"
• "Prove that the sum of two even numbers is always even."
• "Find the equivalence classes of R = {(1,1),(2,2),(3,3),(1,2),(2,1)} on {1,2,3}"
• "Is the argument valid: All men are mortal. Socrates is a man. Therefore Socrates is mortal."
• "Show that if n squared is even then n is even using proof by contrapositive"
""",
            height=180,
            key="nlp_input",
        )

        if st.button("🔍 Solve with AI", key="nlp_run"):
            if not user_problem.strip():
                st.error("Please enter a problem.")
            else:
                with st.spinner("Thinking…"):
                    answer = call_groq_nlp(user_problem)
                st.markdown(f"""
                <div class='result-box' style='line-height:1.8;'>
                {answer.replace(chr(10), '<br>')}
                </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Example Questions to Try")
        examples_nlp = [
            "How many 5-letter passwords can be made from 26 letters if no letter repeats?",
            "Is the relation R = {(1,1),(2,2),(3,3),(1,2),(2,1),(2,3),(3,2),(1,3),(3,1)} an equivalence relation?",
            "Using modus ponens: If it rains, the match is cancelled. It is raining. What follows?",
            "Prove by contradiction that there are infinitely many prime numbers.",
            "Find all ways to arrange the letters in the word MATH.",
            "Use mathematical induction to prove that 1+2+3+...+n = n(n+1)/2",
            "What is the reflexive closure of R = {(1,2),(2,3)} on the set {1,2,3}?",
            "If A = {1,2,3,4} and B = {3,4,5,6}, find A union B, A intersection B, and A minus B.",
        ]
        cols = st.columns(2)
        for i, ex in enumerate(examples_nlp):
            with cols[i % 2]:
                st.markdown(f"""
                <div style='background:#0d0d22;border:1px solid #2a2d4a;padding:0.6rem 0.9rem;
                border-radius:2px;margin-bottom:0.5rem;font-size:0.78rem;color:#8892a4;
                font-family:"JetBrains Mono",monospace;border-left:2px solid #4ECCA3;'>
                {ex}
                </div>""", unsafe_allow_html=True)

    # ── TAB 2 : English → Notation Converter ────────────────
    with tab_notation:
        st.markdown("""
        <div class='card'>
          <div class='sec-tag'>ENGLISH → DISCRETE NOTATION</div>
          <p style='color:#8892a4;font-size:0.85rem;margin-top:0.4rem;'>
          Enter one or more English statements. The AI will identify the atomic propositions,
          assign variables <b style='color:#4ECCA3;'>(p, q, r, …)</b>, and express the statement
          in formal discrete math notation such as <b style='color:#4ECCA3;'>p → q</b>,
          <b style='color:#4ECCA3;'>p ∧ q</b>, <b style='color:#4ECCA3;'>¬p ∨ q</b>, etc.
          </p>
          <div class='formula' style='margin-top:0.6rem;'>
          "If you have a current password, then you can log onto the network."
          &nbsp;→&nbsp; p → q
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style='font-family:"JetBrains Mono",monospace;font-size:0.68rem;color:#4ECCA3;
        letter-spacing:0.1em;margin-bottom:0.5rem;'>ENTER ENGLISH STATEMENT(S)</div>""",
        unsafe_allow_html=True)

        notation_input = st.text_area(
            label="English statement",
            label_visibility="collapsed",
            placeholder="""Enter one or multiple statements, e.g.:

"If you have a current password, then you can log onto the network."
"You have a current password."
"Therefore, you can log onto the network."

Or a single compound statement like:
"Either it is raining or it is sunny, but it is not sunny."
""",
            height=160,
            key="notation_input",
        )

        ex_col1, ex_col2 = st.columns(2)
        notation_examples = [
            ("Simple implication", "If it is raining, then the ground is wet."),
            ("Conjunction", "It is raining and it is cold."),
            ("Disjunction", "Either the alarm is faulty or there is a fire."),
            ("Negation", "It is not the case that the door is locked."),
            ("Biconditional", "You pass the exam if and only if you score above 60."),
            ("Modus Ponens argument", "If all cats are animals, and Whiskers is a cat, then Whiskers is an animal."),
            ("Contrapositive", "If the network is down, then you cannot send emails."),
            ("Compound", "If it is raining or snowing, then the road is slippery."),
        ]
        st.markdown("<div style='font-family:\"JetBrains Mono\",monospace;font-size:0.68rem;color:#4ECCA3;letter-spacing:0.1em;margin-bottom:0.4rem;'>QUICK EXAMPLES — CLICK TO COPY</div>", unsafe_allow_html=True)
        ecols = st.columns(2)
        for idx, (label, example_text) in enumerate(notation_examples):
            with ecols[idx % 2]:
                st.markdown(f"""
                <div style='background:#0d0d22;border:1px solid #2a2d4a;padding:0.5rem 0.8rem;
                border-radius:2px;margin-bottom:0.4rem;border-left:2px solid #2a8a6b;'>
                  <div style='font-family:"JetBrains Mono",monospace;font-size:0.62rem;
                  color:#4ECCA3;letter-spacing:0.08em;margin-bottom:0.2rem;'>{label}</div>
                  <div style='font-size:0.78rem;color:#b8c4d4;font-style:italic;'>"{example_text}"</div>
                </div>""", unsafe_allow_html=True)

        if st.button("🔣 Convert to Notation", key="notation_run"):
            if not notation_input.strip():
                st.error("Please enter an English statement.")
            else:
                with st.spinner("Converting…"):
                    result = call_notation_converter(notation_input.strip())

                if not result["success"]:
                    st.error(f"Conversion error: {result.get('error', 'Unknown error')}")
                    if result.get("raw"):
                        st.code(result["raw"], language="text")
                else:
                    data = result["data"]
                    vars_data = data.get("variables", [])
                    notation = data.get("notation", "")
                    arg_form = data.get("argument_form", "")
                    form_name = data.get("form_name", "")
                    explanation = data.get("explanation", "")
                    truth_cond = data.get("truth_condition", "")

                    # ── Variable assignments
                    if vars_data:
                        vars_html = "".join(
                            f"<div style='display:flex;align-items:center;gap:0.8rem;padding:0.35rem 0;"
                            f"border-bottom:1px solid rgba(42,45,74,0.5);'>"
                            f"<span style='font-family:\"JetBrains Mono\",monospace;font-size:1rem;"
                            f"color:#4ECCA3;font-weight:700;min-width:24px;'>{v['symbol']}</span>"
                            f"<span style='color:#4a5568;'>≔</span>"
                            f"<span style='color:#b8c4d4;font-size:0.83rem;'>{v['meaning']}</span>"
                            f"</div>"
                            for v in vars_data
                        )
                        st.markdown(f"""
                        <div style='margin-bottom:1rem;'>
                          <div style='font-family:"JetBrains Mono",monospace;font-size:0.68rem;
                          color:#4ECCA3;letter-spacing:0.1em;margin-bottom:0.5rem;'>VARIABLE ASSIGNMENTS</div>
                          <div style='background:#0d0d22;border:1px solid #2a2d4a;padding:0.7rem 1rem;
                          border-radius:3px;border-left:3px solid #4ECCA3;'>
                          {vars_html}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    # ── Main notation result
                    st.markdown(f"""
                    <div style='margin-bottom:1rem;'>
                      <div style='font-family:"JetBrains Mono",monospace;font-size:0.68rem;
                      color:#4ECCA3;letter-spacing:0.1em;margin-bottom:0.5rem;'>FORMAL NOTATION</div>
                      <div style='background:#0a0a14;border:1px solid #2a8a6b;padding:1.1rem 1.4rem;
                      border-radius:3px;text-align:center;'>
                        <span style='font-family:"JetBrains Mono",monospace;font-size:1.6rem;
                        font-weight:700;color:#4ECCA3;letter-spacing:0.06em;'>{notation}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # ── Argument form (if present)
                    if arg_form and arg_form.strip():
                        arg_html = arg_form.replace("\\n", "<br>").replace("\n", "<br>")
                        form_label = f" — {form_name}" if form_name else ""
                        st.markdown(f"""
                        <div style='margin-bottom:1rem;'>
                          <div style='font-family:"JetBrains Mono",monospace;font-size:0.68rem;
                          color:#AFA9EC;letter-spacing:0.1em;margin-bottom:0.5rem;'>
                          ARGUMENT FORM{form_label.upper()}</div>
                          <div style='background:#0a0a14;border:1px solid #534AB7;padding:0.9rem 1.2rem;
                          border-radius:3px;font-family:"JetBrains Mono",monospace;
                          font-size:1rem;color:#AFA9EC;line-height:2;'>
                          {arg_html}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    # ── Explanation + truth condition
                    details_html = ""
                    if explanation:
                        details_html += f"<div style='margin-bottom:0.5rem;'><span style='color:#4ECCA3;font-size:0.68rem;letter-spacing:0.08em;font-family:\"JetBrains Mono\",monospace;'>EXPLANATION</span><br><span style='color:#b8c4d4;'>{explanation}</span></div>"
                    if truth_cond:
                        details_html += f"<div><span style='color:#4ECCA3;font-size:0.68rem;letter-spacing:0.08em;font-family:\"JetBrains Mono\",monospace;'>TRUTH CONDITION</span><br><span style='color:#8892a4;'>{truth_cond}</span></div>"
                    if details_html:
                        st.markdown(f"""
                        <div style='background:#0d0d22;border:1px solid #2a2d4a;padding:0.9rem 1.1rem;
                        border-radius:3px;font-size:0.83rem;line-height:1.8;'>
                        {details_html}
                        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# STUDY HUB
# ═══════════════════════════════════════════════════════════
elif section == "studyhub":

    # ── Data definitions ────────────────────────────────────
    STUDY_TOPICS = [
        ("sets",          "Set Theory",             "∩",  "W2-3"),
        ("relations",     "Relations",              "↔",  "W4-8"),
        ("logic",         "Propositional Logic",    "∧",  "W9-11"),
        ("inference",     "Rules of Inference",     "∴",  "W12-13"),
        ("proofs",        "Proof Methods",          "□",  "W14-15"),
        ("induction",     "Mathematical Induction", "Σ",  "W16"),
        ("sequences",     "Sequences & Summations", "∿",  "W8"),
        ("combinatorics", "Combinatorics",          "⊕",  ""),
        ("graphs",        "Graph Theory",           "◇",  ""),
    ]

    ROADMAP_GROUPS = [
        ("FOUNDATIONS",       ["sets", "combinatorics"]),
        ("RELATIONSHIPS",     ["relations", "sequences"]),
        ("LOGIC & REASONING", ["logic", "inference"]),
        ("PROOF TECHNIQUES",  ["proofs", "induction"]),
        ("ADVANCED",          ["graphs"]),
    ]

    TOPIC_OVERVIEWS = {
        "sets":          "A set is an unordered collection of distinct objects. Sets are the foundation of all mathematics and computer science.",
        "relations":     "A relation describes how elements of one set are associated with elements of another. Relations model real-world connections and are fundamental to databases and graph theory.",
        "logic":         "Propositional logic studies the truth values of statements and the rules that combine them. It is the basis of all mathematical reasoning.",
        "inference":     "Rules of inference are templates for building valid logical arguments — guaranteeing that if premises are true, the conclusion must also be true.",
        "proofs":        "A mathematical proof is a rigorous argument establishing the truth of a statement. Mastering proof techniques is the core skill of discrete mathematics.",
        "induction":     "Mathematical induction is a powerful technique for proving statements about all natural numbers, using a base case and an inductive step.",
        "sequences":     "Sequences are ordered lists of numbers following a pattern. Summation formulas provide closed-form expressions for their totals.",
        "combinatorics": "Combinatorics counts arrangements and selections. It underpins probability, cryptography, and algorithm analysis.",
        "graphs":        "Graph theory studies networks of vertices and edges, modelling everything from social networks to circuit layouts and shortest paths.",
    }

    TOPIC_CONCEPTS = {
        "sets": [
            ("Notation",      "A = {1,2,3} — curly braces list elements; ∈ means 'belongs to', ∉ means 'does not belong to'."),
            ("Subset",        "A ⊆ B means every element of A is also in B. A ⊂ B means proper subset (A ≠ B)."),
            ("Union",         "A ∪ B = {x | x ∈ A or x ∈ B} — everything in either set."),
            ("Intersection",  "A ∩ B = {x | x ∈ A and x ∈ B} — only what's in both."),
            ("Difference",    "A − B = {x | x ∈ A and x ∉ B} — elements in A but not B."),
            ("Complement",    "Ā = U − A — everything in the universe NOT in A."),
        ],
        "relations": [
            ("Binary Relation", "R ⊆ A × B — a set of ordered pairs (a,b) linking elements of A to elements of B."),
            ("Reflexive",       "∀a ∈ A: (a,a) ∈ R — every element relates to itself."),
            ("Symmetric",       "(a,b) ∈ R → (b,a) ∈ R — if a relates to b, then b relates to a."),
            ("Transitive",      "(a,b) ∈ R ∧ (b,c) ∈ R → (a,c) ∈ R — chains carry through."),
            ("Antisymmetric",   "(a,b) ∈ R ∧ (b,a) ∈ R → a = b — no mutual distinct pairs."),
            ("Equivalence",     "Reflexive + Symmetric + Transitive — partitions the set into equivalence classes."),
        ],
        "logic": [
            ("Conjunction",    "p ∧ q — true only when both p and q are true."),
            ("Disjunction",    "p ∨ q — true when at least one of p or q is true."),
            ("Negation",       "¬p — flips the truth value of p."),
            ("Implication",    "p → q — false only when p is true and q is false."),
            ("Biconditional",  "p ↔ q — true when p and q have the same truth value."),
            ("De Morgan's",    "¬(p∧q) ≡ ¬p∨¬q and ¬(p∨q) ≡ ¬p∧¬q."),
        ],
        "inference": [
            ("Modus Ponens",          "p, p→q ∴ q — the most fundamental rule."),
            ("Modus Tollens",         "¬q, p→q ∴ ¬p — contrapositive reasoning."),
            ("Hypothetical Syllogism","p→q, q→r ∴ p→r — chain of implications."),
            ("Disjunctive Syllogism", "p∨q, ¬p ∴ q — eliminate a disjunct."),
            ("Addition",              "p ∴ p∨q — a truth implies any disjunction with it."),
            ("Simplification",        "p∧q ∴ p — extract one conjunct from a conjunction."),
        ],
        "proofs": [
            ("Direct Proof",          "Assume p, derive q step by step using definitions and theorems."),
            ("Contradiction",         "Assume ¬p (the negation), derive a logical contradiction."),
            ("Contrapositive",        "Prove p→q by proving its contrapositive ¬q→¬p instead."),
            ("Exhaustive Cases",      "Split into all possible cases and prove each individually."),
            ("Existence Proof",       "Constructive: exhibit a specific example. Non-constructive: show one must exist."),
            ("Uniqueness Proof",      "Show existence, then assume two solutions and prove they are equal."),
        ],
        "induction": [
            ("Base Case",       "Prove P(1) (or P(0)) is true — anchors the chain."),
            ("Inductive Step",  "Assume P(k) is true (inductive hypothesis), prove P(k+1) follows."),
            ("Strong Induction","Assume P(1)…P(k) all true, prove P(k+1) — useful for recurrences."),
            ("Well-Ordering",   "Every non-empty subset of ℕ has a least element — equivalent to induction."),
            ("Sum Formula",     "1+2+…+n = n(n+1)/2 — the classic induction example."),
            ("Power of 2",      "2^n > n for all n ≥ 1 — proved by induction."),
        ],
        "sequences": [
            ("Arithmetic",    "aₙ = a₁ + (n−1)d — constant difference d between terms."),
            ("Geometric",     "aₙ = a₁ · r^(n−1) — constant ratio r between terms."),
            ("Fibonacci",     "F(n) = F(n−1) + F(n−2), F(1)=F(2)=1 — each term is sum of previous two."),
            ("Sum of n",      "Σᵢ₌₁ⁿ i = n(n+1)/2 — sum of first n natural numbers."),
            ("Sum of Squares","Σᵢ₌₁ⁿ i² = n(n+1)(2n+1)/6 — sum of first n squares."),
            ("Geometric Sum", "Σᵢ₌₀ⁿ rⁱ = (r^(n+1)−1)/(r−1) for r≠1."),
        ],
        "combinatorics": [
            ("Multiplication Rule", "If task A has m ways and task B has n ways, together they have m×n ways."),
            ("Permutation",         "P(n,r) = n!/(n−r)! — ordered arrangements of r items from n."),
            ("Combination",         "C(n,r) = n!/(r!(n−r)!) — unordered selections of r items from n."),
            ("Pigeonhole Principle","n+1 objects in n holes → at least one hole has ≥ 2 objects."),
            ("Inclusion-Exclusion", "|A∪B| = |A| + |B| − |A∩B| — avoid double-counting."),
            ("Binomial Theorem",    "(x+y)ⁿ = Σ C(n,k) xᵏ y^(n−k) — coefficient is combination."),
        ],
        "graphs": [
            ("Vertex & Edge",      "A graph G = (V,E) has a vertex set V and edge set E ⊆ V×V."),
            ("Degree",             "deg(v) = number of edges incident to vertex v. Σdeg = 2|E|."),
            ("Path & Cycle",       "Path: sequence of distinct vertices connected by edges. Cycle: path that returns to start."),
            ("Eulerian Path",      "Visits every edge exactly once. Exists iff exactly 0 or 2 vertices have odd degree."),
            ("Eulerian Circuit",   "Eulerian path starting and ending at same vertex. Requires all degrees even."),
            ("Complete Graph Kₙ", "Every pair of vertices is connected. Has n(n−1)/2 edges."),
        ],
    }

    QUIZ_DATA = {
        "sets": [
            {"q": "What does A ∩ B represent?",
             "opts": ["Elements in A or B", "Elements in both A and B", "Elements in A but not B", "Elements not in A or B"], "ans": 1},
            {"q": "If A = {1,2,3} and B = {3,4,5}, what is A ∪ B?",
             "opts": ["{3}", "{1,2,3,4,5}", "{1,2}", "{4,5}"], "ans": 1},
            {"q": "The complement Ā equals:",
             "opts": ["A ∪ U", "U − A", "A ∩ U", "A × U"], "ans": 1},
            {"q": "A ∩ ∅ equals:",
             "opts": ["A", "U", "∅", "A ∪ ∅"], "ans": 2},
            {"q": "How many subsets does a set with 3 elements have?",
             "opts": ["3", "6", "8", "9"], "ans": 2},
            {"q": "A ⊆ B means:",
             "opts": ["A and B are equal", "Every element of A is also in B", "A contains B", "A and B are disjoint"], "ans": 1},
            {"q": "The power set P({a,b}) contains how many elements?",
             "opts": ["2", "4", "3", "1"], "ans": 1},
            {"q": "A − B is equal to:",
             "opts": ["A ∩ B", "A ∩ B'", "A' ∩ B", "A ∪ B'"], "ans": 1},
            {"q": "De Morgan's Law: (A ∪ B)' equals:",
             "opts": ["A' ∪ B'", "A' ∩ B'", "A ∩ B", "A ∪ B"], "ans": 1},
            {"q": "The Cartesian product A × B for |A|=3 and |B|=4 has how many ordered pairs?",
             "opts": ["7", "12", "1", "24"], "ans": 1},
            {"q": "Two sets are disjoint when:",
             "opts": ["Their union is empty", "Their intersection is empty", "One is a subset of the other", "They have equal cardinality"], "ans": 1},
            {"q": "If A = B, then which is true?",
             "opts": ["A ⊂ B only", "B ⊂ A only", "A ⊆ B and B ⊆ A", "A ∩ B = ∅"], "ans": 2},
        ],
        "relations": [
            {"q": "A relation R on set A is symmetric if:",
             "opts": ["(a,a) ∈ R for all a", "(a,b) ∈ R → (b,a) ∈ R", "(a,b),(b,c) ∈ R → (a,c) ∈ R", "None of the above"], "ans": 1},
            {"q": "Which property requires (a,a) ∈ R for all a ∈ A?",
             "opts": ["Symmetric", "Transitive", "Reflexive", "Antisymmetric"], "ans": 2},
            {"q": "An equivalence relation must be:",
             "opts": ["Reflexive only", "Reflexive and symmetric", "Reflexive, symmetric, and transitive", "Transitive only"], "ans": 2},
            {"q": "A partial order relation is:",
             "opts": ["Reflexive, symmetric, transitive", "Reflexive, antisymmetric, transitive", "Irreflexive, symmetric, transitive", "Symmetric and transitive only"], "ans": 1},
            {"q": "The relation 'divides' on positive integers is antisymmetric because:",
             "opts": ["a|b and b|a implies a=b", "a|a for all a", "a|b implies b|a", "a|b and b|c implies a|c"], "ans": 0},
            {"q": "A relation is irreflexive if:",
             "opts": ["(a,a) ∈ R for all a", "(a,a) ∉ R for all a", "(a,b) ∈ R → (b,a) ∉ R", "No pairs exist"], "ans": 1},
            {"q": "The composition R∘S means:",
             "opts": ["Apply R then S", "Apply S then R", "R union S", "R intersect S"], "ans": 1},
            {"q": "An equivalence class [a] contains:",
             "opts": ["Only a itself", "All elements related to a under R", "All elements of the set", "Only elements greater than a"], "ans": 1},
            {"q": "The reflexive closure of R is obtained by adding:",
             "opts": ["All (b,a) for (a,b) ∈ R", "All (a,a) for a ∈ A", "All transitive pairs", "Nothing"], "ans": 1},
            {"q": "A Hasse diagram is used to represent:",
             "opts": ["Any relation", "Equivalence relations only", "Partial orders", "Symmetric relations only"], "ans": 2},
            {"q": "If R has n elements, its relation matrix is of size:",
             "opts": ["n×1", "1×n", "n×n", "n²×n²"], "ans": 2},
            {"q": "The transitive closure ensures:",
             "opts": ["Every element relates to itself", "If aRb and bRc then aRc", "Only direct pairs remain", "All pairs are removed"], "ans": 1},
        ],
        "logic": [
            {"q": "p → q is false only when:",
             "opts": ["p is true and q is true", "p is false and q is true", "p is true and q is false", "p is false and q is false"], "ans": 2},
            {"q": "What is the negation of p ∧ q?  (De Morgan's Law)",
             "opts": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "¬(p ∨ q)"], "ans": 1},
            {"q": "p ↔ q is true when:",
             "opts": ["p is true", "q is false", "p and q have the same truth value", "p implies q only"], "ans": 2},
            {"q": "A tautology is a proposition that is:",
             "opts": ["Always false", "Sometimes true", "Always true", "Undefined"], "ans": 2},
            {"q": "The contrapositive of p → q is:",
             "opts": ["q → p", "¬p → ¬q", "¬q → ¬p", "p → ¬q"], "ans": 2},
            {"q": "p ∨ ¬p is an example of a:",
             "opts": ["Contradiction", "Contingency", "Tautology", "Predicate"], "ans": 2},
            {"q": "p ∧ ¬p is an example of a:",
             "opts": ["Tautology", "Contradiction", "Contingency", "Implication"], "ans": 1},
            {"q": "The converse of p → q is:",
             "opts": ["¬p → ¬q", "q → p", "¬q → ¬p", "p ↔ q"], "ans": 1},
            {"q": "How many rows does a truth table with 3 variables have?",
             "opts": ["3", "6", "8", "9"], "ans": 2},
            {"q": "¬(p ∨ q) is logically equivalent to:",
             "opts": ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∧ q", "¬p → q"], "ans": 1},
            {"q": "The inverse of p → q is:",
             "opts": ["q → p", "¬q → ¬p", "¬p → ¬q", "p ∧ ¬q"], "ans": 2},
            {"q": "p → q is logically equivalent to:",
             "opts": ["q → p", "¬p ∨ q", "p ∧ ¬q", "¬q ∧ p"], "ans": 1},
        ],
        "inference": [
            {"q": "Modus Ponens: from p and p→q, conclude:",
             "opts": ["¬p", "q", "¬q", "p∧q"], "ans": 1},
            {"q": "Modus Tollens: from ¬q and p→q, conclude:",
             "opts": ["p", "q", "¬p", "¬q"], "ans": 2},
            {"q": "Hypothetical Syllogism combines:",
             "opts": ["p and q directly", "p→q and q→r to get p→r", "p and ¬p", "¬p and q"], "ans": 1},
            {"q": "Disjunctive Syllogism: from p∨q and ¬p, conclude:",
             "opts": ["p", "¬q", "q", "p∧q"], "ans": 2},
            {"q": "Addition rule: from p, conclude:",
             "opts": ["p∧q", "¬p", "p∨q for any q", "p→q"], "ans": 2},
            {"q": "Simplification: from p∧q, conclude:",
             "opts": ["p∨q", "p (or q)", "¬p", "p→q"], "ans": 1},
            {"q": "Conjunction rule: from p and q separately, conclude:",
             "opts": ["p→q", "p∨q", "p∧q", "¬p∧¬q"], "ans": 2},
            {"q": "Resolution: from p∨q and ¬p∨r, conclude:",
             "opts": ["p∧r", "q∨r", "¬q∨r", "p∨¬r"], "ans": 1},
            {"q": "An argument is valid when:",
             "opts": ["All premises are true", "The conclusion is true", "True premises guarantee a true conclusion", "The argument uses many rules"], "ans": 2},
            {"q": "Fallacy of affirming the consequent: from q and p→q, (incorrectly) concluding:",
             "opts": ["¬p", "p", "¬q", "q→p"], "ans": 1},
            {"q": "Which rule lets you conclude p→r from p→q and q→r?",
             "opts": ["Modus Ponens", "Disjunctive Syllogism", "Hypothetical Syllogism", "Resolution"], "ans": 2},
            {"q": "Universal Instantiation lets you conclude:",
             "opts": ["∀x P(x) from P(a)", "P(a) for a specific a from ∀x P(x)", "∃x P(x) from ¬∀x ¬P(x)", "None of the above"], "ans": 1},
        ],
        "proofs": [
            {"q": "In proof by contradiction, you assume:",
             "opts": ["The conclusion is true", "The conclusion is false (¬p)", "The hypothesis is false", "Nothing at all"], "ans": 1},
            {"q": "Proof by contrapositive proves p→q by proving:",
             "opts": ["q→p", "¬p→¬q", "¬q→¬p", "p∧¬q → contradiction"], "ans": 2},
            {"q": "A direct proof of p→q starts by assuming:",
             "opts": ["¬p", "¬q", "p", "q"], "ans": 2},
            {"q": "A constructive existence proof:",
             "opts": ["Shows a contradiction", "Exhibits a specific example satisfying the property", "Assumes the opposite and derives falsehood", "Uses induction"], "ans": 1},
            {"q": "Proof by cases is most useful when:",
             "opts": ["The statement is trivially true", "The domain naturally splits into exhaustive sub-cases", "You need a single counterexample", "All variables are quantified universally"], "ans": 1},
            {"q": "To disprove a universal statement ∀x P(x), you need:",
             "opts": ["A proof that P(a) is true for some a", "A single counterexample where P(a) is false", "An infinite chain of implications", "A contradiction in the premises"], "ans": 1},
            {"q": "The contrapositive of 'If n² is odd, then n is odd' is:",
             "opts": ["If n is odd, then n² is odd", "If n is even, then n² is even", "If n² is even, then n is even", "If n is even, then n² is odd"], "ans": 2},
            {"q": "A biconditional proof (p ↔ q) requires proving:",
             "opts": ["Only p→q", "Only q→p", "Both p→q and q→p", "The contrapositive of p→q"], "ans": 2},
            {"q": "A non-constructive existence proof:",
             "opts": ["Constructs the object explicitly", "Shows the object must exist without identifying it", "Proves uniqueness", "Uses strong induction"], "ans": 1},
            {"q": "In a uniqueness proof, after showing existence, you assume:",
             "opts": ["The object does not exist", "Two objects satisfy the condition, then show they are equal", "The negation of the conclusion", "All objects satisfy the condition"], "ans": 1},
            {"q": "Proof by exhaustion is valid only when:",
             "opts": ["The statement is complex", "There are finitely many cases to check", "The domain is infinite", "Contradiction is unavoidable"], "ans": 1},
            {"q": "Which proof technique is being used: 'Assume n is even, write n=2k, show n²=4k² is even'?",
             "opts": ["Contradiction", "Contrapositive", "Direct proof", "Exhaustion"], "ans": 2},
        ],
        "induction": [
            {"q": "Mathematical induction requires:",
             "opts": ["Only the base case", "Only the inductive step", "Both base case and inductive step", "A contradiction"], "ans": 2},
            {"q": "In the inductive step, you prove:",
             "opts": ["P(1) is true", "P(k) → P(k+1)", "P(k) is false", "P(n) for all n at once"], "ans": 1},
            {"q": "The sum 1+2+...+n equals:",
             "opts": ["n²", "n(n+1)/2", "n(n−1)/2", "2n"], "ans": 1},
            {"q": "Strong induction assumes:",
             "opts": ["P(1) only", "P(k) for a single k", "P(1), P(2), …, P(k) all true to prove P(k+1)", "Nothing about previous cases"], "ans": 2},
            {"q": "The base case in induction serves to:",
             "opts": ["Complete the proof alone", "Anchor the chain at the starting value", "Replace the inductive step", "Prove uniqueness"], "ans": 1},
            {"q": "What is the sum 1²+2²+…+n²?",
             "opts": ["n(n+1)/2", "n(n+1)(2n+1)/6", "n²(n+1)²/4", "n(n+1)(n+2)/6"], "ans": 1},
            {"q": "The inductive hypothesis is:",
             "opts": ["The conclusion we want to prove", "The assumption that P(k) is true for some k ≥ base", "The base case", "A counterexample"], "ans": 1},
            {"q": "Which sequence is best proved by strong induction?",
             "opts": ["Arithmetic sequences", "Geometric sequences", "Fibonacci-type recurrences", "Constant sequences"], "ans": 2},
            {"q": "If base case is n=0 and inductive step proves P(k)→P(k+1), induction holds for:",
             "opts": ["n ≥ 1 only", "n ≥ 0", "n = 0 only", "All integers"], "ans": 1},
            {"q": "The sum of first n odd numbers 1+3+5+…+(2n−1) equals:",
             "opts": ["n(n+1)/2", "n²", "2n−1", "n(2n−1)"], "ans": 1},
            {"q": "Structural induction is used to prove properties of:",
             "opts": ["Real numbers", "Recursively defined structures (trees, lists)", "Finite sets only", "Prime numbers"], "ans": 1},
            {"q": "To prove 3ⁿ > 2n+1 for n ≥ 2 by induction, the base case checks:",
             "opts": ["n=0", "n=1", "n=2", "n=3"], "ans": 2},
        ],
        "sequences": [
            {"q": "In arithmetic sequence with first term a₁ and difference d, the nth term is:",
             "opts": ["a₁ + nd", "a₁ + (n−1)d", "a₁ · dⁿ", "a₁ · (n−1)"], "ans": 1},
            {"q": "F(5) in the Fibonacci sequence (F(1)=F(2)=1) is:",
             "opts": ["5", "6", "7", "8"], "ans": 0},
            {"q": "A geometric sequence is characterised by:",
             "opts": ["Constant difference", "Constant ratio between consecutive terms", "Alternating signs", "Constant partial sum"], "ans": 1},
            {"q": "The sum of a finite geometric series a + ar + ar² + … + arⁿ⁻¹ is:",
             "opts": ["a(rⁿ+1)/(r+1)", "a(rⁿ−1)/(r−1) for r≠1", "arⁿ", "a/(1−r)"], "ans": 1},
            {"q": "What is the 7th term of the sequence 2, 5, 8, 11, …?",
             "opts": ["20", "23", "17", "14"], "ans": 0},
            {"q": "The sum Σᵢ₌₁ⁿ i³ equals:",
             "opts": ["n²(n+1)²/4", "n(n+1)(2n+1)/6", "n(n+1)/2", "n³"], "ans": 0},
            {"q": "F(7) in the Fibonacci sequence (F(1)=F(2)=1) is:",
             "opts": ["11", "13", "8", "21"], "ans": 1},
            {"q": "An infinite geometric series a/(1−r) converges when:",
             "opts": ["|r| > 1", "|r| = 1", "|r| < 1", "r = 0 only"], "ans": 2},
            {"q": "The common difference d of the sequence 4, 7, 10, 13, … is:",
             "opts": ["2", "3", "4", "7"], "ans": 1},
            {"q": "Σᵢ₌₁⁵ i equals:",
             "opts": ["10", "15", "20", "25"], "ans": 1},
            {"q": "A sequence defined by aₙ = aₙ₋₁ + aₙ₋₂ is called:",
             "opts": ["Arithmetic", "Geometric", "Fibonacci-type / linear recurrence", "Harmonic"], "ans": 2},
            {"q": "The sum of the first 100 natural numbers is:",
             "opts": ["5000", "5050", "4950", "10100"], "ans": 1},
        ],
        "combinatorics": [
            {"q": "How many ways to arrange 5 distinct objects in a row?",
             "opts": ["5", "25", "120", "60"], "ans": 2},
            {"q": "C(5,2) equals:",
             "opts": ["10", "20", "5", "25"], "ans": 0},
            {"q": "The Pigeonhole Principle states:",
             "opts": ["n objects in n holes → all equal", "n+1 objects in n holes → some hole has ≥2", "n objects need n² holes", "All of the above"], "ans": 1},
            {"q": "P(n,r) = n!/(n−r)! counts:",
             "opts": ["Unordered subsets of size r", "Ordered arrangements of r items from n", "Subsets including repetition", "Circular arrangements"], "ans": 1},
            {"q": "How many ways can a committee of 3 be chosen from 7 people?",
             "opts": ["21", "35", "210", "42"], "ans": 1},
            {"q": "The number of ways to arrange the letters of 'AABB' (with repetition) is:",
             "opts": ["24", "12", "6", "4"], "ans": 2},
            {"q": "By the multiplication principle, if event A has 4 outcomes and event B has 5, the number of combined outcomes is:",
             "opts": ["9", "20", "1", "45"], "ans": 1},
            {"q": "The binomial coefficient C(n,0) equals:",
             "opts": ["0", "n", "1", "n!"], "ans": 2},
            {"q": "How many 4-digit PINs are possible using digits 0–9 with repetition allowed?",
             "opts": ["5040", "210", "10000", "9999"], "ans": 2},
            {"q": "Inclusion-Exclusion: |A ∪ B| equals:",
             "opts": ["|A| + |B|", "|A| + |B| − |A∩B|", "|A| × |B|", "|A| − |B|"], "ans": 1},
            {"q": "The number of permutations of n objects in a circle is:",
             "opts": ["n!", "(n−1)!", "n!/2", "n²"], "ans": 1},
            {"q": "Stars and bars gives the number of ways to distribute k identical objects into n distinct bins as:",
             "opts": ["C(k,n)", "C(n+k−1, k)", "P(n,k)", "k^n"], "ans": 1},
        ],
        "graphs": [
            {"q": "The degree of a vertex is:",
             "opts": ["Its index in the adjacency list", "Number of edges incident to it", "Number of vertices it equals", "Its distance from source"], "ans": 1},
            {"q": "An Eulerian path visits:",
             "opts": ["Every vertex exactly once", "Every edge exactly once", "Every vertex twice", "Only leaf vertices"], "ans": 1},
            {"q": "Complete graph Kₙ has how many edges?",
             "opts": ["n", "n²", "n(n−1)/2", "2n"], "ans": 2},
            {"q": "The Handshaking Lemma states: Σ deg(v) =",
             "opts": ["|V|", "|E|", "2|E|", "|V| × |E|"], "ans": 2},
            {"q": "A graph is bipartite if:",
             "opts": ["Every vertex has even degree", "Vertices can be split into two sets with edges only between sets", "It has no cycles", "It is complete"], "ans": 1},
            {"q": "A Hamiltonian path visits:",
             "opts": ["Every edge exactly once", "Every vertex exactly once", "Only even-degree vertices", "Adjacent vertices twice"], "ans": 1},
            {"q": "An Eulerian circuit exists if and only if:",
             "opts": ["The graph is connected and all vertices have even degree", "The graph has no cycles", "All vertices have degree 2", "The graph is a tree"], "ans": 0},
            {"q": "A tree with n vertices has exactly how many edges?",
             "opts": ["n", "n+1", "n−1", "2n"], "ans": 2},
            {"q": "Two graphs are isomorphic if:",
             "opts": ["They have the same number of vertices", "There exists a structure-preserving bijection between their vertex sets", "They have the same edge weights", "They look identical when drawn"], "ans": 1},
            {"q": "The chromatic number χ(G) of a graph is:",
             "opts": ["The number of edges", "The minimum number of colours needed to colour vertices so adjacent ones differ", "The maximum degree", "The number of cycles"], "ans": 1},
            {"q": "A connected acyclic graph is called:",
             "opts": ["A bipartite graph", "A complete graph", "A tree", "A multigraph"], "ans": 2},
            {"q": "Breadth-First Search (BFS) is used to find:",
             "opts": ["Minimum spanning trees only", "The shortest path in an unweighted graph", "Eulerian circuits", "Graph colouring"], "ans": 1},
        ],
    }

    PRACTICE_DATA = {
        "sets": [
            {"q": "Let A = {1,2,3,4} and B = {3,4,5,6}. Find A∩B, A∪B, and A−B.",
             "sol": "Step 1: List elements of A and B.\nA = {1,2,3,4}, B = {3,4,5,6}.\nStep 2: Find intersection (A∩B): Elements in both A and B are {3,4}.\nStep 3: Find union (A∪B): Combine all unique elements: {1,2,3,4,5,6}.\nStep 4: Find difference (A−B): Elements in A not in B are {1,2}.\nFinal answers: A∩B = {3,4}, A∪B = {1,2,3,4,5,6}, A−B = {1,2}."},
            {"q": "If U = {1…10}, A = {2,4,6,8}, B = {1,2,3,4}, find A' and (A∪B)'.",
             "sol": "Step 1: List universal set U = {1,2,3,4,5,6,7,8,9,10}.\nStep 2: Find complement of A (A'): Elements in U not in A: {1,3,5,7,9,10}.\nStep 3: Find union A∪B: {1,2,3,4,6,8}.\nStep 4: Find complement of (A∪B): Elements in U not in A∪B: {5,7,9,10}.\nFinal answers: A' = {1,3,5,7,9,10}, (A∪B)' = {5,7,9,10}."},
        ],
        "relations": [
            {"q": "R = {(1,1),(1,2),(2,1),(2,2),(3,3)} on A={1,2,3}. Is R reflexive, symmetric, transitive?",
             "sol": "Step 1: Reflexive? Check if (a,a) for all a in A. (1,1), (2,2), (3,3) are present. Yes.\nStep 2: Symmetric? For every (a,b), is (b,a) present? (1,2) and (2,1) are both present. Yes.\nStep 3: Transitive? For (a,b) and (b,c), is (a,c) present? (1,2)+(2,1)→(1,1), (2,1)+(1,2)→(2,2), all such cases are present. Yes.\nConclusion: R is reflexive, symmetric, and transitive, so it is an equivalence relation."},
            {"q": "Find the transitive closure of R = {(1,2),(2,3)} on {1,2,3}.",
             "sol": "Step 1: List pairs: (1,2), (2,3).\nStep 2: Check for indirect connections: (1,2) and (2,3) imply (1,3) by transitivity.\nStep 3: Add (1,3) to the relation.\nFinal answer: Transitive closure = {(1,2), (2,3), (1,3)}."},
        ],
        "logic": [
            {"q": "Construct a truth table for (p → q) ∧ (q → p).",
             "sol": "Step 1: List all combinations of p and q (TT, TF, FT, FF).\nStep 2: Compute p→q and q→p for each row.\nStep 3: Take AND of both results for each row.\nStep 4: Observe that (p→q)∧(q→p) is true only when p and q have the same value (TT or FF), so it is equivalent to p↔q.\nTruth table:\np q | (p→q) | (q→p) | AND\nT T |   T   |   T   |  T\nT F |   F   |   T   |  F\nF T |   T   |   F   |  F\nF F |   T   |   T   |  T"},
            {"q": "Show ¬(p ∧ q) ≡ ¬p ∨ ¬q using a truth table.",
             "sol": "Step 1: List all combinations of p and q.\nStep 2: Compute p∧q for each row.\nStep 3: Compute ¬(p∧q) for each row.\nStep 4: Compute ¬p and ¬q, then (¬p∨¬q) for each row.\nStep 5: Compare columns: they are identical in all cases.\nConclusion: ¬(p∧q) ≡ ¬p∨¬q (De Morgan's Law)."},
        ],
        "inference": [
            {"q": "'If it rains, the ground is wet.' It is raining. Conclude using Modus Ponens.",
             "sol": "Step 1: Premise: If it rains, the ground is wet (p→q).\nStep 2: Premise: It is raining (p is true).\nStep 3: By Modus Ponens, since p→q and p, conclude q.\nConclusion: The ground is wet."},
            {"q": "Given p→q, q→r, p. Derive r step by step.",
             "sol": "Step 1: p (given).\nStep 2: p→q (given).\nStep 3: By Modus Ponens on steps 1 and 2, q is true.\nStep 4: q→r (given).\nStep 5: By Modus Ponens on steps 3 and 4, r is true.\nConclusion: r is derived."},
        ],
        "proofs": [
            {"q": "Prove: If n is odd, then n² is odd. (Direct proof)",
             "sol": "Step 1: Let n be odd, so n = 2k+1 for some integer k.\nStep 2: Compute n² = (2k+1)² = 4k² + 4k + 1.\nStep 3: Factor: 4k² + 4k = 2(2k²+2k), so n² = 2(2k²+2k) + 1.\nStep 4: This is of the form 2m+1, which is odd.\nConclusion: n² is odd if n is odd."},
            {"q": "Prove √2 is irrational by contradiction.",
             "sol": "Step 1: Assume √2 is rational, so √2 = p/q in lowest terms.\nStep 2: Square both sides: 2 = p²/q² → 2q² = p².\nStep 3: p² is even, so p must be even. Let p = 2m.\nStep 4: Substitute: 2q² = (2m)² = 4m² → q² = 2m², so q² is even, so q is even.\nStep 5: Both p and q are even, contradicting lowest terms.\nConclusion: √2 is irrational."},
        ],
        "induction": [
            {"q": "Prove by induction: 1+2+…+n = n(n+1)/2.",
             "sol": "Step 1: Base case n=1: 1 = 1·2/2 = 1. True.\nStep 2: Inductive step: Assume true for n=k, so 1+2+...+k = k(k+1)/2.\nStep 3: For n=k+1: 1+2+...+k+(k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2.\nStep 4: Therefore, true for n=k+1.\nConclusion: The formula holds for all n by induction."},
            {"q": "Prove by induction: 2ⁿ > n for all n ≥ 1.",
             "sol": "Step 1: Base case n=1: 2^1=2 > 1. True.\nStep 2: Inductive step: Assume 2^k > k for some k≥1.\nStep 3: For n=k+1: 2^(k+1) = 2·2^k > 2k.\nStep 4: Since 2k ≥ k+1 for k≥1, 2^(k+1) > k+1.\nConclusion: 2ⁿ > n for all n≥1 by induction."},
        ],
        "sequences": [
            {"q": "Find the 10th term of: 3, 7, 11, 15, …",
             "sol": "Step 1: Identify first term a₁=3 and common difference d=4.\nStep 2: Use formula aₙ = a₁ + (n−1)d.\nStep 3: For n=10: a₁₀ = 3 + 9×4 = 3 + 36 = 39.\nFinal answer: 39."},
            {"q": "What is the sum of the first 20 natural numbers?",
             "sol": "Step 1: Use formula for sum: Sₙ = n(n+1)/2.\nStep 2: For n=20: S = 20×21/2 = 210.\nFinal answer: 210."},
        ],
        "combinatorics": [
            {"q": "How many 3-letter arrangements can be made from the letters M, A, T, H?",
             "sol": "Step 1: Number of letters = 4.\nStep 2: Number of ways to arrange 3 out of 4 = P(4,3).\nStep 3: P(4,3) = 4!/(4−3)! = 24.\nFinal answer: 24."},
            {"q": "A committee of 4 is chosen from 10 people. How many ways?",
             "sol": "Step 1: Number of people = 10.\nStep 2: Number to choose = 4.\nStep 3: Use combinations: C(10,4) = 10!/(4!·6!) = 210.\nFinal answer: 210."},
        ],
        "graphs": [
            {"q": "K₄ has how many edges? Verify with the formula.",
             "sol": "Step 1: K₄ is a complete graph with n=4 vertices.\nStep 2: Use formula for edges: n(n−1)/2.\nStep 3: 4×3/2 = 6.\nFinal answer: 6 edges."},
            {"q": "Does a graph with degree sequence (2,2,2,2,2,2) have an Eulerian circuit?",
             "sol": "Step 1: Eulerian circuit exists if all vertices have even degree and the graph is connected.\nStep 2: All degrees are 2 (even).\nStep 3: If the graph is connected, Euler's Theorem applies.\nConclusion: Yes, an Eulerian circuit exists."},
        ],
    }

    # ── Session state init ────────────────────────────────────
    if "sh_progress" not in st.session_state:
        st.session_state.sh_progress = {
            k: {"read": False, "quiz_score": None, "practice_done": False}
            for k, *_ in STUDY_TOPICS
        }
    if "sh_quiz_ans" not in st.session_state:
        st.session_state.sh_quiz_ans = {}
    if "sh_quiz_submitted" not in st.session_state:
        st.session_state.sh_quiz_submitted = {}
    if "sh_show_sol" not in st.session_state:
        st.session_state.sh_show_sol = {}

    prog = st.session_state.sh_progress

    # ── Helper: per-topic completion score 0-3 ───────────────
    def topic_score(k):
        p = prog[k]
        s = 0
        if p["read"]: s += 1
        if p["quiz_score"] is not None: s += 1
        if p["practice_done"]: s += 1
        return s

    total_topics = len(STUDY_TOPICS)
    topics_explored = sum(1 for k, *_ in STUDY_TOPICS if topic_score(k) > 0)
    quizzes_taken   = sum(1 for k, *_ in STUDY_TOPICS if prog[k]["quiz_score"] is not None)
    best_score      = max((prog[k]["quiz_score"] or 0) for k, *_ in STUDY_TOPICS)
    best_pct        = round(best_score / len(QUIZ_DATA[max(STUDY_TOPICS, key=lambda t: prog[t[0]]["quiz_score"] or 0)[0]]) * 100) if best_score else 0
    overall_pct     = round(sum(topic_score(k) for k, *_ in STUDY_TOPICS) / (total_topics * 3) * 100)

    # ── Achievements ─────────────────────────────────────────
    achievements = [
        ("First Step",   "◉", any(prog[k]["read"] for k, *_ in STUDY_TOPICS)),
        ("Quiz Taker",   "✎", quizzes_taken >= 1),
        ("Half Way",     "◑", overall_pct >= 50),
        ("Quiz Master",  "★", best_pct == 100),
        ("Practice Pro", "⚙", all(prog[k]["practice_done"] for k, *_ in STUDY_TOPICS)),
        ("Graduate",     "◆", overall_pct == 100),
    ]

    # ── Page header ───────────────────────────────────────────
    st.markdown("<div class='sec-tag'>// STUDY_HUB · YOUR_LEARNING_SPACE</div>", unsafe_allow_html=True)
    st.markdown("## Your Learning Journey")
    st.markdown("""
    <p style='color:#8892a4;max-width:700px;'>
    Track your progress across all topics, follow the structured learning roadmap,
    and dive into explanations, quizzes, and practice problems — all in one place.
    </p>""", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    tab_dash, tab_road, tab_session = st.tabs(["📊  Progress Dashboard", "🗺  Learning Roadmap", "📖  Study Session"])

    # ══════════════════════════════════════════════════════════
    # TAB 1 — PROGRESS DASHBOARD
    # ══════════════════════════════════════════════════════════
    with tab_dash:
        # Stat cards
        st.markdown(f"""
        <div class='sh-stat-grid'>
          <div class='sh-stat'>
            <div class='sh-stat-val'>{overall_pct}%</div>
            <div class='sh-stat-lbl'>Overall Progress</div>
          </div>
          <div class='sh-stat'>
            <div class='sh-stat-val'>{topics_explored}</div>
            <div class='sh-stat-lbl'>Topics Explored / {total_topics}</div>
          </div>
          <div class='sh-stat'>
            <div class='sh-stat-val'>{quizzes_taken}</div>
            <div class='sh-stat-lbl'>Quizzes Taken</div>
          </div>
          <div class='sh-stat'>
            <div class='sh-stat-val'>{best_pct}%</div>
            <div class='sh-stat-lbl'>Best Quiz Score</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Overall mastery bar
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;'>
          <span style='font-size:0.88rem;font-weight:600;color:#e8eaf0;'>Overall Mastery</span>
          <span style='font-family:"JetBrains Mono",monospace;font-size:0.75rem;color:#4ECCA3;'>{overall_pct}%</span>
        </div>
        <div class='sh-bar-wrap' style='height:8px;margin-bottom:1.5rem;'>
          <div class='sh-bar-fill' style='width:{overall_pct}%;'></div>
        </div>""", unsafe_allow_html=True)

        # Achievements
        st.markdown("<div class='sec-tag'>// ACHIEVEMENTS</div>", unsafe_allow_html=True)
        ach_html = "<div class='sh-ach-grid'>"
        for name, icon, earned in achievements:
            cls = "earned" if earned else "locked"
            lock = "" if earned else "🔒 "
            ach_html += f"<div class='sh-ach {cls}'>{lock}{icon} {name}</div>"
        ach_html += "</div>"
        st.markdown(ach_html, unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Topic breakdown
        st.markdown("<div class='sec-tag'>// TOPIC_BREAKDOWN</div>", unsafe_allow_html=True)
        for key, label, icon, week in STUDY_TOPICS:
            p = prog[key]
            sc = topic_score(key)
            pct = round(sc / 3 * 100)
            read_cls  = "done" if p["read"]           else "todo"
            quiz_cls  = "done" if p["quiz_score"] is not None else "todo"
            prac_cls  = "done" if p["practice_done"]  else "todo"
            quiz_lbl  = f"{round(p['quiz_score']/len(QUIZ_DATA[key])*100)}%" if p["quiz_score"] is not None else "Quiz"
            st.markdown(f"""
            <div class='sh-topic-row'>
              <span style='font-size:1.1rem;color:#4ECCA3;width:22px;text-align:center;'>{icon}</span>
              <span class='sh-topic-name'>{label}</span>
              <div class='sh-topic-pills'>
                <span class='sh-pill {read_cls}'>READ</span>
                <span class='sh-pill {quiz_cls}'>{quiz_lbl}</span>
                <span class='sh-pill {prac_cls}'>PRACTICE</span>
              </div>
              <div style='width:120px;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                  <span style='font-family:"JetBrains Mono",monospace;font-size:0.6rem;color:#4a5568;'>{week}</span>
                  <span style='font-family:"JetBrains Mono",monospace;font-size:0.6rem;color:#4ECCA3;'>{pct}%</span>
                </div>
                <div class='sh-bar-wrap'><div class='sh-bar-fill' style='width:{pct}%;'></div></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2 — LEARNING ROADMAP
    # ══════════════════════════════════════════════════════════
    with tab_road:
        topic_map = {k: (lbl, icon, week) for k, lbl, icon, week in STUDY_TOPICS}
        st.markdown("""
        <p style='text-align:center;color:#8892a4;font-size:0.85rem;'>
        Follow this structured path from foundations to advanced topics.<br>
        Each node shows your completion progress.
        </p>""", unsafe_allow_html=True)

        for gi, (group_name, keys) in enumerate(ROADMAP_GROUPS):
            nodes_html = ""
            for k in keys:
                lbl, icon, week = topic_map[k]
                sc  = topic_score(k)
                pct = round(sc / 3 * 100)
                nodes_html += f"""
<div class='sh-road-node'>
  <div class='sh-road-icon'>{icon}</div>
  <div class='sh-road-name'>{lbl}</div>
  <div class='sh-road-week'>{week}</div>
  <div class='sh-road-prog'>
    <div class='sh-bar-wrap'><div class='sh-bar-fill' style='width:{pct}%;'></div></div>
    <div style='font-family:"JetBrains Mono",monospace;font-size:0.58rem;color:#4ECCA3;margin-top:3px;'>{pct}%</div>
  </div>
</div>"""

            st.markdown(f"""
            <div class='sh-road-group'>
              <div class='sh-road-label'>{group_name}</div>
              <div class='sh-road-row'>{nodes_html}</div>
            </div>""", unsafe_allow_html=True)

            if gi < len(ROADMAP_GROUPS) - 1:
                st.markdown("<div class='sh-arrow'>↓</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 3 — STUDY SESSION
    # ══════════════════════════════════════════════════════════
    with tab_session:
        topic_labels  = {k: lbl for k, lbl, *_ in STUDY_TOPICS}
        topic_options = [lbl for _, lbl, *_ in STUDY_TOPICS]
        topic_keys    = [k   for k, *_ in STUDY_TOPICS]

        col_sel, col_mode = st.columns([1, 2])
        with col_sel:
            chosen_label = st.selectbox("Topic", topic_options, key="sh_topic_sel",
                                        label_visibility="visible")
        chosen_key = topic_keys[topic_options.index(chosen_label)]

        with col_mode:
            mode = st.radio("Study Mode", ["📘 Read & Learn", "✏️ Take a Quiz", "💪 Practice Problems"],
                            horizontal=True, key="sh_mode_sel", label_visibility="visible")

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # ── READ & LEARN ────────────────────────────────────
        if mode == "📘 Read & Learn":
            st.markdown(f"""
            <div class='sh-overview'>
              <div class='sh-overview-tag'>OVERVIEW</div>
              <div class='sh-overview-text'>{TOPIC_OVERVIEWS[chosen_key]}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("### Key Concepts")
            concepts = TOPIC_CONCEPTS[chosen_key]
            rows = [concepts[i:i+2] for i in range(0, len(concepts), 2)]
            for row in rows:
                cols = st.columns(len(row))
                for ci, (title, body) in enumerate(row):
                    with cols[ci]:
                        st.markdown(f"""
                        <div class='sh-concept-card'>
                          <div class='sh-concept-title'>{title}</div>
                          <div class='sh-concept-body'>{body}</div>
                        </div>""", unsafe_allow_html=True)

            st.markdown("")
            if st.button("✓ Mark as Read", key=f"sh_read_{chosen_key}",
                         type="primary" if not prog[chosen_key]["read"] else "secondary"):
                st.session_state.sh_progress[chosen_key]["read"] = True
                st.success(f"'{chosen_label}' marked as read!")
                st.rerun()

            if prog[chosen_key]["read"]:
                st.markdown("<span style='color:#4ECCA3;font-family:\"JetBrains Mono\",monospace;font-size:0.75rem;'>✓ COMPLETED — READING DONE</span>", unsafe_allow_html=True)

        # ── TAKE A QUIZ ─────────────────────────────────────
        elif mode == "✏️ Take a Quiz":
            questions = QUIZ_DATA[chosen_key]
            qkey = f"quiz_{chosen_key}"
            submitted = st.session_state.sh_quiz_submitted.get(qkey, False)

            if submitted:
                answers = st.session_state.sh_quiz_ans.get(qkey, {})
                score = sum(1 for i, qd in enumerate(questions) if answers.get(i) == qd["opts"][qd["ans"]])
                pct = round(score / len(questions) * 100)
                st.markdown(f"""
                <div class='sh-stat' style='max-width:320px;margin-bottom:1.5rem;'>
                  <div class='sh-stat-val'>{score}/{len(questions)}</div>
                  <div class='sh-stat-lbl'>{pct}% — {'Perfect! ◆' if pct==100 else 'Good effort' if pct>=66 else 'Keep practising'}</div>
                </div>""", unsafe_allow_html=True)

                for i, qd in enumerate(questions):
                    user_ans = answers.get(i)
                    correct  = qd["opts"][qd["ans"]]
                    ok = user_ans == correct
                    colour = "#4ECCA3" if ok else "#ff6b6b"
                    icon_r  = "✓" if ok else "✗"
                    st.markdown(f"""
                    <div class='sh-quiz-q' style='border-left:3px solid {colour};'>
                      <div class='sh-quiz-num'>Q{i+1}</div>
                      <div class='sh-quiz-text'>{qd["q"]}</div>
                      <div style='font-size:0.8rem;color:{colour};margin-top:0.5rem;font-family:"JetBrains Mono",monospace;'>
                        {icon_r} Your answer: {user_ans or "—"}<br>
                        {'✓ Correct!' if ok else f'Correct: {correct}'}
                      </div>
                    </div>""", unsafe_allow_html=True)

                if st.button("Retake Quiz", key=f"sh_retry_{chosen_key}"):
                    st.session_state.sh_quiz_submitted[qkey] = False
                    st.session_state.sh_quiz_ans[qkey] = {}
                    st.rerun()

            else:
                if qkey not in st.session_state.sh_quiz_ans:
                    st.session_state.sh_quiz_ans[qkey] = {}

                for i, qd in enumerate(questions):
                    st.markdown(f"""
                    <div class='sh-quiz-q'>
                      <div class='sh-quiz-num'>QUESTION {i+1} / {len(questions)}</div>
                      <div class='sh-quiz-text'>{qd["q"]}</div>
                    </div>""", unsafe_allow_html=True)
                    chosen_opt = st.radio(
                        f"q{i}", qd["opts"], index=None,
                        key=f"sh_q_{chosen_key}_{i}",
                        label_visibility="collapsed"
                    )
                    if chosen_opt:
                        st.session_state.sh_quiz_ans[qkey][i] = chosen_opt

                st.markdown("")
                if st.button("Submit Quiz", key=f"sh_submit_{chosen_key}", type="primary"):
                    answers = st.session_state.sh_quiz_ans.get(qkey, {})
                    if len(answers) < len(questions):
                        st.warning("Please answer all questions before submitting.")
                    else:
                        score = sum(1 for i, qd in enumerate(questions) if answers.get(i) == qd["opts"][qd["ans"]])
                        st.session_state.sh_progress[chosen_key]["quiz_score"] = score
                        st.session_state.sh_quiz_submitted[qkey] = True
                        st.rerun()

        # ── PRACTICE PROBLEMS ──────────────────────────────
        elif mode == "💪 Practice Problems":
            problems = PRACTICE_DATA[chosen_key]
            show_key = f"sol_{chosen_key}"
            if show_key not in st.session_state.sh_show_sol:
                st.session_state.sh_show_sol[show_key] = set()

            st.markdown(f"<div class='sec-tag'>// {len(problems)} PRACTICE PROBLEMS — {chosen_label.upper()}</div>", unsafe_allow_html=True)

            for i, prob in enumerate(problems):
                st.markdown(f"""
                <div class='sh-practice-card'>
                  <div style='font-family:"JetBrains Mono",monospace;font-size:0.6rem;color:#4ECCA3;margin-bottom:0.4rem;'>PROBLEM {i+1}</div>
                  <div class='sh-practice-q'>{prob["q"]}</div>
                </div>""", unsafe_allow_html=True)

                if i in st.session_state.sh_show_sol[show_key]:
                    st.markdown(f"<div class='sh-practice-sol'>{prob['sol']}</div>", unsafe_allow_html=True)
                    st.markdown("")
                else:
                    if st.button(f"Show Solution", key=f"sh_sol_{chosen_key}_{i}"):
                        st.session_state.sh_show_sol[show_key].add(i)
                        st.rerun()
                st.markdown("")

            all_revealed = len(st.session_state.sh_show_sol.get(show_key, set())) == len(problems)
            if all_revealed and not prog[chosen_key]["practice_done"]:
                if st.button("✓ Mark Practice Complete", key=f"sh_prac_{chosen_key}", type="primary"):
                    st.session_state.sh_progress[chosen_key]["practice_done"] = True
                    st.success("Practice marked as complete!")
                    st.rerun()

            if prog[chosen_key]["practice_done"]:
                st.markdown("<span style='color:#4ECCA3;font-family:\"JetBrains Mono\",monospace;font-size:0.75rem;'>✓ PRACTICE COMPLETE</span>", unsafe_allow_html=True)

# ── Footer (all pages) ───────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(FOOTER_HTML, unsafe_allow_html=True)

