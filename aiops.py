"""Synthetic event correlation baseline; no causal inference or remediation."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


SOURCES = {"waf", "dlp", "firewall", "application", "operations"}
FIELDS = {"event_id", "source", "timestamp", "entity"}


def correlate(events, window_seconds=300):
    """Return UTC timelines using inclusive, first-event-anchored windows.

    Input is a JSON-compatible list of exact four-field event objects. Source
    event IDs must be globally unique. Multiple sources establish co-occurrence,
    not a root cause. All validation completes before any result is returned.
    """
    if type(window_seconds) is not int or window_seconds < 0:
        raise ValueError("window_seconds must be a nonnegative integer")
    if not isinstance(events, list):
        raise ValueError("events must be an array")
    normalized, seen = [], set()
    for row in events:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError("event must contain exactly event_id, source, timestamp, entity")
        if any(not isinstance(value, str) or not value.strip() for value in row.values()):
            raise ValueError("event fields must be nonempty strings")
        if row["source"] not in SOURCES:
            raise ValueError("unsupported event source")
        if row["event_id"] in seen:
            raise ValueError("event IDs must be unique")
        try:
            timestamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be an offset-aware ISO datetime") from None
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("timestamp must include a UTC offset")
        try:
            timestamp = timestamp.astimezone(timezone.utc)
        except OverflowError:
            raise ValueError("UTC timestamp is outside the supported date range") from None
        seen.add(row["event_id"])
        normalized.append((timestamp, row))

    normalized.sort(key=lambda item: (item[0], item[1]["entity"], item[1]["event_id"]))
    groups, active = [], {}
    for timestamp, row in normalized:
        group = active.get(row["entity"])
        if group is None or (timestamp - group[0][0]).total_seconds() > window_seconds:
            group = []
            groups.append(group)
            active[row["entity"]] = group
        group.append((timestamp, row))

    def utc(value):
        return value.isoformat().replace("+00:00", "Z")

    result = []
    for group in groups:
        sources = sorted({row["source"] for _, row in group})
        result.append({
            "schema_version": "1.0", "entity": group[0][1]["entity"],
            "start": utc(group[0][0]), "end": utc(group[-1][0]),
            "event_ids": [row["event_id"] for _, row in group], "sources": sources,
            "evidence_status": "correlated" if len(sources) > 1 else "insufficient_evidence",
            "root_cause": None,
        })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, help="synthetic event JSON array")
    parser.add_argument("--window-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        events = json.loads(args.events.read_text(encoding="utf-8"))
        result = correlate(events, args.window_seconds)
    except (OSError, ValueError) as error:
        # Avoid echoing input contents or sensitive filesystem paths into output.
        message = "cannot read input file" if isinstance(error, OSError) else (
            "invalid JSON input" if isinstance(error, json.JSONDecodeError) else str(error)
        )
        print(f"error: {message}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
