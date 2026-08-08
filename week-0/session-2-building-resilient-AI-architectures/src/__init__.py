"""session-2-building-resilient-AI-architectures src package.

Use this package in notebooks to import shared helpers and classes.
"""

from .agent_core import AgentProfile, create_default_profile
from .team import TeamMember, build_welcome_context

__all__ = ["TeamMember", "build_welcome_context", "AgentProfile", "create_default_profile"]
