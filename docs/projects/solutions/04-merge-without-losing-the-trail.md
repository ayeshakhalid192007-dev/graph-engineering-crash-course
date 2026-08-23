# Solution · Project 4: Merge Without Losing the Trail

This works through [Project 4](../04-merge-without-losing-the-trail.md)'s five ticket mentions of a Ferreira customer.

## Reading the evidence

| Mention | Raw name | Ticket | Shared evidence with another mention |
| --- | --- | --- | --- |
| m1 | Jonathan Ferreira | #401 | email matches m2, m4; order matches m5 |
| m2 | Jon Ferreira | #405 | email matches m1, m4 |
| m3 | J. Ferreira | #412 | none — different email domain, different order |
| m4 | Jonny F | #418 | email matches m1, m2 |
| m5 | Ferreira, J | #420 | order matches m1 |

m1, m2, and m4 all share the exact same email address, `jonathan.ferreira88@gmail.com`, across three different tickets — that's concrete, checkable evidence, not a guess based on how the names look. m5 has no email on file, but its order number, `#10432`, is the same order referenced in m1, tying it to the same purchase. All four have a stated reason to merge.

m3 looks like it belongs — same surname, same initial, superficially the closest-looking name in the set to the canonical form. But its email domain (`ferreiradesigns.com`, not `gmail.com`) and order number (`#10890`, matching nothing else in the set) share nothing with the other four mentions. Nothing here says m3 is definitely a different person — it's entirely possible this is the same Jonathan Ferreira emailing from a work address about an unrelated order — but nothing says it's the same person either, and a merge needs a reason, not a plausible story.

## The resolved graph

```json
{
  "mentions": [
    { "id": "m1", "raw_name": "Jonathan Ferreira", "source_ticket": "401", "email": "jonathan.ferreira88@gmail.com", "order": "10432" },
    { "id": "m2", "raw_name": "Jon Ferreira", "source_ticket": "405", "email": "jonathan.ferreira88@gmail.com", "order": "10432" },
    { "id": "m3", "raw_name": "J. Ferreira", "source_ticket": "412", "email": "j.ferreira@ferreiradesigns.com", "order": "10890" },
    { "id": "m4", "raw_name": "Jonny F", "source_ticket": "418", "email": "jonathan.ferreira88@gmail.com", "order": "11002" },
    { "id": "m5", "raw_name": "Ferreira, J", "source_ticket": "420", "phone_last4": "4471", "order": "10432" }
  ],
  "canonical_customers": [
    {
      "id": "cust-1",
      "mentioned_as": ["m1", "m2", "m4", "m5"],
      "merge_reason": "m1, m2, and m4 share the email jonathan.ferreira88@gmail.com across tickets #401, #405, and #418. m5 has no email on file but shares order #10432 with m1, tying it to the same purchase."
    },
    {
      "id": "cust-2",
      "mentioned_as": ["m3"],
      "merge_reason": null,
      "note": "Not merged into cust-1: different email domain (ferreiradesigns.com vs. gmail.com) and a different order number (#10890) from every mention in cust-1. Same surname and initial as cust-1, but that alone is not a stated reason. Merge if a future ticket ties this email or order to cust-1's evidence."
    }
  ]
}
```text

## Why this is reversible

Every one of the five original mention nodes is still sitting in `mentions`, untouched, with its own raw name and its own ticket. `cust-1` doesn't replace m1, m2, m4, and m5 — it points at them. If evidence later surfaces that m4's order was actually placed by a different family member using the same shared email, splitting `cust-1` back apart means reading `merge_reason`, re-checking which mentions relied on the email versus the order match, and moving m4 back out — not reconstructing four tickets' worth of context from scratch.

## Checking your own attempt

- Are all five mentions still present as their own nodes, with nothing deleted or overwritten?
- Does `cust-1`'s merge reason name the specific field and specific tickets that matched, rather than "names looked the same"?
- Is m3 left unmerged, with a written reason rather than a guess dressed up as a decision?
- Could you hand your JSON to someone else and have them correctly undo the `cust-1` merge using only what's written in `merge_reason`?
