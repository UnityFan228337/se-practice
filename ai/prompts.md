1. How will marks be entered into the app?

2. Who is this tool mainly for?

rewritten prompt: A simple, personal-use web tool where you paste a comma-separated or line-by-line list of student marks and instantly see the key stats — average, highest mark, lowest mark, and pass rate — displayed cleanly on screen. No login, no setup, just fast results.


input <br/>
85, 23, 45, 90, 92 - MarksAnalyzer — Results<br/>

output:<br/>
─────────────────────────<br/>
Total Marks:        5 <br/>
Average:            67.00 <br/>
Median:             85.00<br/>
Std Deviation:      27.92<br/>
Highest:            92<br/>
Lowest:             23<br/>
Pass (≥50):     3 (60.0%)<br/>
Fail (<50):      2 (40.0%)<br/>

----------------------------------------------------

input<br/>
88, 47, -5, 101, abc, 73, 50, , 100	- MarksAnalyzer — Results<br/>
output<br/>
─────────────────────────<br/>
Total Marks:        5<br/>
Average:            71.60<br/>
Median:             73.00<br/>
Std Deviation:      20.73<br/>
Highest:            100<br/>
Lowest:             47<br/>
Pass (≥50):     4 (80.0%)<br/>
Fail (<50):      1 (20.0%)<br/>

-------------------------------------------------------


input<br/>
10, 20, 30 - MarksAnalyzer — Results<br/>
output<br/>
─────────────────────────<br/>
Total Marks:        3<br/>
Average:            20.00<br/>
Median:             20.00<br/>
Std Deviation:      8.16<br/>
Highest:            30<br/>
Lowest:             10<br/>
Pass (≥50):     0 (0.0%)<br/>
Fail (<50):      3 (100.0%)<br/>

-------------------------------------------


input<br/>
abc, , xyz<br/>

output<br/>
2 invalid entries skipped
("abc", "xyz")<br/>
No valid marks found. Enter numbers between 0 and 100, separated by commas or newlines.