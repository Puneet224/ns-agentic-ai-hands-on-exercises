# app.py

# 1. THE DATA BASELINE (Dictionaries & Lists)

# Simulating a database pull of user records. Dictionaries provide O(1) lookups.

users_database = [
    {"id": 101, "name": "Alice", "role": "admin", "is_active": True},
    {"id": 102, "name": "Bob", "role": "user", "is_active": False},
    {"id": 103, "name": "Charlie", "role": "editor", "is_active": True}
]

# 2. PYTHONIC ITERATION (List Comprehensions)

# Cleanly extract only the names of active users in a single line.

active_users = [user["name"] for user in users_database if user["is_active"]]

print(f"System Log: Found {len(active_users)} active users.\n")

# 3. STRING MANIPULATION (enumerate & f-strings)

# Dynamically build the context payload for the LLM.

context_block = ""

for index, name in enumerate(active_users, start=1):
    context_block += f"{index}. {name}\n"

# Utilizing multi-line triple quotes for clean prompt architecture

system_prompt = f"""

System Instruction: You are a corporate communication assistant.

Task: Write a highly professional welcome message for the following active team members.

Active Members:

{context_block}

Please keep the tone encouraging and brief.

"""

print("--- GENERATED PAYLOAD ---")
print(system_prompt)
print("-------------------------\n")

# 4. DYNAMIC FUNCTION SIGNATURES (**kwargs)

# We use **kwargs to catch any unexpected API parameters (like temperature, top_p)
# without needing to rewrite this function for different AI providers.

def execute_mock_llm_call(prompt_text, model_engine="gpt-4", **kwargs):
    print(f"Routing request to target model: {model_engine}")
    print(f"Applying dynamic configuration parameters: {kwargs}")
    print("Awaiting API response...\n")
    return f"Mock API Output: Welcome aboard, {', '.join(active_users)}! Let's get to work."


# 5. EXECUTION

# We can now pass any provider-specific parameters on the fly.

if __name__ == "__main__":
    api_response = execute_mock_llm_call(
        prompt_text=system_prompt,
        model_engine="gpt-4-turbo",
        temperature=0.4,
        max_tokens=250,
        top_k=50,
    )

    print(f"Final Result:\n{api_response}")
