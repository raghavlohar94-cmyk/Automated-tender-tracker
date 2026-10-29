"""Synthetic, local framework tender alert demo. No external network requests."""
from datetime import date, timedelta
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def check_notices(notices, rules, state=None, today=None, horizon=183):
    today = today or date.today()
    new_state = dict(state or {})
    alerts = []
    for notice in notices:
        release = today + timedelta(days=notice["release_in_days"])
        if not 0 <= (release - today).days <= horizon:
            continue
        for team in rules:
            if notice["category"] not in team["categories"]:
                continue
            if notice["region"] not in team["regions"] and "ALL" not in team["regions"]:
                continue
            key = team["name"] + ":" + notice["id"]
            revision = str(notice["revision"])
            if new_state.get(key) == revision:
                continue
            alerts.append({"team":team["name"],"notice_id":notice["id"],
                           "title":notice["title"],"release":str(release),
                           "revision":revision})
            new_state[key] = revision
    return alerts, new_state

if __name__ == "__main__":
    notices = json.loads((ROOT / "sample_notices.json").read_text())
    rules = json.loads((ROOT / "team_rules.json").read_text())
    state_file = ROOT / ".demo_state.json"
    old = json.loads(state_file.read_text()) if state_file.exists() else {}
    alerts, state = check_notices(notices, rules, old)
    print(json.dumps(alerts, indent=2))
    state_file.write_text(json.dumps(state, indent=2))
