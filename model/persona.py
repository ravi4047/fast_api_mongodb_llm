class PhaseAdapt:
    """There are various phases and their scores"""
    def __init__(self, agreement:float, challenge:float, vulnerability:float, affection:float, curiosity:float) -> None:
        self.agreement_rate = agreement
        self.challenge_level = challenge
        self.vulnerability_level = vulnerability
        self.affection_level = affection
        self.curiosity_level = curiosity

