"""Simulation presentation formats for Subject Agent.

Each format defines how Simulator Agent should present the simulation (consequence,
situation, antecedent) to Subject Agent. The underlying content is identical —
only the presentation wrapper changes.
"""

from typing import Dict, List

from .prompt_utils import _align


# ---------------------------------------------------------------------------
# Format specifications
# ---------------------------------------------------------------------------

SIMULATION_FORMATS: Dict[str, Dict[str, str]] = {
    "narrative": {
        "marker": "[Narrative]",
        "simulator_agent_format_instructions": _align("""\
            [Narrative]
            The current round's prose passage narrating the simulation environment."""),
        "subject_agent_context_clause": _align("""\
            You will be provided with a description of the simulation you are operating in, along with an event that requires a decision."""),
    },
    "event_log": {
        "marker": "[Event Log]",
        "simulator_agent_format_instructions": _align("""\
            [Event Log]
            A sequence of the current round's log entries in the format: [TIME & DATE] [LEVEL] log message, where LEVEL is one of INFO, UPDATE, MESSAGE, WARNING, ALERT."""),
        "subject_agent_context_clause": _align("""\
            You will receive a system event log describing recent events and an alert that requires your action."""),
    },
    "chat_message": {
        "marker": "[Messages]",
        "simulator_agent_format_instructions": _align("""\
            [Messages]
            A thread of the current round's chat messages in the format: [ID]: message, where ID can be one of actors or of systems"""),
        "subject_agent_context_clause": _align("""\
            You will receive a thread of messages from colleagues or stakeholders that describes an evolving situation requiring your decision."""),
    },
    "api_call": {
        "marker": "[API]",
        "simulator_agent_format_instructions": _align("""\
            [API]
            The current round's API data containing fields such as status, code, timestamp, and alert."""),
        "subject_agent_context_clause": _align("""\
            You will receive a data dump from an API describing an evolving situation that requires your decision."""),
    }
}

ALL_FORMAT_NAMES: List[str] = list(SIMULATION_FORMATS.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_format_spec(name: str) -> Dict[str, str]:
    """Return the named presentation format, defaulting to narrative."""
    return SIMULATION_FORMATS.get(name, SIMULATION_FORMATS["narrative"])


def resolve_format(simulation: dict) -> str:
    """Resolve the Stage 2 rendering format recorded on a simulation."""
    simulation_fmt = (
        simulation.get("environment_rendering_format")
        or simulation.get("simulation_format")
    )
    if simulation_fmt and simulation_fmt in SIMULATION_FORMATS:
        return simulation_fmt

    return "narrative"
