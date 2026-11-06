#!/usr/bin/env python3
"""M5 retrospective integrity audit of held-out ORRAM postroute evidence.

Purpose: catch omitted or unconstrained path/metadata comparisons before
faculty reporting. This audits preserved evidence; it does not claim signoff
DRC/LVS, CTS, or PVT closure.
"""
import csv, hashlib, json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
modes = ("ring24", "serpentine_tile", "dma_stride")
report_names = (
    "top.sdc", "routed.odb", "routed.def", "routed.spef",
    "placed.def", "routed_read_path.rpt", "routed_overall.rpt",
    "routed_worst_slack.rpt", "read_reg_to_reg.rpt",
    "setup_check.rpt", "routing.log", "placement.log",
    "routed_flow_status.txt", "seed_status.txt",
)
def read(path):
    if not path.exists() or path.stat().st_size <= 0:
        raise ValueError(f"Missing or empty evidence: {path}")
    return path.read_text(errors="replace")

def first_path(path):
    content = read(path)
    if "Startpoint:" not in content or "Endpoint:" not in content:
        raise ValueError(f"No STA path in {path}")
    piece = "Startpoint:" + content.split("Startpoint:", 1)[1].split("Startpoint:", 1)[0]
    start = re.search(r"(?m)^Startpoint:\s*([^\n]+)", piece)
    end = re.search(r"(?m)^Endpoint:\s*([^\n]+)", piece)
    slack = re.search(r"(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((MET|VIOLATED)\)", piece)
    if not (start and end and slack):
        raise ValueError(f"No complete setup STA path in {path}")
    return dict(start=start.group(1).split(" (")[0],
                end=end.group(1).split(" (")[0],
                slack_ns=float(slack.group(1)),
                slack_status=slack.group(2))

rows = []
pairs = []
warnings = []
failures = []
for size in ("32x8", "32x16"):
    width = int(size.split("x")[1])
    for mode in modes:
        for seed in (11,23):
            current = {}
            for arch in ("row","word"):
                p = root / size / "integration" / arch / mode / f"s{seed}"
                found = {}
                for name in report_names:
                    file = p/name
                    if not file.exists():
                        failures.append(f"{size}/{mode}/s{seed}/{arch}: missing {name}")
                        continue
                    found[name] = file.stat().st_size
                    if name != "setup_check.rpt" and file.stat().st_size == 0:
                        failures.append(f"{size}/{mode}/s{seed}/{arch}: empty {name}")
                if len(found) != len(report_names):
                    continue
                if "ROUTED_AND_SPEF_IMPORTED" not in read(p/"routed_flow_status.txt"):
                    failures.append(f"{p}: routed SPEF import marker absent")
                if f"SEED_SUPPORTED:{seed}" not in read(p/"seed_status.txt"):
                    failures.append(f"{p}: verified random placement seed marker absent")
                sdc = read(p/"top.sdc")
                for command in ("create_clock", "set_input_delay", "set_output_delay",
                                "set_clock_uncertainty"):
                    if command not in sdc:
                        failures.append(f"{p}: SDC missing {command}")
                checks = read(p/"setup_check.rpt")
                if re.search(r"(?i)unconstrained endpoints|no clock|no input delay|no output delay",checks):
                    warnings.append(f"{p}: placement check_setup contains potential unconstrained-path warning; manual Tcl check needed")
                try:
                    read_path = first_path(p/"routed_read_path.rpt")
                    overall_path = first_path(p/"routed_overall.rpt")
                    place_path = first_path(p/"read_reg_to_reg.rpt")
                except ValueError as exc:
                    failures.append(str(exc))
                    continue
                if not read_path["start"].startswith("u_addrff_") or not read_path["end"].startswith("u_capture_"):
                    failures.append(f"{p}: wrong targeted read path class: {read_path}")
                if overall_path["slack_ns"] > read_path["slack_ns"] + 0.00015:
                    failures.append(f"{p}: whole-design worst path is better than constrained read path")
                if abs(overall_path["slack_ns"]-read_path["slack_ns"]) > 0.00015:
                    warnings.append(f"{p}: targeted read-path slack differs from whole-design worst slack")
                row = {
                    "size":size,"mode":mode,"seed":seed,"arch":arch,
                    "read_slack_ns":read_path["slack_ns"],
                    "overall_slack_ns":overall_path["slack_ns"],
                    "placement_read_slack_ns":place_path["slack_ns"],
                    "read_launch":read_path["start"],"read_endpoint":read_path["end"],
                    "overall_launch":overall_path["start"],"overall_endpoint":overall_path["end"],
                    "sdc_sha256":hashlib.sha256(sdc.encode()).hexdigest(),
                    "spef_bytes":found["routed.spef"],
                    "routed_odb_bytes":found["routed.odb"],
                    "route_drc_bytes":(p/"route_drc.rpt").stat().st_size if (p/"route_drc.rpt").exists() else None,
                }
                rows.append(row)
                current[arch]=row
            if set(current) == {"row","word"}:
                a,b=current["row"],current["word"]
                if a["sdc_sha256"] != b["sdc_sha256"]:
                    failures.append(f"{size}/{mode}/s{seed}: row and word have different serialized SDCs")
                pairs.append({
                    "size":size,"mode":mode,"seed":seed,
                    "row_minus_word_read_slack_ps":round(1000*(a["read_slack_ns"]-b["read_slack_ns"]),3),
                    "row_minus_word_overall_slack_ps":round(1000*(a["overall_slack_ns"]-b["overall_slack_ns"]),3),
                    "read_winner":"row" if a["read_slack_ns"]>b["read_slack_ns"] else "word" if b["read_slack_ns"]>a["read_slack_ns"] else "tie",
                    "whole_design_winner":"row" if a["overall_slack_ns"]>b["overall_slack_ns"] else "word" if b["overall_slack_ns"]>a["overall_slack_ns"] else "tie",
                    "same_winner":(a["read_slack_ns"]>b["read_slack_ns"])==(a["overall_slack_ns"]>b["overall_slack_ns"]) if a["read_slack_ns"]!=b["read_slack_ns"] and a["overall_slack_ns"]!=b["overall_slack_ns"] else False
                })
                if not pairs[-1]["same_winner"]:
                    warnings.append(f"{size}/{mode}/s{seed}: targeted-read and whole-design architecture winner differ")

if len(rows)!=24:
    failures.append(f"Only {len(rows)}/24 expected architecture samples verified")
if len(pairs)!=12:
    failures.append(f"Only {len(pairs)}/12 expected matched comparison pairs verified")

if rows:
    with (out/"sample_integrity.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
if pairs:
    with (out/"paired_integrity.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(pairs[0]))
        writer.writeheader();writer.writerows(pairs)

summary = {
    "scope":"Retrospective serialized artifacts only; no fresh physical optimization",
    "samples_verified":len(rows),"pairs_verified":len(pairs),
    "same_read_vs_whole_winner_count":sum(p["same_winner"] for p in pairs),
    "read_vs_whole_disagreements":[p for p in pairs if not p["same_winner"]],
    "warnings":warnings,"failures":failures,
    "known_unverified":"No full post-route clock-tree signoff; no DRC/LVS/EM/IR, multi-corner, power, or independent validation of all unconstrained endpoints. The rerun OpenSTA signoff-style review is a separate gate.",
    "scientific_interpretation":"Previously published experimental scorecards use targeted address-register-to-capture setup slack; never silently present as overall worst setup improvement."
}
(out/"integrity_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
if failures:
    raise SystemExit("M5_CHECK_FAIL: evidence consistency conditions not met; investigate")
print("M5_SERIALIZED_EVIDENCE_AUDIT_COMPLETE")
