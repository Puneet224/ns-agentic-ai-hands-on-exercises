from typing import List, Dict

class TeamMember:
    def __init__(self, name: str, role: str, is_active: bool = True) -> None:
        self.name = name
        self.role = role
        self.is_active = is_active

    def welcome_message(self) -> str:
        return f"Welcome {self.name}, our valued {self.role}."


def build_welcome_context(members: List["TeamMember"]) -> str:
    active_names = [member.name for member in members if member.is_active]
    return "\n".join(f"{index}. {name}" for index, name in enumerate(active_names, start=1))
