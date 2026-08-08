from pathlib import Path

from src.agent_core import create_default_profile, create_profile, mock_api_call


print("--- INITIALIZING AGENT ---")
profile = create_default_profile()
print(f"Agent '{profile.agent_name}' initialized on {profile.model_engine}.")
print(profile.to_json())

custom_profile = create_profile("AgentX", "gpt-4o", 0.3)
print(f"Custom profile created: {custom_profile.agent_name} on {custom_profile.model_engine}.")

config_path = Path("agent_config.json")
print("\n--- SAVING CONFIGURATION ---")
saved_path = profile.save_to_json(config_path)
print(f"Configuration securely saved to {saved_path}.")

print("\n--- RESILIENCE TESTS ---")
mock_api_call(payload={"data": "test"}, simulate_missing_key=True)
mock_api_call(payload={"data": "test"}, simulate_timeout=True)

