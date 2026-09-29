# MCP Platform Assistant

Python **Model Context Protocol (MCP)** server that exposes ticket/platform tools for AI assistants.

Works with [`platform-ticket-api`](https://github.com/sumanthgowda45/platform-ticket-api).

## Tools

- `list_tickets` — filter by status / assignee
- `get_ticket` — fetch by id
- `create_ticket` — create a ticket
- `bulk_update_tickets` — bulk status/assignee/note updates
- `summarize_open_work` — quick open/in-progress summary for an assignee

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the ticket API first, then:

```bash
export TICKET_API_BASE=http://localhost:8088/api/v1/tickets
python server.py
```

## Example MCP client config

```json
{
  "mcpServers": {
    "platform-assistant": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/mcp-platform-assistant",
      "env": {
        "TICKET_API_BASE": "http://localhost:8088/api/v1/tickets"
      }
    }
  }
}
```

## Author

Sumanth D Gowda — Senior Platform Developer (Java Backend) with MCP integration experience
