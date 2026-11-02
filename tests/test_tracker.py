import unittest
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tracker import check_notices

TODAY = date(2026, 11, 2)
TEAMS = [
    {"name": "UK Sales", "categories": ["construction"], "regions": ["UK"]},
    {"name": "EU Engineering", "categories": ["manufacturing"], "regions": ["EU", "UK"]},
]
NOTICE = {"id": "D-100", "title": "Sample framework", "category": "construction",
          "region": "UK", "release_in_days": 60, "revision": 1}

class TrackerTests(unittest.TestCase):
    def test_eligible_notice_routes_to_relevant_team(self):
        alerts, state = check_notices([NOTICE], TEAMS, today=TODAY)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["team"], "UK Sales")
        self.assertEqual(state["UK Sales:D-100"], "1")

    def test_unchanged_notice_not_resent(self):
        _, state = check_notices([NOTICE], TEAMS, today=TODAY)
        alerts, _ = check_notices([NOTICE], TEAMS, state, today=TODAY)
        self.assertEqual(alerts, [])

    def test_revised_notice_triggers_new_alert(self):
        _, state = check_notices([NOTICE], TEAMS, today=TODAY)
        alerts, state = check_notices([{**NOTICE, "revision": 2}], TEAMS, state, today=TODAY)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(state["UK Sales:D-100"], "2")

    def test_irrelevant_region_does_not_alert(self):
        alerts, _ = check_notices([{**NOTICE, "region": "US"}], TEAMS, today=TODAY)
        self.assertFalse(alerts)

    def test_outside_six_month_horizon_does_not_alert(self):
        alerts, _ = check_notices([{**NOTICE, "release_in_days": 210}], TEAMS, today=TODAY)
        self.assertFalse(alerts)

    def test_past_release_does_not_alert(self):
        alerts, _ = check_notices([{**NOTICE, "release_in_days": -1}], TEAMS, today=TODAY)
        self.assertFalse(alerts)

if __name__ == "__main__":
    unittest.main()
