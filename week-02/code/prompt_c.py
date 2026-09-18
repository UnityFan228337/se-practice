import pytest

def analyze_marks(marks, pass_mark=50):
    """
    Analyzes a list of numerical marks and calculates basic statistics.
    
    Args:
        marks (list): List of numeric marks between 0 and 100.
        pass_mark (int/float): The threshold for passing. Defaults to 50.
        
    Returns:
        dict: Summary containing average, highest, lowest, and pass_rate.
    """
    if not marks:
        raise ValueError("The marks list cannot be empty.")

    total = 0
    highest = float('-inf')
    lowest = float('inf')
    passed_count = 0

    for mark in marks:
        # Exclude booleans explicitly (bool is a subclass of int in Python)
        if type(mark) not in (int, float):
            raise ValueError(f"Invalid value '{mark}'. All marks must be numeric.")

        if not (0 <= mark <= 100):
            raise ValueError(f"Mark {mark} is out of range. Must be between 0 and 100.")

        total += mark

        if mark > highest:
            highest = mark
        if mark < lowest:
            lowest = mark
        if mark >= pass_mark:
            passed_count += 1

    total_count = len(marks)
    
    return {
        "average": total / total_count,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": (passed_count / total_count) * 100
    }


# ==========================================
# Test Suite (pytest)
# ==========================================

def test_single_mark():
    result = analyze_marks([75])
    assert result == {
        "average": 75.0,
        "highest": 75,
        "lowest": 75,
        "pass_rate": 100.0
    }
    print("Test 'test_single_mark' passed.")

def test_decimals():
    result = analyze_marks([45.5, 60.5, 84.0])
    assert result["average"] == pytest.approx(63.3333, rel=1e-3)
    assert result["highest"] == 84.0
    assert result["lowest"] == 45.5
    assert result["pass_rate"] == pytest.approx(66.6666, rel=1e-3)
    print("Test 'test_decimals' passed.")

def test_custom_pass_mark():
    # Pass threshold raised to 70
    result = analyze_marks([40, 60, 80], pass_mark=70)
    assert result["average"] == 60.0
    assert result["highest"] == 80
    assert result["lowest"] == 40
    assert result["pass_rate"] == pytest.approx(33.3333, rel=1e-3)
    print("Test 'test_custom_pass_mark' passed.")

def test_empty_list_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        analyze_marks([])
        print("Test 'test_empty_list_raises_value_error' passed.")

def test_text_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numeric"):
        analyze_marks([50, "eighty", 90])
        print("Test 'test_text_value_raises_value_error' passed.")

def test_out_of_range_below_zero_raises_value_error():
    with pytest.raises(ValueError, match="out of range"):
        analyze_marks([50, -10, 80])
        print("Test 'test_out_of_range_below_zero_raises_value_error' passed.")

def test_out_of_range_above_hundred_raises_value_error():
    with pytest.raises(ValueError, match="out of range"):
        analyze_marks([50, 105, 80])
        print("Test 'test_out_of_range_above_hundred_raises_value_error' passed.")


