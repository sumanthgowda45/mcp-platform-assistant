"""
MCP Platform Assistant

Model Context Protocol (MCP) server that exposes ticket/platform helper tools.
Designed to integrate with local platform APIs (e.g. platform-ticket-api).
"""

from __future__ import annotations

import json
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

TICKET_API_BASE = os.getenv("TICKET_API_BASE", "http://localhost:8088/api/v1/tickets")

mcp = FastMCP("platform-assistant")


def _client() -> httpx.Client:
    return httpx.Client(timeout=15.0)


@mcp.tool()
def list_tickets(status: str | None = None, assignee: str | None = None) -> str:
    """List tickets from the platform API with optional status/assignee filters."""
    params: dict[str, str] = {}
    if status:
        params["status"] = status
    if assignee:
        params["assignee"] = assignee

    with _client() as client:
        response = client.get(TICKET_API_BASE, params=params)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
def get_ticket(ticket_id: int) -> str:
    """Fetch a single ticket by id."""
    with _client() as client:
        response = client.get(f"{TICKET_API_BASE}/{ticket_id}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
def create_ticket(subject: str, description: str, assignee: str, priority: str = "MEDIUM") -> str:
    """Create a new platform ticket."""
    payload = {
        "subject": subject,
        "description": description,
        "assignee": assignee,
        "priority": priority,
    }
    with _client() as client:
        response = client.post(TICKET_API_BASE, json=payload)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
def bulk_update_tickets(
    ticket_ids: list[int],
    status: str | None = None,
    assignee: str | None = None,
    note: str | None = None,
) -> str:
    """Apply a bulk action (status/assignee/note) to multiple tickets."""
    payload: dict[str, Any] = {"ticketIds": ticket_ids}
    if status:
        payload["status"] = status
    if assignee:
        payload["assignee"] = assignee
    if note:
        payload["note"] = note

    with _client() as client:
        response = client.post(f"{TICKET_API_BASE}/bulk-actions", json=payload)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
def summarize_open_work(assignee: str = "sumanth") -> str:
    """Summarize open/in-progress tickets for an assignee."""
    with _client() as client:
        open_tickets = client.get(TICKET_API_BASE, params={"assignee": assignee, "status": "OPEN"}).json()
        in_progress = client.get(TICKET_API_BASE, params={"assignee": assignee, "status": "IN_PROGRESS"}).json()

    summary = {
        "assignee": assignee,
        "openCount": len(open_tickets),
        "inProgressCount": len(in_progress),
        "openSubjects": [t.get("subject") for t in open_tickets],
        "inProgressSubjects": [t.get("subject") for t in in_progress],
    }
    return json.dumps(summary, indent=2)


if __name__ == "__main__":
    mcp.run()
