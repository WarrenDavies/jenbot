

@dataclass
class WorkingMemoryRuleset():
    # Need to move to schemas/
    max_messages: int = 8
    max_summaries: int = 2
    max_memories: int = 5
    memory_confidence_threshold: float = 0.7