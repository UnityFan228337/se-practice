def analyze_marks(marks, pass_mark=50):
    # Validate non-empty list
    if not marks:
        raise ValueError("The marks list cannot be empty.")
    
    # Validate mark types and ranges
    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError(f"Invalid mark '{mark}': All marks must be numeric (int or float).")
        if mark < 0 or mark > 100:
            raise ValueError(f"Invalid mark '{mark}': Marks must be between 0 and 100.")
            
    total = sum(marks)
    count = len(marks)
    
    avg_mark = total / count
    highest_mark = max(marks)
    lowest_mark = min(marks)
    
    passed_count = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = round((passed_count / count) * 100, 2)
    
    return {
        "average": round(avg_mark, 2) if isinstance(avg_mark, float) else avg_mark,
        "highest": highest_mark,
        "lowest": lowest_mark,
        "pass_rate": pass_rate
    }


# Optional console input interaction
if __name__ == "__main__":
    user_input = input("Enter marks separated by spaces: ").strip()
    if user_input:
        try:
            # Parse inputs into float/int
            parsed_marks = []
            for item in user_input.split():
                val = float(item)
                parsed_marks.append(int(val) if val.is_integer() else val)
            
            result = analyze_marks(parsed_marks)
            print("Analysis Result:", result)
        except ValueError as e:
            print("Error:", e)


# --- Unit Tests covering all required test cases ---
def run_tests():
    # Test 1: Standard case
    res1 = analyze_marks([40, 60, 80], 50)
    print(res1)
    assert res1 == {"average": 60, "highest": 80, "lowest": 40, "pass_rate": 66.67}

    # Test 2: One mark
    res2 = analyze_marks([100], 50)
    print(res2)
    assert res2 == {"average": 100, "highest": 100, "lowest": 100, "pass_rate": 100}

    # Test 3: Decimals & Custom pass_mark
    res3 = analyze_marks([49.5, 50], 50)
    print(res3)
    assert res3 == {"average": 49.75, "highest": 50, "lowest": 49.5, "pass_rate": 50}

    # Test 4: Empty list
    try:
        analyze_marks([], 50)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test 5: Text value inside list
    try:
        analyze_marks([40, "60"], 50)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test 6: Out of range values (< 0 or > 100)
    try:
        analyze_marks([-1, 50, 101], 50)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    print("All tests passed successfully!")

run_tests()