# Boundary-context ORRAM feasibility — empirical gate report

**Date:** 2026-11-05  
**Status:** **CONDITIONAL GO for a carefully controlled top-level integration experiment; NOT YET A GO for the proposed original EDA algorithm or a publication claim.**

## Reproducibility
- [Successful GitHub Actions run 42053883466](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466); [all raw artifacts](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466/artifacts/13428256326).
- Nangate45 standard-cell ORRAM 32 words × 8 bits, one read/write port, **asynchronous combinational read** (not an equivalent full synchronous FIFO).
- Row and word decoder options generated in the same pinned ORFS revision and pinned OpenROAD Docker image.
- The generated behavioral Verilog models are byte-identical; independent Icarus simulation passed the two designs against a known-content testbench.
- Mapped component histograms are identical and contain 256 DFF, 256 tri-state buffers, 160 AND2, 40 BUF, 37 INV, 32 CLKGATE cells and the same filler inventory; physical net-connection signatures differ. Equal cell counts do not imply identical electrical behavior.
- Both DEF DIEAREA records match: `(0,0) to (4560,4620)` DBU. Weights, placements and physical nets differ by architecture.
- SDC clock period 2 ns; identical per-context constraints for both architectures; estimated **placement** interconnect RC (not validated detailed-route extracted parasitics).

## Measured targeted address-to-output slack

All values are **ns**; the winner threshold used in screening is a 0.020 ns (20 ps) margin.

| External timing context | Row-decoder slack | Word-decoder slack | Preferred architecture |
|---|---:|---:|---|
| Reference (all address inputs arrive after 0.10 ns) | 1.42467 | 1.45014 | **Word** by 25.47 ps |
| Low address bits 0/1 arrive after 0.65 ns | 0.92663 | 0.90014 | **Row** by 26.49 ps |
| High address bits 3/4 arrive after 0.65 ns | 0.87467 | 0.90170 | **Word** by 27.03 ps |
| Output-load setting 0.005 → 0.050 | 1.42467 | 1.45014 | Word, **no measured slack response** |
| Output-delay setting 0.10 → 0.75 ns | 0.77467 | 0.80014 | Word, no ranking change |

The unexpected but measurable observation is the **row/word ranking reversal** under a late low-order address. Under uniform arrival assumptions, row's limiting path begins at `addr_rw[4]` while word's begins at `addr_rw[1]`. Under late low-bit conditions both limit through `addr_rw[1]`, and row has approximately 26.49 ps less intrinsic path delay. This path migration is enough to invert the preference.

**Critical nuance:** This ranking switch follows from externally changing input arrival times on fixed physical blocks. It establishes a context-sensitive timing-selection example, **not** a novel architecture, algorithm, or quantified chip-level improvement. At fixed RC, a roughly 25.47 ps extra low-bit arrival increment is sufficient for the two worst-path margins to cross (in the measured regime). This is a modest effect requiring robust follow-up, not an impressive performance gain by itself.

## Verified technical limitations
1. **Not an integrated-chip experiment.** The external environment is represented by SDC delays/loads, not surrounding logic, floorplan, macro pin placement, clock-tree interaction or full-system extracted parasitics.
2. **No multi-seed validation.** Both memory options were generated once; architectural ranking may change with placement and physical constraints. A deterministic generator gives repeatability, not population robustness.
3. **Output-load test is not informative.** The saved SDC confirms that 0.050 and 0.005 load values were applied, but reported read-path arrival and slack did not change. Investigate the output timing model/tri-state handling before using output-load claims.
4. **Physical signoff is incomplete.** The loaded Nangate45 ORFS macro LEF lacks the expected tapcell, so generation omitted tapcells and issued RAM-0022. PDN also emitted via-removal warnings. The result is a functional/timing pilot, **not DRC-clean or tapeout-ready signoff**.
5. No characterization of power, variation across timing corners, area tradeoffs beyond identical cell histograms, or comprehensive prior-art comparison against existing timing-aware memory optimizers.
6. Research hypothesis says *architecture selection for integrated designs*. Only the narrower **boundary-timing sensitivity** has been tested. No algorithm was implemented.

## Gate evaluation
- **A: Can ORRAM produce two equivalent but structurally different memory implementations?** **PASS.**
- **B: Can external timing context change a memory architecture ranking in a controlled initial test?** **PASS, with a small measured margin.**
- **C: Is top-level timing-aware selection better than standalone selection under a constrained compute/area budget?** **NOT TESTED.**
- **D: Is a specific selection method distinct from existing published approaches?** **NOT ESTABLISHED.**

**GO to the next, tightly scoped top-level integration experiment, but NO-GO to claiming original research contribution or building an optimizer yet.**

## Recommended discriminating follow-up
Integrate the two functionally identical memory variants into the **same registered surrounding circuit**. Synthesize a small asymmetric address-generation cone with a deliberate low-bit late path, plus a symmetric reference design. Match clock, I/O constraints, layout area and pin placement; re-route with proper parasitic extraction and compare **whole-chip** setup slack, path migration, area and wire burden across several seeds. Add an independent memory configuration or reference design. Test and preregister: does timing-aware selection consistently choose a configuration that a standalone selector gets wrong, after practical physical implementation?

If this effect does not survive realistic integration/variation, classify the hypothesis as a negative result and preserve the reproducible benchmark. If it does, **only then** scope the automated architecture-selection method and its comparisons with ORRAM's existing roadmap and prior EDA literature.
