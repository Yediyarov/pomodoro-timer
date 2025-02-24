class UserNotFound(Exception):
    detail = "User not found"

class UserAlreadyExists(Exception):
    detail = "User already exists"

class InvalidCredentials(Exception):
    detail = "Invalid credentials"

class InvalidToken(Exception):
    detail = "Invalid token"

