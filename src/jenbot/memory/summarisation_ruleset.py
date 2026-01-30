@dataclass
class SummarisationRuleset():
    # Need to move to schemas/
    max_tokens_to_summarise: int = 1000
    max_summary_size: int = 100