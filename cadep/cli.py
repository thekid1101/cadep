"""CADEP CLI — submit, resolve, defer, status (PRD Section 10)."""

from __future__ import annotations

import asyncio
import json
import sys
import time

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cadep import __version__
from cadep.audit_logger import AuditLogger
from cadep.friction_generator import FrictionGenerator
from cadep.models import (
    Decision,
    FrictionAnswer,
    PanelMode,
    ResolveRecord,
    VerificationBasis,
)
from cadep.orchestrator import Orchestrator
from cadep.output_formatter import format_status
from cadep.prompts import (
    BACKLOG_PAUSE,
    FRICTION_TOO_BRIEF,
    UNDERSPECIFIED_RESPONSE,
)
from cadep.token_logger import TokenLogger

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """CADEP — Cross-Domain Adversarial Expert Panel."""
    pass


@cli.command()
@click.argument("proposal", required=False)
@click.option("--mode", type=click.Choice(["fast", "full"]), default="fast",
              help="Panel mode: fast (inline) or full (async audit)")
@click.option("--proposal-file", "--file", "-f", type=click.Path(exists=True),
              help="Path to YAML proposal file")
def submit(proposal: str | None, mode: str, proposal_file: str | None):
    """Submit a proposal for adversarial review."""
    if not proposal and not proposal_file:
        console.print("[red]Provide a proposal as argument or --file path.[/red]")
        raise SystemExit(1)

    raw_input = proposal or ""
    panel_mode = PanelMode.FULL if mode == "full" else PanelMode.FAST

    orch = Orchestrator()

    # Progress display
    steps = [
        ("Normalizing input", "1/6"),
        ("Classifying domain", "2/6"),
        ("Retrieving documents", "3/6"),
        ("Panel (parallel)", "4/6"),
        ("Synthesizing", "5/6"),
    ]
    if panel_mode == PanelMode.FULL:
        steps.append(("Friction question", "6/6"))

    with console.status("[bold green]Running CADEP panel...") as status:
        result = asyncio.run(
            orch.submit(raw_input, mode=panel_mode, proposal_file=proposal_file)
        )

    if not result["success"]:
        error = result.get("error", "")
        if error == "underspecified":
            clarification = result.get("clarification", "")
            console.print(UNDERSPECIFIED_RESPONSE.format(
                clarification=clarification or "What problem are you trying to solve, and what approach are you considering?"
            ))
        elif error == "ambiguous":
            console.print(f"\n[yellow]One clarification needed:[/yellow]")
            console.print(f"  {result.get('clarification', '')}")
            console.print(f"\nProvide the answer and resubmit, or resubmit as-is and defaults will be used.")
        else:
            console.print(f"\n[red]{error}[/red]")
        return

    # Display results
    if result["mode"] == "fast":
        console.print()
        console.print(result["display"])
        console.print()

    elif result["mode"] == "full":
        path = result["output_path"]
        console.print()
        console.print(f"[bold green]Full audit saved to:[/bold green] {path}")
        console.print()
        console.print("Review asynchronously. When ready:")
        console.print(f"    [bold]cadep resolve {result['query_id']}[/bold]")
        console.print()

    # Stats footer
    console.print(
        f"[dim]Total: {result['runtime_seconds']:.1f}s | "
        f"Tokens: {result['tokens']:,} | "
        f"Est. cost: ${result['cost']:.4f}[/dim]"
    )


@cli.command()
@click.argument("query_id")
def resolve(query_id: str):
    """Resolve a full-audit panel output."""
    audit_logger = AuditLogger()

    # Load panel output
    markdown = audit_logger.load_panel_output(query_id)
    if not markdown:
        console.print(f"[red]No panel output found for {query_id}[/red]")
        console.print("Check available audits with: cadep status")
        return

    # Display the full audit
    console.print()
    console.print(markdown)
    console.print()

    # Load friction question if exists
    # Search execution records for the friction question
    submissions = audit_logger.get_submissions()
    sub = next((s for s in submissions if s["query_id"] == query_id), None)
    if not sub:
        console.print(f"[red]No submission record for {query_id}[/red]")
        return

    # Generate friction question if not cached
    console.print("=" * 50)
    console.print("[bold]VERIFICATION QUESTION[/bold]")
    console.print("=" * 50)
    console.print()

    # Load the context-specific friction question generated during submit
    friction_q = audit_logger.load_friction_question(query_id)
    if friction_q:
        console.print(friction_q)
    else:
        # Fallback if friction question wasn't persisted
        console.print(
            "Describe the specific verification you will perform before "
            "acting on this panel output, and what finding would change your decision."
        )
    console.print()

    # Collect friction answer
    start_time = time.time()
    while True:
        answer = click.prompt("Your response", type=str)
        if FrictionGenerator.validate_answer(answer):
            break
        console.print(f"[yellow]{FRICTION_TOO_BRIEF}[/yellow]")

    # Log friction answer
    from datetime import datetime, timezone
    audit_logger.log_friction_answer(FrictionAnswer(
        query_id=query_id,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        question="verification",
        answer=answer,
        answer_word_count=len(answer.split()),
    ))

    # Collect decision
    console.print()
    decision_str = click.prompt(
        "Decision",
        type=click.Choice(["accept", "override", "reject"], case_sensitive=False),
    )
    decision = Decision(decision_str.lower())

    reasoning = None
    override_category = None
    verification_basis = None

    if decision in (Decision.OVERRIDE, Decision.REJECT):
        reasoning = click.prompt("Reasoning (required)")
        if decision == Decision.OVERRIDE:
            override_category = click.prompt(
                "Override category",
                type=click.Choice([
                    "implementation-constraint",
                    "domain-knowledge",
                    "data-specific",
                    "cost-benefit",
                    "other",
                ]),
            )
    else:
        # Accept — collect verification basis
        vb_str = click.prompt(
            "Verification basis",
            type=click.Choice([
                "checked_cited_source",
                "checked_implementation_constraint",
                "found_contradictory_evidence",
                "validated_applicability_condition",
                "not_verified",
            ]),
        )
        verification_basis = VerificationBasis(vb_str)

    review_time = int(time.time() - start_time)

    # Log resolve
    audit_logger.log_resolve(ResolveRecord(
        query_id=query_id,
        decision=decision,
        override_category=override_category,
        reasoning=reasoning,
        review_time_seconds=review_time,
        friction_response_saved=True,
        verification_basis=verification_basis,
    ))

    console.print()
    console.print(f"[green]Logged. Panel output retained.[/green]")


@cli.command()
@click.argument("query_id")
@click.option("--reason", "-r", required=True, help="Reason for deferral")
def defer(query_id: str, reason: str):
    """Defer a pending full-audit resolution."""
    audit_logger = AuditLogger()
    audit_logger.log_defer(query_id, reason)
    console.print(f"[green]Deferred {query_id}: {reason}[/green]")


@cli.command()
def status():
    """Show CADEP status — unresolved audits, staleness, usage."""
    audit_logger = AuditLogger()
    token_logger = TokenLogger()

    unresolved = audit_logger.get_unresolved_audits()
    staleness = audit_logger.get_staleness_warnings()
    totals = token_logger.get_totals()

    output = format_status(unresolved, staleness, totals)
    console.print(output)

    # Backlog warning
    if len(unresolved) >= 3:
        from cadep import config
        console.print()
        console.print(f"[yellow]{BACKLOG_PAUSE.format(max=config.MAX_UNRESOLVED_AUDITS)}[/yellow]")


if __name__ == "__main__":
    cli()
