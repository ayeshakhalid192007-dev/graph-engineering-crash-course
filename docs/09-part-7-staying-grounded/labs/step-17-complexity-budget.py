#!/usr/bin/env python3
"""Step 17 live lab: complexity budgets, up front vs. evidence-driven.

No dependencies, no network, standard library only. Illustrative, not a
strict pass/fail assertion -- it prints a maintenance-cost comparison and
always exits 0. There is nothing to assert against, because both teams are
watching the identical loops over the identical twenty-six weeks; the only
difference is *when* each team pays for each governance edge.

Two toy teams run the same restock loop and substitution loop for twenty-six
weeks. In that window, exactly one of the four failure modes from Step 12
actually shows up: metric-gaming, observed at week 19. The other three
(blind spot, collision, drift) never occur for either team in this window --
restock and substitution never touch the same resource, and nothing about
the substitution rule's assumptions goes stale in six months.

  OVER-EAGER TEAM -- installs all four governance fixes at week 1, before
  any evidence any of them is needed:
    - counter-metric:      1 minute/week of monitoring, from week 1
    - audit loop:          45 minutes/week of triaging its reports
                            (all false positives in this window), from week 1
    - arbitration edge:    5 minutes/week of upkeep, from week 1
    - anchor + frozen node: 10 minutes/week of upkeep, from week 1, PLUS a
                            480-minute (8-hour) change-review process in
                            week 3 to unlock and correct a miscalibrated
                            threshold, because it was already frozen

  EVIDENCE-DRIVEN TEAM -- ships both loops bare, adds a fix only when its
  matching failure is actually observed:
    - week 3: the same threshold miscalibration is caught, but nothing is
      frozen yet, so it's a direct 10-minute code fix, not a change-review
      process
    - week 19: metric-gaming is observed, so the counter-metric goes in
      then -- 1 minute/week of monitoring, from week 19 onward only
    - blind spot, collision, drift: never observed in this window, so the
      audit loop and the arbitration edge are never added at all

The lab tallies total minutes spent by each team through week 26 and prints
both the weekly shape and the final numbers side by side.
"""

WEEKS = 26
GAMING_OBSERVED_WEEK = 19
THRESHOLD_MISCALIBRATION_WEEK = 3

COUNTER_METRIC_WEEKLY = 1
AUDIT_LOOP_WEEKLY = 45
ARBITRATION_EDGE_WEEKLY = 5
ANCHOR_FROZEN_WEEKLY = 10
FROZEN_UNLOCK_PROCESS_COST = 480  # minutes, one-time, over-eager team only
DIRECT_THRESHOLD_FIX_COST = 10    # minutes, one-time, evidence-driven team only


def over_eager_weekly_cost(week):
    """All four edges installed since week 1; every one accrues its
    ongoing cost every week regardless of whether it has caught anything."""
    cost = (
        COUNTER_METRIC_WEEKLY
        + AUDIT_LOOP_WEEKLY
        + ARBITRATION_EDGE_WEEKLY
        + ANCHOR_FROZEN_WEEKLY
    )
    if week == THRESHOLD_MISCALIBRATION_WEEK:
        cost += FROZEN_UNLOCK_PROCESS_COST
    return cost


def evidence_driven_weekly_cost(week):
    """No edge exists until its matching failure is actually observed."""
    cost = 0
    if week == THRESHOLD_MISCALIBRATION_WEEK:
        cost += DIRECT_THRESHOLD_FIX_COST
    if week >= GAMING_OBSERVED_WEEK:
        cost += COUNTER_METRIC_WEEKLY
    return cost


def main():
    print("Step 17 lab -- complexity budget, day-one governance vs. evidence-driven\n")
    print("  week  over-eager (min)  evidence-driven (min)  note")

    over_eager_total = 0
    evidence_driven_total = 0

    for week in range(1, WEEKS + 1):
        oe_cost = over_eager_weekly_cost(week)
        ed_cost = evidence_driven_weekly_cost(week)
        over_eager_total += oe_cost
        evidence_driven_total += ed_cost

        note = ""
        if week == THRESHOLD_MISCALIBRATION_WEEK:
            note = "threshold miscalibration caught this week"
        elif week == GAMING_OBSERVED_WEEK:
            note = "metric-gaming observed this week"

        print(f"  {week:>4}  {oe_cost:>16}  {ed_cost:>22}  {note}")

    print()
    print("Totals through week 26:")
    print(f"  over-eager team:     {over_eager_total} minutes")
    print(f"  evidence-driven team: {evidence_driven_total} minutes")
    print()

    difference = over_eager_total - evidence_driven_total
    if difference > 0:
        print(
            f"The over-eager team paid {difference} more minutes across the same "
            "twenty-six weeks, on the same two loops, for governance edges that "
            "caught real problems no more often than the evidence-driven team's "
            "did -- they simply paid for three of the four edges the whole time, "
            "whether or not those three ever had a job to do."
        )
    else:
        print(
            "In this run the two teams' totals did not diverge the way the step "
            "page describes -- adjust the weekly costs above to model your own "
            "situation."
        )

    print(
        "\nThis comparison is illustrative, not a correctness check: there is no "
        "single right maintenance-cost number, only the shape of who pays for "
        "unproven governance and when."
    )


if __name__ == "__main__":
    main()
