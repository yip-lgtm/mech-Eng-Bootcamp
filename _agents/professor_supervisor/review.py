#!/usr/bin/env python3
"""Multi-Agent Pipeline — Professor Supervisor Quality Gate Reviewer"""
import os, re, sys, json, argparse
from pathlib import Path

TEMPLATE_MARKERS = [
    r'\[TBD\]', r'待補充', r'placeholder', r'Lorem ipsum',
    r'CORE_DEEPDIVE_ONE', r'T0 — Core', r'T1 — Methods', r'T2 — Applications',
    r'PLACEHOLDER', r'\[TODO\]', r'Fixme', r'fixme',
]

SCHOLAR_HINT = re.compile(r'\b('
    r'Newton|Euler|Lagrange|Hamilton|Maxwell|Boltzmann|Fourier|'
    r'Bohr|Heisenberg|Schrödinger|Dirac|Fermi|Bose|Einstein|Planck|'
    r'Timoshenko|Stokes|Navier|Reynolds|Prandtl|von Kármán|'
    r'Hemond|Sigmund|Bendsøe|Holzapfel|Ogden|Simo|Taylor|'
    r'Stumm|Schwarzenbach|Girard|Sposito|Bradl|'
    r'Braudel|Hobsbawm|Thompson|Anderson|Tilly|Mayer|'
    r'von Ranke|Bloch|Marc Bloch|Febvre|'
    r'Boyd|Vandenberghe|Nesterov|Bertsekas|Papadimitriou|'
    r'Papoulis|Ross|Feller|Billingsley|Durrett|'
    r'Wasserman|Casella|Hastie|Trefethen|Golub|'
    r'Sheffi|Daganzo|Wardrop|Newell|'
    r'Porter|Ansoff|Christensen|'
    r'Wen|Bernevig|Hasan|Qi|Zhang|'
    r'Ashcroft|Kittel|Mermin|Simon|'
    r'Griffiths|Sakurai|Zee|Weinberg|Peskin|Srednicki|'
    r'Coleman|Polchinski|Witten|Gross|Politzer|Wilczek|'
    r'Ginsparg|Larivière|Eysenbach|Wager|Harnad|'
    r'Wilkinson|Vicente-Saiz|Nosek|McKiernan|'
    r'Bornmann|Peters|Mahoney|Squazzoni|'
    r'Bubela|Hilgartner|Weigold|'
    r'Bunge|Kuhn|Popper|Feyerabend|'
    r'Sword|Hill|Hyland|Salomone|'
    r'Feynman|Bohr|Heisenberg|Schrödinger|Dirac|von Neumann|'
    r'Coulomb|Ampère|Ohm|Faraday|Henry|Tesla|Weber|'
    r'Wuchty|Newman|Barabási|Guimerà|'
    r'Wager|Peters|Bornmann|'
    r'Wager|Harnad'
    r')\b')

YEAR_HINT = re.compile(r'\b(1[6-9]\d{2}|20\d{2})\b')


def gate1_length(c):
    lines = c.count("\n")
    return 10 if lines >= 400 else 7 if lines >= 300 else 4 if lines >= 200 else 0

def gate2_format(c):
    s = 0
    if re.search(r"問題 1|心智模型|mental model|5.*core", c, re.I): s += 3
    if re.search(r"問題 2|根本分歧|disagree|divergence", c, re.I): s += 3
    if re.search(r"問題 3|深度問題|10.*question", c, re.I): s += 3
    if re.search(r"深入|deep dive|Deep Dive", c, re.I): s += 3
    if re.search(r"解答|solution|Solution", c, re.I): s += 3
    return min(s, 15)

def gate3_citations(c):
    sc = set(SCHOLAR_HINT.findall(c))
    yr = YEAR_HINT.findall(c)
    if len(sc) >= 8 and len(yr) >= 5: return 15
    if len(sc) >= 5 and len(yr) >= 3: return 12
    if len(sc) >= 3: return 8
    if len(sc) >= 1: return 4
    return 0

def gate4_specificity(c):
    eq = re.findall(r"\$\$.*\$\$|\$[^$\n]+\$", c)
    nu = re.findall(r"\b\d+\.?\d*\b", c)
    if len(eq) >= 8 and len(nu) >= 30: return 15
    if len(eq) >= 5 and len(nu) >= 15: return 12
    if len(eq) >= 3 and len(nu) >= 10: return 8
    if len(eq) >= 1: return 4
    return 0

def gate5_bilingual(c):
    cn = re.findall(r"[\u4e00-\u9fff]", c)
    if len(cn) >= 500: return 10
    if len(cn) >= 200: return 7
    if len(cn) >= 100: return 4
    return 0

def gate6_no_placeholder(c):
    h = sum(1 for p in TEMPLATE_MARKERS if re.search(p, c, re.I | re.M))
    return 10 if h == 0 else 6 if h == 1 else 3 if h <= 3 else 0

def gate7_mermaid(c):
    b = re.findall(r"```mermaid", c)
    if len(b) >= 5: return 10
    if len(b) >= 3: return 6
    if len(b) >= 1: return 3
    return 0

def gate8_solutions(c):
    n = re.findall(r"(?:^|\n)\s*\d+[\.)\s]\s+\S", c)
    if len(n) >= 30: return 10
    if len(n) >= 20: return 7
    if len(n) >= 12: return 5
    if len(n) >= 6: return 3
    return 0

def gate9_deep_dives(c):
    d = re.findall(r"(?:深入\s*\d|Deep\s+Dive\s*[IVX\d]|##\s*\d+\.\s+\S|###\s*\d+\.\s+\S)", c, re.I)
    if len(d) >= 5: return 5
    if len(d) >= 3: return 3
    if len(d) >= 1: return 1
    return 0

def gate10_no_template(c):
    bad = re.findall(r"T\d\s*—\s*(Core|Methods|Applications)", c)
    return 5 if len(bad) == 0 else 3 if len(bad) <= 2 else 0


def review(fp):
    c = Path(fp).read_text(encoding="utf-8")
    gates = {
        "G1_length": gate1_length(c), "G2_format": gate2_format(c),
        "G3_citations": gate3_citations(c), "G4_specificity": gate4_specificity(c),
        "G5_bilingual": gate5_bilingual(c), "G6_no_placeholder": gate6_no_placeholder(c),
        "G7_mermaid": gate7_mermaid(c), "G8_solutions": gate8_solutions(c),
        "G9_deep_dives": gate9_deep_dives(c), "G10_no_template": gate10_no_template(c),
    }
    total = sum(gates.values())
    decision = "APPROVED" if total >= 85 else "REVISE" if total >= 70 else "REJECT"
    return {"file": fp, "score": total, "decision": decision, "gates": gates, "lines": c.count("\n")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--course"); p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    if a.course:
        r = review(a.course)
        print(f"\n{r['file']}\n  Score: {r['score']}/100  Decision: {r['decision']}\n  Lines: {r['lines']}")
        for k, v in r["gates"].items():
            print(f"    {k:25s} {v:3d}")
        return r["decision"]
    
    if a.all:
        cfs = []
        for r, _, fs in os.walk("."):
            if any(x in r for x in (".git", "_agents", "_pipeline", "__pycache__", "node_modules", ".skills")):
                continue
            for f in fs:
                if f.endswith(".md") and not f.startswith("00_") and f not in ("README.md", "AGENTS.md", "STUDY_PLAN.md", "COURSE_INDEX.md", "Master_Tracking.md"):
                    cfs.append(os.path.join(r, f))
        
        results = []; dc = {"APPROVED": 0, "REVISE": 0, "REJECT": 0}
        for f in sorted(cfs):
            r = review(f); results.append(r); dc[r["decision"]] += 1
            if r["decision"] != "APPROVED":
                m = "⚠️" if r["decision"] == "REVISE" else "❌"
                print(f"{m} {r['score']:3d}  {f}  [{r['decision']}]")
        
        print(f"\n{'='*60}\nTotal: {len(results)} | APPROVED: {dc['APPROVED']} | REVISE: {dc['REVISE']} | REJECT: {dc['REJECT']}")
        if a.json:
            os.makedirs("_pipeline", exist_ok=True)
            with open("_pipeline/review.json", "w", encoding="utf-8") as fp:
                json.dump(results, fp, indent=2, ensure_ascii=False)
            print(f"\nDetailed report: _pipeline/review.json")


if __name__ == "__main__":
    main()
