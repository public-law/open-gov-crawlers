def fixture(country: str, subdiv: str, filename: str) -> str:
    return open(f"tests/fixtures/{country}/{subdiv}/{filename}", encoding="utf8").read()
