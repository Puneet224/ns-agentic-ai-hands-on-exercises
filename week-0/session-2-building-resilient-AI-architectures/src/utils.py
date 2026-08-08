def greet(name: str) -> str:
    """Return a greeting string for notebook and script use."""
    return f"Hello, {name}! Welcome to the project."


if __name__ == "__main__":
    print(greet("world"))
