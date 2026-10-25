# E2E Security AIOps

A research and prototype project exploring how heterogeneous security and operational events can be normalized, correlated, and analyzed for AIOps-oriented incident understanding.

## Research Problem

Enterprise incidents rarely appear in a single log source. WAF, DLP, firewall, application, infrastructure, and observability systems may each expose only part of an incident.

This project explores the pipeline:

```text
WAF / DLP / Firewall / Application / Operations
                    ↓
              Normalization
                    ↓
             Event Correlation
                    ↓
          Anomaly / Pattern Analysis
                    ↓
             Incident Context
                    ↓
                  AIOps
```

## Research Questions

- How can heterogeneous security and operational events be represented in a common event model?
- Which temporal, entity, and topology relationships are useful for end-to-end correlation?
- How should anomaly signals be combined with deterministic security evidence?
- How can an AIOps system preserve provenance and evidence for operator verification?

## Planned Components

- source adapters
- common event schema
- timestamp and entity normalization
- correlation rules
- anomaly-detection experiments
- incident timeline reconstruction
- evaluation metrics
- reproducible sample/synthetic data

## Current Status

**Early research/prototype stage.**

This branch adds a standalone synthetic correlation baseline and automated tests. Production adapters, anomaly detection, causal RCA, an operator UI and human evaluation remain planned. A passing synthetic test is not evidence of operational security effectiveness or operator trust.

## Run the Synthetic Baseline

Python 3.11+; no third-party dependencies or service credentials required.

```sh
python -m unittest discover -s tests -v
python aiops.py examples/synthetic-events.json
python aiops.py examples/synthetic-events.json --window-seconds 60
```

Input is a JSON array. Each event has exactly four nonempty string fields:

```json
{"event_id":"demo-1","source":"waf","timestamp":"2026-10-25T00:00:00Z","entity":"demo-service"}
```

- Sources: `waf`, `dlp`, `firewall`, `application`, `operations`. Event IDs are unique across the input.
- Offset-aware ISO timestamps normalize to UTC; naive timestamps and unknown/missing fields are rejected. This is a canonical input contract, not a parser for vendor raw logs.
- Same-entity events group within an inclusive window measured from the group's first event (default 300 seconds). Windows do not extend through chained events. Input order does not affect results.
- Every timeline retains event IDs and distinct sources. Two or more sources yield `correlated`; one source yields `insufficient_evidence`. Empty input produces an empty list.
- Correlation means temporal/entity co-occurrence. `root_cause` is always `null`; this baseline does not infer causation, severity, anomalies or recommended actions.
- Input errors exit with code 2 and no partial JSON output. Data is read locally; there are no outbound requests or remediation actions.

The `Synthetic correlation checks` workflow runs unit tests and the example on Linux/Windows with Python 3.11–3.13. Consult the exact PR SHA and workflow run before claiming remote CI passed.

## Evidence and Integration Status

See [2026-10-25 implementation and integration audit](docs/implementation-integration-audit-2026-10-25.md) for research boundaries, connector coverage and next gates. External app availability does not mean an ingestion or synchronization adapter exists in this repository.

## Evaluation Principles

Candidate evaluation dimensions include:

- detection / correlation precision and recall
- false-positive rate
- time-to-detection
- root-cause localization quality
- incident reconstruction completeness
- operator verification effort

Metrics will only be reported when an executable experiment and ground truth are available.

## Research Connection

This project represents the operational-AI stream of the broader portfolio:

```text
Network / Security Operations
          ↓
        AIOps
          ↓
Human–AI Operational Decision Support
          ↓
AI Governance / Decision Authority
```

Related project: [Enterprise AI Observatory](https://github.com/komy1122/enterprise-ai-observatory)

## Data and Licensing

Do not commit production logs, credentials, personal information, or proprietary customer data.

Experiments should use synthetic, public, or explicitly authorized datasets, with provenance and licensing documented before reuse.
