---
name: todoist-orbit
description: "Operate Todoist through a Python CLI backed by the Todoist REST API. Use when the task requires deterministic Todoist automation instead of chatty natural-language parsing: listing, creating, updating, moving, completing, deleting, or resolving tasks; creating/updating/archiving projects; creating/updating/archiving sections; uploading files and attaching them to task/project comments; or concurrent Todoist lookups. Prefer this skill when Todoist, projects, sections, attachments, or task comments are involved."
metadata: { "openclaw": { "requires": { "bins": ["python3"] }, "env": ["TODOIST_API_KEY"] } }
---

# Todoist Orbit

Use the bundled Python CLI. It is async at the command layer and uses only Python stdlib HTTP primitives, so there is no SDK dependency to install.

## Prerequisites

Set `TODOIST_API_KEY` in the environment.

## Primary command

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty <group> <action> ...
```

## Common commands

### Tasks

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty tasks list --filter "today"
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty tasks add "Ship release" --project-id <project_id> --section-id <section_id> --due "tomorrow" --priority 1
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty tasks update <task_id> --content "Ship release v2" --due "next monday"
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty tasks move <task_id> --project-id <project_id> --section-id <section_id>
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty tasks close <task_id>
```

### Projects

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty projects list
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty projects add "Client Ops" --view-style board --favorite
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty projects archive <project_id>
```

### Sections

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty sections list --project-id <project_id>
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty sections add <project_id> "Inbox"
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty sections move <section_id> <project_id>
```

`sections move` is preserved for CLI compatibility, but Todoist REST does not provide a section move endpoint, so the command exits with a documented error instead of attempting a move.

### Attachments and comments

Upload the file first or let `comments add` do it implicitly.

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty uploads add ./voice-note.m4a
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty comments add --task-id <task_id> "Voice memo attached" --attachment ./voice-note.m4a
```

Todoist stores attachments on comments, not directly on the task object. For task attachments, add a task comment with `--attachment`.

### Concurrent resolution

```bash
python3 skills/todoist-orbit/scripts/todoist_orbit.py --pretty resolve --project "Work" --section "Inbox" --task-filter "today"
```

Use `resolve` when you want project and section lookups plus a task query in one call.

## Operational notes

- Prefer IDs once resolved; names are ambiguous.
- The CLI is REST-only; there is no Sync API fallback.
- `sections move` is intentionally unsupported because Todoist REST does not expose a section move operation. The command remains available only to fail clearly for callers that already invoke it.
- `comments add --attachment` uploads the file and passes the returned attachment object into the comment create request.
- Read `references/api-notes.md` only when you need endpoint-specific details or attachment behavior.
