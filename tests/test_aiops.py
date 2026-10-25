import unittest

from aiops import correlate


def event(event_id="w1", source="waf", timestamp="2026-10-25T00:00:00Z", entity="demo-service"):
    return dict(event_id=event_id, source=source, timestamp=timestamp, entity=entity)


class CorrelationTests(unittest.TestCase):
    def test_normalizes_offsets_sorts_and_preserves_provenance(self):
        result = correlate([event("a1", "application", "2026-10-25T09:01:00+09:00"), event()])
        self.assertEqual(result, [{
            "schema_version": "1.0", "entity": "demo-service",
            "start": "2026-10-25T00:00:00Z", "end": "2026-10-25T00:01:00Z",
            "event_ids": ["w1", "a1"], "sources": ["application", "waf"],
            "evidence_status": "correlated", "root_cause": None,
        }])

    def test_inclusive_anchored_window_does_not_chain(self):
        rows = [event(), event("a1", "application", "2026-10-25T00:05:00Z"),
                event("f1", "firewall", "2026-10-25T00:10:00Z")]
        result = correlate(rows)
        self.assertEqual([r["event_ids"] for r in result], [["w1", "a1"], ["f1"]])

    def test_different_entities_do_not_merge(self):
        self.assertEqual(len(correlate([event(), event("a1", "application", entity="other")])), 2)

    def test_single_source_is_insufficient_even_with_two_events(self):
        self.assertEqual(correlate([event(), event("w2")])[0]["evidence_status"], "insufficient_evidence")

    def test_empty_input_has_no_invented_incident(self):
        self.assertEqual(correlate([]), [])

    def test_equal_timestamps_are_order_independent(self):
        rows = [event(), event("a1", "application")]
        self.assertEqual(correlate(rows), correlate(rows[::-1]))

    def test_rejects_missing_unknown_and_empty_fields(self):
        rows = [event(), event(), event()]
        del rows[0]["source"]
        rows[1]["raw_log"] = "not part of contract"
        rows[2]["entity"] = " "
        for row in rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                correlate([row])

    def test_rejects_naive_or_malformed_time(self):
        for timestamp in ["2026-10-25T00:00:00", "invalid", "2026-13-01T00:00:00Z"]:
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                correlate([event(timestamp=timestamp)])

    def test_rejects_unknown_source_and_duplicate_ids(self):
        for rows in [[event(source="unknown")], [event(), event()]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                correlate(rows)

    def test_rejects_utc_conversion_outside_datetime_range(self):
        for timestamp in ["0001-01-01T00:00:00+01:00", "9999-12-31T23:59:59-01:00"]:
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                correlate([event(timestamp=timestamp)])

    def test_rejects_non_array_input_and_non_object_rows(self):
        for rows in [None, {}, "events", [None], [1]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                correlate(rows)

    def test_rejects_invalid_window(self):
        for window in [-1, True, 1.5, "300"]:
            with self.subTest(window=window), self.assertRaises(ValueError):
                correlate([], window_seconds=window)

    def test_zero_window_only_groups_simultaneous_events(self):
        rows = [event(), event("a1", "application"), event("f1", "firewall", "2026-10-25T00:00:01Z")]
        self.assertEqual([r["event_ids"] for r in correlate(rows, window_seconds=0)], [["a1", "w1"], ["f1"]])


if __name__ == "__main__":
    unittest.main()
