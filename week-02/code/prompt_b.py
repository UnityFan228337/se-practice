def analyze_marks(marks, pass_mark=50):
    if not marks:
        raise ValueError("The marks list cannot be empty.")

    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError(f"All marks must be numeric. Found invalid value: {mark}")
        if not (0 <= mark <= 100):
            raise ValueError(f"Marks must be between 0 and 100. Found out-of-range value: {mark}")

    total_count = len(marks)
    highest = max(marks)
    lowest = min(marks)
    average = sum(marks) / total_count
    passed_count = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = (passed_count / total_count) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }