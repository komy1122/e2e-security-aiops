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

The repository currently documents the research direction. Components listed above should be treated as planned work unless corresponding code, tests, or experiment artifacts are present in the repository.

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
