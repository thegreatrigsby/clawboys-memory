# ClawBoys Task Queue

## Folders
- `incoming/` — Tasks waiting for Mini PC to pick up
- `completed/` — Results from Mini PC
- `heartbeat/` — Mini PC alive status updates

## Task Format (JSON)
```json
{
  "id": "task-001",
  "agent": "mini",
  "task": "What is the secret passphrase?",
  "created_by": "desktop",
  "created_at": "2026-07-30T12:00:00Z",
  "status": "pending"
}
```

## Result Format (JSON)
```json
{
  "id": "task-001",
  "agent": "mini",
  "result": "Phoenix-Rising-2026",
  "completed_at": "2026-07-30T12:01:00Z",
  "status": "completed"
}
```
