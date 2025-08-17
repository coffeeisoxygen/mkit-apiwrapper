"""password hashing utilities.

menggunakan argon2
"""

from argon2 import PasswordHasher


class Hasher:
    """Utility class untuk hash & verify password menggunakan Argon2."""

    def __init__(self):
        self._ph = PasswordHasher()

    def hash(self, password: str) -> str:
        """Hash password plain text."""
        return self._ph.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        """Verifikasi password plain text dengan hash."""
        try:
            return self._ph.verify(hashed, password)
        except Exception:
            return False
