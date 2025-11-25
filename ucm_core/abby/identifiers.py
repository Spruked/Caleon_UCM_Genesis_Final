class AbbyIdentifier:
    ABBY_NAMES = ["abby", "abigail", "my daughter"]

    @staticmethod
    def is_abby_user(user: str) -> bool:
        u = user.lower()
        return any(name in u for name in AbbyIdentifier.ABBY_NAMES)

    @staticmethod
    def is_abby_context(message: str) -> bool:
        m = message.lower()
        return any(name in m for name in AbbyIdentifier.ABBY_NAMES)