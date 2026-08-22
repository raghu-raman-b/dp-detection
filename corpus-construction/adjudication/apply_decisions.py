#!/usr/bin/env python3
"""
apply_decisions.py -- write the adjudication decisions back into labeled_data.

    python apply_decisions.py        # DRY_RUN=True: prints the diff, writes nothing

Set DRY_RUN = False below to actually write. It snapshots both source files to a
timestamped folder first, every time, so any run is undoable by copying back.

What it touches on a changed row: the 29 binary label columns, `labels`, `labels_str`,
`none`, plus adj_* provenance fields. Nothing else. Field order is preserved (json round
trips dict order) and the separator style is sniffed per file, so the git diff shows the
rows that changed rather than every line reformatted.

Rows the tool left undecided are skipped and counted. Decided-but-unchanged rows get the
adj_* provenance fields only, so the record shows the row was checked and upheld.
"""

from __future__ import annotations

import json
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_input import LABEL_CODES

# ============================== CONFIG ==============================
DRY_RUN        = False                     # flip to False to write

DECISIONS_FILE = "../decisions/decisions.jsonl"   # exported from dp_adjudicator.html
DATA_DIR       = "../labeled_data"
SNAPSHOT_ROOT  = "../labeled_data_pre_adjudication"
CHANGELOG      = "../decisions/changelog.txt"

# Written onto every decided row so the corpus records what was checked and by what.
STAMP_FIELDS   = True
# ====================================================================

GROUP_NAME = {
    "T": "Temporal", "M": "Monetary", "S": "Social",
    "P": "Psychological", "Tech": "Technical",
}

# code -> the display name the labeller wrote into labels_str. Mirrors CONFIG.groups in
# dp_adjudicator.html / dp_labeler.html. These cannot be derived from the code (the code
# strips punctuation: "Fear of Missing Out (FOMO)" -> S_FearOfMissingOutFOMO), so the map
# is explicit and must stay in step with the tool.
DISPLAY = {
    "T_PlayingByAppointment": "T: Playing by Appointment",
    "T_DailyRewards": "T: Daily Rewards",
    "T_Grinding": "T: Grinding",
    "T_Advertisement": "T: Advertisement",
    "T_InfiniteTreadmill": "T: Infinite Treadmill",
    "T_MandatoryMarathon": "T: Mandatory Marathon",
    "M_PayToProgress": "M: Pay to Progress",
    "M_IntermediateCurrency": "M: Intermediate Currency",
    "M_DeceptiveLuxury": "M: Deceptive Luxury",
    "M_RecurringFee": "M: Recurring Fee",
    "M_Gambling": "M: Gambling",
    "M_PowerCreep": "M: Power Creep",
    "M_WasteAversion": "M: Waste Aversion",
    "M_EasyToPurchase": "M: Easy to Purchase",
    "M_UIMisdirection": "M: UI Misdirection",
    "M_NeverEndingLure": "M: Never-Ending Lure",
    "S_ForcedFellowship": "S: Forced Fellowship",
    "S_FriendSpamImpersonation": "S: Friend Spam / Impersonation",
    "S_Reciprocity": "S: Reciprocity",
    "S_EncouragesAntiSocialBehavior": "S: Encourages Anti-Social Behavior",
    "S_FearOfMissingOutFOMO": "S: Fear of Missing Out (FOMO)",
    "S_Competition": "S: Competition",
    "P_EasyToGetHardToLose": "P: Easy to Get Hard to Lose",
    "P_CompleteTheCollection": "P: Complete the Collection",
    "P_IllusionOfControl": "P: Illusion of Control",
    "P_AestheticManipulation": "P: Aesthetic Manipulation",
    "P_OptimismAndFrequencyBiases": "P: Optimism and Frequency Biases",
    "P_RewardMania": "P: Reward Mania",
    "Tech_FragmentedDownloads": "Tech: Fragmented Downloads",
}
_missing = [c for c in LABEL_CODES if c not in DISPLAY]
if _missing:
    sys.exit(f"DISPLAY map is out of step with LABEL_CODES, missing: {_missing}")


def labels_str_for(codes: list[str]) -> str:
    """Rebuild labels_str exactly as the labelling tool writes it."""
    return "; ".join(DISPLAY[c] for c in codes)


def sniff_separators(first_line: str) -> tuple[str, str]:
    """Match the file's existing json spacing so unchanged lines stay byte-identical."""
    return (", ", ": ") if '", "' in first_line or '": "' in first_line else (",", ":")


def main() -> None:
    dec_path = Path(DECISIONS_FILE)
    if not dec_path.exists():
        sys.exit(f"no decisions file at {dec_path.resolve()}\n"
                 f"Export one from dp_adjudicator.html first.")

    decisions = [json.loads(l) for l in
                 dec_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    by_file: dict[str, dict[int, dict]] = {}
    skipped_undecided = 0
    for d in decisions:
        if not int(d.get("decided", 0)):
            skipped_undecided += 1
            continue
        f, ln = d.get("source_file"), d.get("source_line")
        if not f or not isinstance(ln, int):
            sys.exit(f"decision without source_file/source_line: {d.get('row_uid')}")
        if ln in by_file.setdefault(f, {}):
            sys.exit(f"two decisions target {f}:{ln} — export again from one session")
        by_file[f][ln] = d

    data_dir = Path(DATA_DIR)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap_dir = Path(SNAPSHOT_ROOT) / stamp

    changelog: list[str] = []
    totals = Counter()
    per_label = Counter()

    for fname, per_line in sorted(by_file.items()):
        src = data_dir / fname
        if not src.exists():
            sys.exit(f"decisions reference {fname}, which is not in {data_dir.resolve()}")

        raw_lines = src.read_text(encoding="utf-8").splitlines()
        seps = sniff_separators(raw_lines[0] if raw_lines else "")
        out_lines: list[str] = []

        for i, line in enumerate(raw_lines, start=1):
            if not line.strip():
                out_lines.append(line)
                continue
            d = per_line.get(i)
            if d is None:
                out_lines.append(line)
                continue

            row = json.loads(line)
            rid = str(row.get("review_id", ""))
            if d.get("review_id") and d["review_id"] != rid:
                sys.exit(f"{fname}:{i} review_id mismatch: decisions say {d['review_id']}, "
                         f"file says {rid}. The labels file changed since the run; rerun "
                         f"build_input.py and the adjudication.")

            final = [c for c in LABEL_CODES if c in (d.get("final_labels") or [])]
            orig = [c for c in LABEL_CODES if c in (d.get("original_labels") or [])]
            changed = set(final) != set(orig)

            if changed:
                for c in LABEL_CODES:
                    row[c] = 1 if c in final else 0
                row["labels"] = final
                row["labels_str"] = labels_str_for(final)
                row["none"] = 0 if final else 1
                totals["changed"] += 1
                for c in set(orig) - set(final):
                    per_label[f"-{c}"] += 1
                for c in set(final) - set(orig):
                    per_label[f"+{c}"] += 1
                changelog.append(
                    f"{fname}:{i}  {rid}\n"
                    f"    before : {orig or ['NONE']}\n"
                    f"    after  : {final or ['NONE']}\n"
                    f"    removed: {sorted(set(orig) - set(final)) or '-'}\n"
                    f"    added  : {sorted(set(final) - set(orig)) or '-'}\n"
                    f"    model  : {d.get('adj_model','')} {d.get('adj_run_tag','')}"
                    f"  contested={d.get('contested')}"
                    f"  contract_errors={d.get('adj_contract_errors')}\n"
                    f"    note   : {d.get('note','') or '-'}\n")
            else:
                totals["upheld"] += 1

            if STAMP_FIELDS:
                row["adj_checked"] = 1
                row["adj_changed"] = 1 if changed else 0
                row["adj_model"] = d.get("adj_model", "")
                row["adj_run_tag"] = d.get("adj_run_tag", "")
                row["adj_prompt_sha256"] = d.get("adj_prompt_sha256", "")
                row["adj_contested"] = int(d.get("contested", 0) or 0)
                row["adj_note"] = d.get("note", "")
                row["adj_decided_at"] = d.get("decided_at", "")

            out_lines.append(json.dumps(row, ensure_ascii=False, separators=seps))

        missing = sorted(set(per_line) - set(range(1, len(raw_lines) + 1)))
        if missing:
            sys.exit(f"{fname}: decisions point at line(s) {missing}, file has "
                     f"{len(raw_lines)}. Rerun build_input.py against the current files.")

        if not DRY_RUN:
            snap_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, snap_dir / fname)
            src.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    print(f"decisions read : {len(decisions)}")
    print(f"  undecided, skipped : {skipped_undecided}")
    print(f"  decided, upheld    : {totals['upheld']}")
    print(f"  decided, changed   : {totals['changed']}")
    if per_label:
        print("\nlabel deltas:")
        for k, v in sorted(per_label.items(), key=lambda kv: -kv[1]):
            print(f"  {k:<34} {v:>4}")

    if DRY_RUN:
        print("\nDRY_RUN is True. Nothing was written.")
        print("Read the changes above, then set DRY_RUN = False and rerun.")
        if changelog:
            print("\n--- first 5 changes ---")
            print("\n".join(changelog[:5]))
    else:
        cl = Path(CHANGELOG)
        cl.parent.mkdir(parents=True, exist_ok=True)
        cl.write_text(
            f"adjudication applied {stamp}\n"
            f"snapshot: {snap_dir.resolve()}\n"
            f"decisions: {dec_path.resolve()}\n"
            f"upheld {totals['upheld']}, changed {totals['changed']}, "
            f"skipped {skipped_undecided}\n\n" + "\n".join(changelog),
            encoding="utf-8")
        print(f"\nwrote {len(by_file)} file(s). snapshot: {snap_dir}")
        print(f"changelog: {cl}")
        print("\nRerun your corpus stats: prevalence and the co-occurrence lifts have moved.")


if __name__ == "__main__":
    main()