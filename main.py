import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file into a pandas DataFrame
df = pd.read_csv('student_scores_random_names.csv')


def failed_students():
    students_below_50 = (df.iloc[:, 3:] < 50).any(axis=1)
    failed_students_list = pd.Series(df.loc[students_below_50, 'Student'].unique())  # Convert to Series

    print("Students with less than 50 points:")
    print(failed_students_list.to_string(index=False))  # Use .to_string() on Series


def average_score_for_each_subject():
    averages = df.iloc[:, 3:].mean()
    print("\nAverage score for each subject:")
    for subject, avg in averages.items():
        print(f"{subject}: {avg:.2f}")

def student_with_highest_average():
    # Calculate the average for each student across all subjects
    df['Average'] = df.iloc[:, 3:].mean(axis=1)  # Take mean across subject columns for each row

    # Group by student and calculate their overall average across all semesters
    student_avg = df.groupby('Student')['Average'].mean()

    # Find the student(s) with the maximum average
    max_avg = student_avg.max()
    top_students = student_avg[student_avg == max_avg]

    print("Student(s) with the highest average points across all semesters and subjects:")
    for student, avg in top_students.items():
        print(f"{student}: {avg:.2f}")

def subject_with_least_average():
    # Calculate the average for each subject across all semesters
    subject_averages = df.iloc[:, 3:].mean()

    # Find the subject with the minimum average score
    min_avg = subject_averages.min()
    subject_with_min_avg = subject_averages[subject_averages == min_avg]

    print("Subject(s) with the least average points across all semesters:")
    for subject, avg in subject_with_min_avg.items():
        print(f"{subject}: {avg:.2f}")


def generate_avg_by_semester():
    # Group by 'Semester' and calculate the mean for each subject within each semester
    avg_by_semester = df.groupby('Semester').mean(numeric_only=True)

    # Save the result into an Excel file
    avg_by_semester.to_excel('average_points_by_semester.xlsx')

    print("DataFrame with average points per semester saved as 'average_points_by_semester.xlsx'")
    print(avg_by_semester)


def students_improving():
    # Sort the DataFrame by Student and Semester
    df.sort_values(by=['Student', 'Semester'], inplace=True)

    improving_students = []

    # Group by Student
    grouped = df.groupby('Student')

    for student, group in grouped:
        # Extract only the scores for the subjects
        scores = group.iloc[:, 3:]  # Assuming the first columns are 'Student', 'Semester', etc.

        # Calculate the average score for each semester for this student
        semester_avg = scores.mean(axis=1)

        # Check if all semester averages are increasing
        if (semester_avg.diff().dropna() > 0).all():
            improving_students.append(student)

    print("Students who consistently improved their scores across semesters:")
    if improving_students:
        for student in improving_students:
            print(student)
    else:
        print("No students consistently improved.")


# Calculate average points per subject across all semesters
def average_points_per_subject():
    # Group by Semester and calculate the mean for each subject
    avg_by_subject = df.iloc[:, 3:].mean()

    # Create a column diagram (bar plot)
    plt.figure(figsize=(12, 6))
    bars = plt.bar(avg_by_subject.index, avg_by_subject.values)
    sns.barplot(x=avg_by_subject.index, y=avg_by_subject.values)
    plt.title('Average Points of Each Subject Across All Semesters')
    plt.xlabel('Subjects')
    plt.ylabel('Average Points')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Calculate overall average points by semester
def average_points_per_semester():
    # Group by Semester and calculate the overall mean for each semester
    avg_by_semester = df.groupby('Semester').mean(numeric_only=True).mean(axis=1)

    # Create a line diagram
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=avg_by_semester.index, y=avg_by_semester.values, marker='o')
    plt.title('Average Overall Points According to Semesters')
    plt.xlabel('Semester')
    plt.ylabel('Average Points')
    plt.xticks(rotation=45)
    plt.show()

failed_students()
average_score_for_each_subject()
student_with_highest_average()
subject_with_least_average()
generate_avg_by_semester()
students_improving()
average_points_per_subject()
average_points_per_semester()