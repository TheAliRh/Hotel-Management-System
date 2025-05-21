"""
Dedicated custome exception handler.
"""


class BusinessRuleViolation(Exception):
    def __init__(
        self, message: str, code: int = 400, error_type: str = "business_rule"
    ):
        self.message = message
        self.code = code
        self.error_type = error_type
