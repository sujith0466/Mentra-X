class DifficultyPolicy:
    """
    Abstracts branching rules for the adaptive assessment engine.
    Supports varying strategies in the future based on student style or exam track.
    """
    def __init__(self, min_difficulty: int = 1, max_difficulty: int = 5):
        self.min_difficulty = min_difficulty
        self.max_difficulty = max_difficulty

    def get_next_difficulty(self, current_difficulty: int, is_correct: bool) -> int:
        """
        Determines the next question's difficulty tier.
        Default algorithm: Escalates by 1 on correct, decays by 1 on incorrect.
        """
        if is_correct:
            return min(self.max_difficulty, current_difficulty + 1)
        return max(self.min_difficulty, current_difficulty - 1)
