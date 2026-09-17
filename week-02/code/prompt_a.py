import numpy as np
import pandas as pd


def analyze_student_marks(data):
    """Analyzes student marks data and generates class summary metrics.

    Parameters:
        data (dict or pd.DataFrame): Student data containing 'Name', 'Math',
          'Science', and 'English' scores.

    Returns:
        pd.DataFrame: Comprehensive summary showing total, average, grade, and
        status.
    """
    # Load into DataFrame
    df = pd.DataFrame(data)

    subject_cols = ["Math", "Science", "English"]

    # Calculate total and average marks
    df["Total Marks"] = df[subject_cols].sum(axis=1)
    df["Average Marks"] = df[subject_cols].mean(axis=1).round(2)

    # Determine Pass/Fail status (Passing threshold: 40 per subject)
    df["Status"] = np.where((df[subject_cols] >= 40).all(axis=1), "Pass", "Fail")

    # Assign Letter Grade based on average score
    conditions = [
        (df["Average Marks"] >= 90),
        (df["Average Marks"] >= 80),
        (df["Average Marks"] >= 70),
        (df["Average Marks"] >= 60),
        (df["Average Marks"] >= 40),
    ]
    grades = ["A+", "A", "B", "C", "D"]
    df["Grade"] = np.select(conditions, grades, default="F")

    return df


def generate_class_insights(df, subject_cols=["Math", "Science", "English"]):
    """Prints overall class performance statistics."""
    print("=" * 45)
    print("            CLASS OVERVIEW SUMMARY            ")
    print("=" * 45)

    print(f"Total Students Analyzed : {len(df)}")
    print(f"Pass Percentage         : {(df['Status'] == 'Pass').mean() * 100:.1f}%")
    print(
        f"Top Performer           : {df.loc[df['Total Marks'].idxmax(), 'Name']} ({df['Total Marks'].max()} pts)"
    )

    print("\n" + "-" * 45)
    print("Subject-Wise Performance Metrics:")
    print("-" * 45)

    subject_stats = pd.DataFrame(
        {
            "Mean": df[subject_cols].mean().round(2),
            "Max": df[subject_cols].max(),
            "Min": df[subject_cols].min(),
            "Std Dev": df[subject_cols].std().round(2),
        }
    )
    print(subject_stats)
    print("=" * 45)


# Sample Data
student_data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank"],
    "Math": [88, 42, 95, 30, 78, 65],
    "Science": [92, 55, 98, 45, 82, 58],
    "English": [79, 38, 91, 50, 85, 62],
}

# Run Analysis
analyzed_df = analyze_student_marks(student_data)

# Display Individual Results
print("\nIndividual Student Results:")
print(
    analyzed_df[
        [
            "Name",
            "Math",
            "Science",
            "English",
            "Total Marks",
            "Average Marks",
            "Grade",
            "Status",
        ]
    ]
)

# Display Summary Insights
generate_class_insights(analyzed_df)