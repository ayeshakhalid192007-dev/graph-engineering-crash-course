# Incident Report: INC-4482

**Company:** Northwind Analytics (fictional, invented for this kit)
**Status:** Resolved
**Duration:** ~14 hours of delayed customer-facing output

## Summary

Daily digest emails to customers went out roughly fourteen hours late.
Customers who rely on the digest to catch overnight threshold breaches
noticed the delay before our own monitoring did.

## Timeline

- **02:14** — `ingest-api` begins accepting a larger-than-usual batch of
  customer CSV uploads ahead of a scheduled partner import.
- **02:40** — A code path added the previous week for CSV header
  validation opens a database connection per uploaded file but does not
  release it back to the pool when validation succeeds. Over the batch,
  the connection pool fills up.
- **03:05** — `ingest-api` starts queuing new upload requests instead of
  rejecting them, because the retry logic assumed pool exhaustion was
  always transient.
- **03:20** — `digest-scheduler`, which reads from the same database to
  assemble the nightly digest, cannot acquire a connection and silently
  falls back to a retry loop instead of alerting.
- **04:00–16:00** — `digest-scheduler` keeps retrying without success.
  `alert-dispatcher`, which is supposed to notify customers of threshold
  breaches independent of the digest, also depends on the same connection
  pool and goes quiet during this window.
- **16:10** — On-call engineer Priya Raman is paged after a customer
  emails support asking where their digest is. Priya finds the exhausted
  connection pool, restarts `ingest-api` to release the leaked
  connections, and the backlog drains within twenty minutes.
- **16:45** — Digest emails and queued alerts finish sending. Incident
  closed.

## Root cause

A leaked database connection in `ingest-api`'s CSV header validation
path. The validation function opened a connection for each uploaded file
to check header rows against an allow-list, but an early `return` on the
success path skipped the connection release. Under normal upload volume
the leak was slow enough not to matter; the partner import's larger batch
exhausted the pool in under an hour.

## Impact

- `digest-scheduler`: no digest emails sent for the affected window.
- `alert-dispatcher`: threshold-breach alerts queued but not delivered
  until the pool was freed.

## Follow-up

- Discussed in the `#northwind-incidents` Slack channel.
- Priya Raman is filing a follow-up ticket to add a connection-pool
  saturation alert so this doesn't require a customer report to surface
  next time.

---

*This is an invented scenario written for the `document-to-facts` starter
kit. Northwind Analytics, `INC-4482`, and all names above are fictional.*
