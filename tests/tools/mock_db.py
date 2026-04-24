class FakeResult:
    """
    Simple mock of a SQLAlchemy Result object that supports the methods used in the gateway code, allowing tests to specify rows, scalar counts, and single results as needed.
    """
    def __init__(self, rows=None, one=None, count=None):
        self._rows = rows or []
        self._one = one
        self._count = count

    def scalars(self):
        return self

    def all(self):
        return self._rows

    def one_or_none(self):
        return self._one

    # Matching the gateway/db code, func.count is assumed to be the only case where scalar_one is used
    def scalar_one(self):
        return self._count


class FakeSession:
    """
    Simple mock of a SQLAlchemy session that returns predefined results for execute calls and records executed statements for verification in tests.
    """
    def __init__(self, responses):
        self.responses = list(responses)
        self.executed = []

    async def execute(self, statement):
        self.executed.append(statement)
        return self.responses.pop(0)