def fixture(country: str, subdiv: str, filename: str) -> str:
    return open(f"tests/fixtures/{country}/{subdiv}/{filename}", encoding="utf8").read()


class NullLogger:
    def warn(self, message: str) -> None:
        pass

# An instance of NullLogger that can be used in tests.
null_logger = NullLogger()
