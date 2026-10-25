# Explainable AIOps — version and PoC gate v0.2
**Canonical repository:** early research README only, little/no executable testbed verified here; **research audit:** v0.2. Graduation NetworkOps is a distinct implementation reference, not proof of this repo's runtime.
**Unit:** operator × incident (human study) and isolated incident (technical test). Explanation fidelity, perceived trust, calibrated reliance and MTTR are separate constructs.
**PoC feasible:** synthetic WAF/firewall/application log normalization + timeline correlation + provenance-backed RCA descriptions; compare rule-based vs explanatory trace; show an operator UI mock with explicit 'no evidence' state.
**Acceptance:** versioned schema & source timestamps, held-out incident root-cause labels, top-k localization and unsupported-claim rate, missing-source robustness, severity-stratified calibration and counterexamples. Human reliance/trust conclusions require randomized operator sample, IRB review if applicable.
**Next gate:** add standalone executable minimal parser/tests on feature branch before declaring implementation.

## Version rule / evidence limits
This is **cross-system audit protocol v0.2 (2026-10-25)**, **not** a promotion of the research model, preregistration, code release, empirical maturity, IRB status, or published finding. Existing program IDs, frozen hypotheses, and open Draft PRs remain unchanged. Separate observed record, prior run record, proposal, and independent rerun. Source: [9-program register](https://app.notion.com/p/404d67f01bc181608467ff4178db2616).
No client data, personal data, research participant data, API secrets, or licensed full text may enter GitHub.