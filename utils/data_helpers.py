def compare_answers(question_data, solution_data):
    """Compare questions and solutions."""
    # Dummy comparison logic (replace with real implementation)
    comparison = {"matches": 0, "errors": 0}
    for q, s in zip(question_data, solution_data):
        if q["content"] == s["content"]:
            comparison["matches"] += 1
        else:
            comparison["errors"] += 1
    return comparison
def compare_answers(question_data, solution_data):
    """Compare questions and solutions."""
    # Dummy comparison logic (replace with real implementation)
    comparison = {"matches": 0, "errors": 0}
    for q, s in zip(question_data, solution_data):
        if q["content"] == s["content"]:
            comparison["matches"] += 1
        else:
            comparison["errors"] += 1
    return comparison
