# Recovery Playbook: When Your Graph Goes Wrong

Use this when something breaks in production. Follow the steps in order.

## Phase 1: Stop the Bleeding (First 5 minutes)

1. **Assess severity:**
   - [ ] Is data being written incorrectly? (Stop writes immediately)
   - [ ] Are queries returning wrong results? (Route around the graph)
   - [ ] Is the graph totally unavailable? (Fail over to replica if you have one)

2. **Cut off new damage:**
   - [ ] Stop all writes if data corruption is happening
   - [ ] Redirect queries to read replica or cached results
   - [ ] Page on-call engineer and stakeholders

3. **Document what happened:**
   - [ ] What query/write failed?
   - [ ] When did it start?
   - [ ] How many rows/edges are affected?

## Phase 2: Diagnosis (5-30 minutes)

1. **Check the usual suspects:**
   - [ ] Disk full? (check storage layer)
   - [ ] Replica lag? (check replication lag metric)
   - [ ] Query timeout? (check query logs for long-running queries)
   - [ ] Network partition? (check connectivity between shards)

2. **Look at recent changes:**
   - [ ] Was there a deploy in the last 30 minutes?
   - [ ] Did someone run a migration?
   - [ ] Did write volume spike?
   - [ ] Did query patterns change?

3. **Inspect the data:**
   - [ ] Are there orphaned edges? (edge points to node that doesn't exist)
   - [ ] Are there duplicate nodes? (same entity with multiple IDs)
   - [ ] Is the graph connected? (are there islands?)

## Phase 3: Recovery (30 min - hours)

### If it's a query layer issue:
1. Roll back recent query code
2. Restart the query service
3. Verify queries work
4. Gradually send traffic back

### If it's a data consistency issue:
1. Identify the corruption boundary (which rows/edges are bad?)
2. Do you have a backup from before the corruption? (Restore it)
3. Do you have an immutable log? (Replay from the last good state)
4. If neither: Manual fix or accept data loss and move forward

### If it's a storage layer issue:
1. If it's disk full: Archive old data or add storage
2. If it's a replica: Resync from primary
3. If it's the primary: Fail over to replica (if you have one)
4. If you don't have a replica: This is a Very Bad Day

### If it's a sharding/coordination issue:
1. Identify which shard is problematic
2. Quarantine it (don't route new requests to it)
3. Fix the issue on that shard
4. Gradually reintegrate it

## Phase 4: Prevention (After recovery)

1. **Add monitoring for this scenario** — So you catch it faster next time
2. **Document what happened** — Update runbooks
3. **Test recovery** — Do a practice recovery drill quarterly
4. **Fix root cause** — Not just the symptom

---

## Common Scenarios and Fast Fixes

| Scenario | Fast Fix | Prevention |
|----------|----------|-----------|
| **Disk full** | Delete old snapshots or archive data | Set up automated cleanup or add storage monitoring |
| **Slow queries** | Restart query service, check for long queries | Profile queries regularly, adjust indexes |
| **Duplicate nodes** | Dedup using natural key, keep one | Add uniqueness constraint at write time |
| **Orphaned edges** | Delete edges pointing to missing nodes | Add referential integrity checks |
| **Replication lag** | Wait for lag to catch up or fail over | Monitor lag, alert if > threshold |
| **Network partition** | Manual intervention to reunite shards | Regular network health checks |

---

## When to Give Up and Revert

If recovery is taking > 30 minutes and you're not sure of the fix:
- Restore from backup (if you have one)
- Revert the recent deploy
- Accept the data loss, document it, move on

**It's okay to lose an hour of data to save 8 hours of manual recovery.**

