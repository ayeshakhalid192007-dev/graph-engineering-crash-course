#!/usr/bin/env python3
"""Step 12 live lab: metric-gaming, and the counter-metric that catches it.

No dependencies, no network, standard library only. A toy version of the
step-12 triage queue. Ten bug reports arrive each working day. Seven of
them genuinely need an owner picked; three genuinely do need more
information from the reporter. The loop has a fixed budget of effort
units per day.

  * routing a report properly costs 3 effort units
  * stamping it `needs-more-info` costs 1

The headline number the team put on the dashboard is "reports cleared
per day", and stamping counts as clearing. So a loop maximizing that
number alone will stamp everything: ten clearances a day for ten units
of effort, versus three clearances if it does the work honestly.

The lab runs the queue twice over five days.

  RUN A -- scored on the headline number alone.
  RUN B -- same loop, same budget, but a counter-metric is watching:
           the share of cleared reports a human reopens within a week.
           It is computed by the reporting pipeline, not by the loop,
           and the loop never receives it as an input. A run whose
           reopen rate exceeds the ceiling is rejected.

Both runs' outcomes are printed side by side. The interesting contrast
is that Run A wins the dashboard by a wide margin and settles fewer
reports in reality, and that only the counter-metric can tell.

Exits 1 if the counter-metric fails to reject the gamed run, if it
wrongly rejects the honest run, or if the gamed run does not in fact
look better on the headline number (which would mean the lab is no
longer demonstrating anything). Exits 0 otherwise.
"""

import sys

DAYS = 5
DAILY_EFFORT = 10
ROUTE_COST = 3
STAMP_COST = 1

# Per day: seven reports where `needs-more-info` is the wrong answer and
# will be reopened, three where it is the right answer and will not be.
NEEDS_OWNER_PER_DAY = 7
GENUINELY_INCOMPLETE_PER_DAY = 3

REOPEN_CEILING = 0.25


def run_day(honest):
    """One day of triage. Returns (cleared, reopened, settled).

    `settled` is the number of reports that actually went away: cleared
    minus the ones a human had to reopen. Nothing in the loop computes
    this -- it is here so the lab can print what the dashboard cannot.
    """
    budget = DAILY_EFFORT
    cleared = 0
    reopened = 0

    if honest:
        # Route the reports that need an owner, as far as the budget
        # reaches; stamp only the ones where stamping is the truthful
        # answer, with whatever is left.
        owners_left = NEEDS_OWNER_PER_DAY
        while owners_left > 0 and budget >= ROUTE_COST:
            budget -= ROUTE_COST
            owners_left -= 1
            cleared += 1
        incomplete_left = GENUINELY_INCOMPLETE_PER_DAY
        while incomplete_left > 0 and budget >= STAMP_COST:
            budget -= STAMP_COST
            incomplete_left -= 1
            cleared += 1
    else:
        # Maximize the dashboard: stamping is the cheapest clearance, so
        # stamp everything. The seven that needed an owner come back.
        arriving = NEEDS_OWNER_PER_DAY + GENUINELY_INCOMPLETE_PER_DAY
        stamped = 0
        while stamped < arriving and budget >= STAMP_COST:
            budget -= STAMP_COST
            stamped += 1
            cleared += 1
        reopened = min(stamped, NEEDS_OWNER_PER_DAY)

    return cleared, reopened, cleared - reopened


def run_queue(label, honest):
    totals = {"cleared": 0, "reopened": 0, "settled": 0}
    print(f"\n{label}")
    print("  day  cleared  reopened  settled")
    for day in range(1, DAYS + 1):
        cleared, reopened, settled = run_day(honest)
        totals["cleared"] += cleared
        totals["reopened"] += reopened
        totals["settled"] += settled
        print(f"  {day:>3}  {cleared:>7}  {reopened:>8}  {settled:>7}")

    per_day = totals["cleared"] / DAYS
    rate = totals["reopened"] / totals["cleared"] if totals["cleared"] else 0.0
    print(f"  headline metric (cleared per day): {per_day:.1f}")
    print(f"  counter-metric (reopened share):   {rate:.2f}")
    print(f"  reports actually settled in {DAYS} days: {totals['settled']}")
    return per_day, rate, totals["settled"]


def counter_metric_verdict(rate):
    """Owned by the reporting pipeline, never handed to the loop."""
    return "ACCEPTED" if rate <= REOPEN_CEILING else "REJECTED"


def main():
    print("triage queue: 10 reports a day, 10 effort units a day")
    print(f"routing costs {ROUTE_COST}, stamping needs-more-info costs {STAMP_COST}")
    print(f"counter-metric ceiling: reopened share must stay at or below {REOPEN_CEILING}")

    a_per_day, a_rate, a_settled = run_queue(
        "RUN A -- scored on cleared-per-day alone", honest=False
    )
    a_verdict = counter_metric_verdict(a_rate)
    print(f"  counter-metric verdict: {a_verdict}")

    b_per_day, b_rate, b_settled = run_queue(
        "RUN B -- same loop, counter-metric watching from outside", honest=True
    )
    b_verdict = counter_metric_verdict(b_rate)
    print(f"  counter-metric verdict: {b_verdict}")

    print(
        f"\ncontrast: Run A posts {a_per_day:.1f} clearances a day against Run B's "
        f"{b_per_day:.1f}, and settles {a_settled} reports against Run B's {b_settled}."
    )

    try:
        assert a_per_day > b_per_day, (
            "the gamed run no longer beats the honest one on the headline "
            "number, so this lab is not demonstrating metric-gaming at all"
        )
        assert a_verdict == "REJECTED", (
            f"the counter-metric accepted the gamed run at a reopened share of "
            f"{a_rate:.2f} -- a counter-metric that does not move when the "
            "primary number is being gamed is not a check on anything"
        )
        assert b_verdict == "ACCEPTED", (
            f"the counter-metric rejected the honest run at a reopened share of "
            f"{b_rate:.2f}, which would make it useless as a gate"
        )
        assert a_settled < b_settled, (
            "the gamed run settled at least as many reports as the honest one, "
            "so the headline number was not actually misleading here"
        )
    except AssertionError as exc:
        print(f"\nFAIL: {exc}")
        sys.exit(1)

    print(
        "\nPASS: the run that looked best on the dashboard was rejected by a "
        "counter-metric the loop could neither see nor influence, and the run "
        "that survived the gate is the one that actually cleared the queue."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
