# MSP incident-to-decision — E2E Security AIOps
Checked: 2026-10-27. Status: proposed integration, not production incident frequency, completed studies or accepted publications.
Notion MSP registry: https://app.notion.com/p/405d67f01bc181e0a324f7eed9de0613
Notion journal & literature registry: https://app.notion.com/p/405d67f01bc18141a170e9fc6ebbc78c

## Research evidence rules
- 96 items are candidate decision problems, NOT observed incident counts or repeat frequencies.
- E0 synthetic; E1 conversation recollection; E2 correspondence/document existence; E3 authorized de-identified event log; E4 independently verified.
- Separate incident, decision, action, and outcome identifiers; record access authorization and provenance.
- No client identities, configurations, proprietary logs, contact details or contract files may be committed.
- Venue fit is a candidate assessment; "submitted" requires submission receipt, "accepted" requires decision evidence.

## Candidate events
MSP-02-02: firewall logs show no block in a connectivity failure; NAC/endpoint security should be investigated but the root cause is NOT established. MSP-01 group alert triage; MSP-06-01 access exception evaluation.
## Data contract
For authorized sanitized data only: event_id, incident_id, decision_id, source_type, observed_at_utc, ingestion_at_utc, pseudonymous_service_id, event_class, severity, source_digest, evidence_grade, ground_truth_origin. Reject unexpected fields; hide secrets and endpoint identities before any external agent use.
## Baselines
Compare firewall-only, sequential human diagnosis, rules, and heterogeneous log correlation. Ground-truth provenance, precision/recall, false diagnosis cost, time-to-triage and SLA must be defined before results are claimed.
## Next
Test Pydantic v2 structured ingestion contract (Context7 docs verified) on synthetic records, then permission gate for real events.
