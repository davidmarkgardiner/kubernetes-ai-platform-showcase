from __future__ import annotations

import argparse
from pathlib import Path

from .engine import run, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path("policy_evidence/fixtures/policy-set.json"))
    parser.add_argument("--plan", type=Path, default=Path("policy_evidence/fixtures/plan.json"))
    parser.add_argument("--out", type=Path, default=Path("policy_evidence/out"))
    args = parser.parse_args()
    bundle, spans = run(args.fixtures, args.plan)
    write_outputs(bundle, spans, args.out)
    summary = bundle["summary"]
    print(
        f"run {bundle['run_id']}: {summary['read_calls']} read calls, "
        f"{summary['denials']} denial (403), {summary['plan_deviations']} deviations"
    )


if __name__ == "__main__":
    main()
