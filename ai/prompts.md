1. How will marks be entered into the app?

2. Who is this tool mainly for?

rewritten prompt: A simple, personal-use web tool where you paste a comma-separated or line-by-line list of student marks and instantly see the key stats — average, highest mark, lowest mark, and pass rate — displayed cleanly on screen. No login, no setup, just fast results.


input
85, 23, 45, 90, 92 - MarksAnalyzer — Results

output:
─────────────────────────
Total Marks:        5
Average:            67.00
Median:             85.00
Std Deviation:      27.92
Highest:            92
Lowest:             23
Pass (≥50):     3 (60.0%)
Fail (<50):      2 (40.0%)

----------------------------------------------------

input
88, 47, -5, 101, abc, 73, 50, , 100	- MarksAnalyzer — Results
output
─────────────────────────
Total Marks:        5
Average:            71.60
Median:             73.00
Std Deviation:      20.73
Highest:            100
Lowest:             47
Pass (≥50):     4 (80.0%)
Fail (<50):      1 (20.0%)

-------------------------------------------------------


input
10, 20, 30 - MarksAnalyzer — Results
output
─────────────────────────
Total Marks:        3
Average:            20.00
Median:             20.00
Std Deviation:      8.16
Highest:            30
Lowest:             10
Pass (≥50):     0 (0.0%)
Fail (<50):      3 (100.0%)

-------------------------------------------


input
abc, , xyz

output
2 invalid entries skipped
("abc", "xyz")
No valid marks found. Enter numbers between 0 and 100, separated by commas or newlines.