# Synthetic correlation implementation plan

Goal: satisfy the existing standalone parser/test gate using synthetic data only.

Architecture: a standard-library Python module validates a versioned event contract, normalizes aware ISO timestamps to UTC and groups same-entity events within an inclusive window anchored at the first event. Every timeline retains source event IDs. Two sources provide correlation evidence, never causal proof. No network calls or actions.

Files: `aiops.py`, `tests/test_aiops.py`, `examples/synthetic-events.json`, `.github/workflows/synthetic-checks.yml`, README and evidence audit.

- [x] Write tests for UTC ordering, provenance, window boundaries, entity separation, missing evidence and invalid inputs; observe failure before implementation.
- [x] Implement validation, deterministic correlation and JSON CLI using Python 3.11+ standard library.
- [x] Run the tests and example, including nonzero CLI rejection of invalid input.
- [ ] Add Windows/Linux CI, document integration coverage and research limitations, review diff and push the existing Draft PR branch without merging.
