from typing import List

users_database = [
    {"id": 101, "name": "Alice", "role": "admin", "is_active": True},
    {"id": 102, "name": "Bob", "role": "user", "is_active": False},
    {"id": 103, "name": "Charlie", "role": "editor", "is_active": True},
]


def get_active_user_names(users: List[dict]) -> List[str]:
    return [user["name"] for user in users if user["is_active"]]


def build_context_block(active_names: List[str]) -> str:
    return "".join(f"{index}. {name}\n" for index, name in enumerate(active_names, start=1))


def generate_system_prompt(active_names: List[str]) -> str:
    context_block = build_context_block(active_names)
    return f"""
System Instruction: You are a corporate communication assistant.

Task: Write a highly professional welcome message for the following active team members.

Active Members:

{context_block}
Please keep the tone encouraging and brief.
"""


def execute_mock_llm_call(prompt_text: str, model_engine: str = "gpt-4", **kwargs) -> str:
    print(f"Routing request to target model: {model_engine}")
    print(f"Applying dynamic configuration parameters: {kwargs}")
    print("Awaiting API response...\n")
    active_users = get_active_user_names(users_database)
    return f"Mock API Output: Welcome aboard, {', '.join(active_users)}! Let's get to work."


if __name__ == "__main__":
    active_users = get_active_user_names(users_database)
    print(f"System Log: Found {len(active_users)} active users.\n")
    print("--- GENERATED PAYLOAD ---")
    print(generate_system_prompt(active_users))
    print("-------------------------\n")
    api_response = execute_mock_llm_call(
        prompt_text=generate_system_prompt(active_users),
        model_engine="gpt-4-turbo",
        temperature=0.4,
        max_tokens=250,
        top_k=50,
    )
    print(f"Final Result:\n{api_response}")