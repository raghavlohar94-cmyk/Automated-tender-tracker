# Automated Framework & Tender Tracker

Independent, portfolio-safe Python demonstration using **synthetic notices** and rules. It tracks upcoming framework opportunities over a six-month horizon, routes relevant notices by team and avoids duplicate alerts.

**Run:** `python tracker.py` (Python 3.10+, standard library only). Output is local JSON. No real procurement feeds or messaging services are connected.

This is not employer-owned code, and it does not use confidential procurement information.

## Technical scope
- 183-day lookahead window
- Category and region routing
- New/revised notice detection
- Revision-based alert deduplication

## Next steps
Production source adapters, scheduling, monitoring, role-aware alerts and Teams/email integrations. These are not implemented in the demo.