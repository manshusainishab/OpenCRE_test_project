def structural_code_filter(commit):
    """
    Placeholder for CodeRabbit.
    Currently naive heuristic:
    If commit message contains refactor/lint/format → discard
    """

    msg = commit["message"].lower()

    structural_keywords = [
        "refactor",
        "format",
        "lint",
        "cleanup",
        "rename",
        "restructure"
    ]

    if any(k in msg for k in structural_keywords):
        return False  # not meaningful

    return True  # meaningful code change