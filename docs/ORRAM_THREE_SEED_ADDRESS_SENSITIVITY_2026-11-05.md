# Milestone 1C — Three-seed verification of address-pin sensitivity

**Date:** November 5, 2026

## Verdict — PASS within constrained exploratory study

[Successful physical sensitivity run 42128929892](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128929892), artifact `orram-memory-sensitivity-three-seed-42128929892`.

Reopened the **same existing** successful physical results for 32×8 and 32×16 XOR-wrapped ORRAM row/word decoders (seed 11, seed 23, seed 37) from GitHub Actions 42078118809 and 42078118831. The analysis read routed ODB, original SDC and routed SPEF, and used OpenSTA pinned to the original OpenROAD Docker image. No new placement, route, or optimization was performed.

Collected **420** constrained timing suffix path records. The matched-output comparisons cover **30 width × address-context × seed × capture-output combinations**, each with five memory address pins, totalling **150 paired row-versus-word suffix comparisons**.

- **30/30 matched-output cases:** both low-order address bits A0 and A1 have lower downstream path delay in the **row decoder** design.
- **30/30 matched-output cases:** both high-order address bits A3 and A4 have lower downstream path delay in the **word decoder** design.
- A2 has a smaller, variable preference and is not declared to favor either architecture.

Equivalently, all **60** low-bit row/word comparisons favor row and all **60** high-bit comparisons favor word; there are **30** intermediate A2 comparisons of varying sign.

This is a robust observed **address-dependent timing asymmetry under three independently perturbed placements**. It supplies a concrete mechanistic explanation for the previous context-dependent rank reversal: a circuit with different critical address cones can prefer a different decoder even when the memory function is the same.

## Measurement method

The flattened structural RAM does not preserve an abstract hierarchical address port. The boundary is the final XOR-driver `Z` pin feeding each `addr_mem[bit]` net. In a timing report constrained through that output and terminating at the same named capture register for row and word, subtract:

`RAM-side path suffix = arrival at capture register D − time at final address XOR driver Z`.

This excludes upstream source FF and XOR logic and includes the final address net, RAM decoder, selection/output logic and capture net. The suffix is **not** a standalone Liberty arc delay; it depends on physical driver slew, load, selected internal path and routing.

Matched endpoints were Q0 and Q7 for 32×8, and Q0, Q7, Q14 for 32×16. There are 2 contexts (balanced, late_low) and 3 seeds, yielding 12 cases of 32×8 and 18 cases of 32×16, or 30 matched-output cases total.

## Interpretation and scientific limits

These 30 cases come from two handcrafted XOR cones and three physical-placement seeds. Do not interpret 30/30 as predictive accuracy on independent workloads. They are repeated correlated tests of a specific design family.

The result makes the *physical mechanism more plausible*, but does not prove that the decoder gates alone caused the effect, because output-selection and storage read path, sensitized word, edge polarity, signal slew, parasitic loading and placement may differ between architectures.

Independent synthesized application wrappers, new memory depths, corners/PDKs, fully constrained signoff, power and actual predictor compute overhead remain missing.

The next **research method** milestone is a pre-placement per-address timing predictor using an independently characterized library, a truly frozen holdout protocol, and an explicit compute-cost baseline. Do not train it on the same physical implementations and then call their test performance out-of-sample.

## Artifacts

- `boundary/boundary_suffix_paths.csv`: 420 complete cases, timing startpoints/endpoints, boundary-time and capture-time provenance.
- `boundary/multiseed_boundary_summary.json`: 30 fixed-output cases and low/high bit sign checks.
- Original per-case raw OpenSTA reports, audit logs and provenance manifests in the same archived Actions artifact.
- [Earlier single-seed sensitivity report](ORRAM_FIXED_ENDPOINT_SENSITIVITY_2026-11-05.md), including all initial per-output numerical differences.

**Milestone conclusion:** memory-boundary path sensitivity demonstrated and repeatable within this test family. **Novel predictor and full causal isolation remain unfinished.**
