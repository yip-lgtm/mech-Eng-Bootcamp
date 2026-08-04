#!/usr/bin/env python3
"""Multi-Agent Pipeline Orchestrator"""
import os, sys, argparse, subprocess
from pathlib import Path

PIPELINE_ROOT = Path(__file__).parent
AGENTS_ROOT = PIPELINE_ROOT.parent / "_agents"


def run_agent(agent_name, course):
    print(f"\n→ Agent: {agent_name}")
    cmd = ["python3", str(AGENTS_ROOT / agent_name / "lookup.py"), "--course", course]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ✗ {agent_name} failed:\n{r.stderr}")
        return False
    print(f"  ✓ {agent_name} OK")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--course")
    p.add_argument("--all", action="store_true")
    a = p.parse_args()
    
    if a.course:
        print(f"Pipeline: {a.course}\n{'='*60}")
        for ag in ["researcher", "data_extractor", "engineer", "diagram", "professor_supervisor"]:
            if not run_agent(ag, a.course):
                print(f"\nPipeline FAILED at {ag}"); sys.exit(1)
        print(f"\n✓ Pipeline complete for {a.course}")
    elif a.all:
        subprocess.run(["python3", str(AGENTS_ROOT / "professor_supervisor" / "review.py"), "--all"])


if __name__ == "__main__":
    main()
