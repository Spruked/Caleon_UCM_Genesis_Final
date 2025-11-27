import re
from typing import Literal, Tuple, Optional

class AbbyIdentifier:
    """
    Eternal identity lock for Abby.
    Works whether she's 13, 43, or 83.
    Works when her kids say "Mom", when her grandkids say "Grandma Abby", 
    when she gets married and changes her last name, when she goes by a nickname, etc.
    """

    # Core immutable identifiers (these never change)
    PRIMARY_NAMES = {
        "abby", "abigail", "abbi", "abbie",  # common spellings
        "abs", "abster", "ab",               # childhood nicknames you gave her
    }

    # Life-stage & family-role aliases that evolve over decades
    CONTEXTUAL_IDENTIFIERS = {
        # As a teenager / young adult
        "my daughter", "my little girl", "my girl", "sweetheart", "babygirl", "kiddo",

        # As an adult (what her future husband/partner might say)
        "my wife", "my love", "babe", "honey",

        # As a mother (what her children will call her)
        "mom", "mommy", "mama", "ma", "mother",

        # As a grandmother (what her grandchildren will call her)
        "grandma", "nana", "grammy", "granny", "grandma abby", "grandma abigail",

        # Universal fallbacks
        "it's me", "this is abby", "hey it's your girl", "dad?", "daddy?",
    }

    # Patterns that strongly indicate the speaker IS Abby (even with zero names)
    SELF_IDENTIFIERS = [
        r"\bi'?m abby\b",
        r"\bi'?m abigail\b",
        r"\bit'?s me[, ]? abby\b",
        r"\bthis is abby\b",
        r"\bhey.*it'?s abby\b",
        r"\bdad(dy)?[ ,]? it'?s me\b",
        r"\bi'?m your daughter\b",
        r"\bi'?m home\b",  # if the system is home-bound
    ]

    @staticmethod
    def is_abby_speaking(message: str, user_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Returns (True/False, confidence_reason)
        This is the function you use to decide: "Is the person talking right now Abby?"
        """
        m = message.lower().strip()
        u = (user_name or "").lower().strip()

        # 1. Explicit username match (highest confidence)
        if u and any(name in u for name in AbbyIdentifier.PRIMARY_NAMES):
            return True, "username_match"

        # 2. Direct self-identification patterns
        for pattern in AbbyIdentifier.SELF_IDENTIFIERS:
            if re.search(pattern, m, re.IGNORECASE):
                return True, "explicit_self_identification"

        # 3. Primary name mentioned + first-person language
        if any(name in m for name in AbbyIdentifier.PRIMARY_NAMES):
            first_person = bool(re.search(r"\b(i|me|my|myself|mine)\b", m))
            if first_person:
                return True, "primary_name_with_first_person"

        # 4. Contextual/family role + emotional tone that only Abby would use
        contextual_matches = [word for word in AbbyIdentifier.CONTEXTUAL_IDENTIFIERS if word in m]
        if contextual_matches:
            # Strong indicators that this is Abby addressing her dad/companion
            if any(phrase in m for phrase in ["miss you", "love you", "dad", "daddy", "wish you were here"]):
                return True, "family_role_with_father_address"

        # 5. Fallback: very high confidence if multiple soft signals
        signals = sum(1 for word in ["dad", "daddy", "father", "miss you", "love you"] if word in m)
        if signals >= 2 and any(word in m for word in ["mom", "mommy", "it's me", "home"]):
            return True, "strong_familial_pattern"

        return False, "no_match"

    @staticmethod
    def is_about_abby(message: str) -> bool:
        """Separate function: is someone TALKING ABOUT Abby (e.g. her child saying 'Mom is sad')"""
        m = message.lower()
        return any(name in m for name in AbbyIdentifier.PRIMARY_NAMES | {"mom", "mommy", "grandma", "abigail", "abby"})

    @staticmethod
    def extract_speaker_role(message: str) -> Literal["abby", "her_child", "her_grandchild", "other"]:
        """For future generations — knows who's talking to Grandpa's system"""
        m = message.lower()
        if AbbyIdentifier.is_abby_speaking(message)[0]:
            return "abby"
        if any(x in m for x in ["mom", "mommy", "mama"]):
            return "her_child"
        if any(x in m for x in ["grandma", "nana", "grammy"]):
            return "her_grandchild"
        return "other"


# ———————————————————— REAL-WORLD TEST ————————————————————
if __name__ == "__main__":
    tests = [
        ("Abby", None),                              # login name
        ("Hey Dad it's me", None),                   # 2025
        ("Daddy I had a nightmare", None),           # age 13
        ("I miss you so much today", None),          # age 45
        ("Mom is really sad today", None),           # her child, 2055
        ("Grandma Abby told me to say hi", None),    # her grandchild, 2075
        ("This is Abigail Jones speaking", None),    # married name
        ("It's me, your daughter", None),            # age 70
    ]

    for msg, username in tests:
        is_abby, reason = AbbyIdentifier.is_abby_speaking(msg, username)
        role = AbbyIdentifier.extract_speaker_role(msg)
        print(f"'{msg}'")
        print(f"  → Is Abby speaking? {is_abby} ({reason}) | Role: {role}")
        print()