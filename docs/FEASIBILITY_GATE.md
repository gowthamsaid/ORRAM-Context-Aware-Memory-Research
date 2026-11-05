# Feasibility gate (preregistered)

**Gate A — implementation:** two verified 32×8 ORRAM variants with identical 1RW port timing semantics and behavior, verified distinct cell connectivity, and complete STA reports.

**Gate B — contextual effect:** in at least one realistic boundary setting, context changes the measured timing-feasibility ranking relative to standalone timing, by more than 20 ps.

**Gate C — research-worthiness:** the effect survives an enclosing-circuit integration using propagated interconnect loading and matched placement/routing; comparisons include context-blind selection, structural baselines, and actual chip-level timing. Existing published approaches must be evaluated.

Outcome `GO_TO_TOP_LEVEL_INTEGRATION` is *not* a final scientific GO. It means Gate A and a screening observation justify a costly Gate C test. `NO_REVERSAL_IN_ISOLATED_BOUNDARY_SCREEN` is a null result for that screen. Any implementation failure is `BLOCKED`, not a rejection of the scientific hypothesis.

We do not claim previously unstudied context-aware memory selection. ORRAM itself and prior memory compiler literature already address surrounding system constraints.
