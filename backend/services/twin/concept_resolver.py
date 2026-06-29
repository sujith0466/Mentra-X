class ConceptResolver:
    """
    Abstracts concept extraction from existing Mentra models to provide
    a unified concept representation for the Twin Knowledge State.
    """

    @staticmethod
    def resolve_from_quiz(quiz_title: str) -> str:
        """
        In Phase 1, we use the quiz title to generate a normalized concept tag.
        E.g. 'Python Basics Quiz 1' -> 'python_basics_quiz_1'
        """
        if not quiz_title:
            return "unknown_concept"
        return quiz_title.strip().lower().replace(' ', '_')
    
    @staticmethod
    def resolve_from_coding_topic(topic: str) -> str:
        """
        In Phase 1, we use the coding challenge topic to generate a normalized concept tag.
        """
        if not topic:
            return "unknown_coding_concept"
        return topic.strip().lower().replace(' ', '_')
