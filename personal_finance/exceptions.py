class FinanceError(Exception):
"""Base exception for the finance app"""

class AuthenticationError(FinanceError):
pass

class NotFoundError(FinanceError):
pass

class ValidationError(FinanceError):
pass
