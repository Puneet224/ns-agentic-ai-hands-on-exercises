from dataclasses import asdict, dataclass
import json
from pathlib import Path
import time
from typing import Any, Dict


@dataclass(slots=True)
class AgentProfile:
    agent_name: str
    model_engine: str
    temperature: float
    max_retries: int = 3
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def save_to_json(self, file_path: str | Path) -> str:
        output_path = Path(file_path)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=4)
        return str(output_path)


def create_default_profile() -> AgentProfile:
    return AgentProfile(
        agent_name="DataBot_v1",
        model_engine="gpt-4-turbo",
        temperature=0.2,
    )


def mock_api_call(payload: dict, simulate_timeout: bool = False, simulate_missing_key: bool = False) -> bool:
    print("\n--- INITIATING API CALL ---")

    try:
        if simulate_missing_key:
            malformed_response = {"text": "Hello, world!"}
            malformed_response["usage_metrics"]

        if simulate_timeout:
            time.sleep(1)
            raise TimeoutError("The LLM API endpoint took too long to respond.")

        print("API Call Successful!")
        return True

    except KeyError as error:
        print(f"[CRITICAL ERROR] LLM output parsing failed. Missing expected key: {error}")

    except TimeoutError as error:
        print(f"[NETWORK ERROR] {error} Switching to backup endpoint...")

    finally:
        print("API transaction finalized (Connection Closed).")

    return False
