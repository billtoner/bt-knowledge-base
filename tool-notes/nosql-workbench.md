# NoSQL Workbench for DynamoDB

Free AWS-provided GUI for designing and querying DynamoDB tables. Standalone Mac app. Far
better than the AWS web console for everything except managing the actual tables in your account.

**Tags:** aws · database · gui

## Cool features

### Visualizer / Data Modeler

- **Design tables and GSIs visually.** Drag-and-drop partition/sort keys, GSIs, LSIs. Validate
  before creating the table in AWS.
- **Access pattern modeling.** Describe your access patterns ("get sessions for a participant",
  "list events for a session in time order"), the tool tells you which GSIs you need and where
  hot partitions would form.
- **Sample data generation.** Auto-generate fake records that match your schema for testing.
- **Aggregate views.** See your model from the perspective of one access pattern at a time —
  useful when you have many GSIs and want to verify each one solves what it should.

### Operation Builder

- **Query builder UI.** Pick a table, pick an index, click to build the `KeyConditionExpression`
  and `FilterExpression`. See the resulting code in Python/JS/Java/etc.
- **Run queries against a real AWS account.** Connect with profile credentials, execute, see results.
- **Pagination handled visually.** Click "next" instead of remembering LastEvaluatedKey paste.
- **Generate code.** Copy the boto3 / Java / JS code that would do the same query. Useful for
  porting an ad-hoc exploration into actual application code.

### Visualizer

- **Visualize partition distribution.** See whether your access pattern would cause hot partitions
  *before* you push it to production.

## Useful in FPOC

Your FPOC DynamoDB tables (`audiopulse-sessions`, `audiopulse-events`, `insole_pressure_buffer`)
and their GSIs (e.g., `session_id-timestamp-index`) are where NoSQL Workbench earns its keep:

- "What if I added a new access pattern — say, list all sessions by participant?" — model it
  visually before creating the GSI.
- "Why is this query slow?" — visualize partition distribution.
- "I need to migrate the events schema" — sketch the new shape, generate sample data, verify
  access patterns still work, then plan the migration.

For day-to-day debugging (querying existing data), `aws-cli` with JMESPath filters is faster:

```bash
aws dynamodb query \
  --table-name audiopulse-events \
  --index-name session_id-timestamp-index \
  --key-condition-expression "session_id = :s" \
  --expression-attribute-values '{":s":{"S":"p001_walk_20260516_1400"}}' \
  --query 'Items[].{ts:timestamp.N,type:event_type.S}' \
  --output table
```

Or `bin/dynamodb-report.py` which already wraps queries for the common gait-report use case.

## When to reach for NoSQL Workbench specifically

- **Designing a new table or GSI** — verify schema before committing
- **Documenting access patterns** — generate diagrams for design docs
- **Debugging a specific item** — point-and-click is faster than aws-cli syntax
- **Onboarding** — visual schema beats reading boto3 source

## When NOT to use it

- Quick CLI queries — aws-cli wins
- Scripting / automation — boto3 in Python
- Production data manipulation — use bin/ scripts that wrap boto3 with safeguards

## Install

NOT in Homebrew. Direct download from AWS:

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html

Look for "Download NoSQL Workbench" → macOS section. Standalone app, no AWS account needed
to launch (just to connect to actual tables).

## Setup once

1. Download + drag to /Applications
2. Open → Operation Builder → Add connection
3. Use an existing AWS profile (`audiopulse`) or paste keys directly
4. Pick region (us-west-2 per FPOC config)
5. Browse tables

## Workflow sketch

For "I need to debug a session that didn't sync to DynamoDB":

1. Open Operation Builder → pick `audiopulse-events` table
2. Switch to `session_id-timestamp-index` GSI
3. KeyConditionExpression: `session_id = "p001_walk_20260516_1400"`
4. Execute
5. Sort the results by timestamp visually, look for gaps
6. Copy the boto3 code to use in `bin/sync-to-dynamodb.py` for one-off targeted re-syncs
