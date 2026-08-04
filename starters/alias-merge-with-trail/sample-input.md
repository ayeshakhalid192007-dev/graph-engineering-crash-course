# Two Mentions of the Same Backend System

**Company:** Meridian Freight (fictional, invented for this kit)

Meridian Freight runs a small internal platform. Two teams write about it in
two very different registers, and neither team is wrong about what they
saw.

## Source A — Support Ticket #5821 (customer success queue)

> **Subject:** Checkout charges stuck in "processing"
>
> A shipper on the Pro plan reports that checkout has been stuck on
> "processing" since **14:03 UTC on 2026-03-03**. She says the payments
> service has done this before during a deploy window and it usually
> clears on its own, but wants it logged in case it doesn't this time.
> Support has no visibility into which backend system actually handles
> checkout — only that customers call it "the payments service" because
> that's the label on the billing page in the customer portal.
>
> Update, 14:24 UTC: shipper confirms checkout is processing normally
> again. No credits requested. Ticket closed.

## Source B — Infrastructure Change Log (platform team, internal)

```
2026-03-03T13:58:00Z  deploy  billing-svc  v2.4.1 -> v2.4.2
2026-03-03T14:01:00Z  alert   billing-svc  connection pool saturated, rolling back
2026-03-03T14:02:00Z  deploy  billing-svc  v2.4.2 -> v2.4.1  (rollback; ref: support #5821)
2026-03-03T14:22:00Z  deploy  billing-svc  v2.4.1 confirmed healthy
2026-03-03T15:40:00Z  deploy  notify-svc   v1.9.0 -> v1.9.1
```

The platform team never writes "the payments service" anywhere — every
entry in this log names the deployment target by its exact identifier,
`billing-svc`.

## Decoy mention — not a match

Source A's shipper also mentioned, in a follow-up line not quoted above,
that "the notifications thing seemed fine the whole time." Source B's log
has a deploy entry for `notify-svc` an hour and a half later, with no
alert, no rollback, and no reference to ticket #5821. This kit's schema
lists `notify-svc` only so the merge step has a second, unrelated pair of
mentions to consider — the point of including it is to see the skill leave
it unmerged rather than fold it into the same canonical entity just
because it showed up in the same two documents.

---

*This is an invented scenario written for the `alias-merge-with-trail`
starter kit. Meridian Freight, `billing-svc`, `notify-svc`, and all
identifiers above are fictional.*
