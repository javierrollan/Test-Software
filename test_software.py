import pandas as pd
import random
from datetime import datetime
import os
from prettytable import PrettyTable

# Load the Excel file into a pandas DataFrame
try:
    df = pd.read_excel('practice_test.xlsx')
except FileNotFoundError:
    print("Error: practice_test.xlsx not found.")
    print("Please make sure the file exists and contains the necessary columns.")
    exit()

# Check if the progress.xlsx file exists
progress_file_exists = os.path.isfile('progress.xlsx')

# Load the progress DataFrame or create an empty one
progress_df = pd.read_excel('progress.xlsx') if progress_file_exists else pd.DataFrame()

def practice_tests():
    global progress_df  # Declare progress_df as a global variable
    # Welcome message for practice tests
    print("Welcome to the Practice Tests!")

    # Ensure unique questions based on the "Question Weight" column
    total_questions = 125
    unique_questions = df.sample(n=total_questions, weights='Question Weight', replace=False)

    # Initialize variables to track results
    correct_answers = 0
    results = []

    # Loop through selected questions
    for i, (_, question) in enumerate(unique_questions.iterrows(), start=1):
        # Display the question number and text
        print(f"\nQuestion {i} - Domain: {question['Question Domain']} - (Weight: {question['Question Weight']}):\n{question['Question']}")

        # If it's a multiple-choice question
        if isinstance(question['Answer'], str) and ',' in question['Answer']:
            user_answer = input("\nEnter the letters of your choices (e.g., A, C): ")

            # Convert the user's answer to uppercase
            user_answer = user_answer.upper()

            # Check if the user's answer is correct
            if user_answer == question['Answer'].upper():
                print("\nCorrect!")
                correct_answers += 1
            else:
                print(f"\nWrong! The correct answer is {question['Answer']}.")
                print(f"\nExplanation: {question.get('Explanation', '')}")

        else:
            # If it's a unique solution question
            user_answer = input("Enter your answer: ")

            # Convert both answers to lowercase for case-insensitive comparison
            user_answer_lower = user_answer.lower()
            correct_answer_lower = question['Answer'].lower()

            # Check if the user's answer is correct
            if user_answer_lower == correct_answer_lower:
                print("\nCorrect!")
                correct_answers += 1
            else:
                print(f"\nWrong! The correct answer is {question['Answer']}.")
                print(f"\nExplanation: {question.get('Explanation', '')}")

        # Store results for each question
        results.append({
            'Question': f"Question {i} (Weight: {question['Question Weight']}):\n{question['Question']}",
            'User Answer': user_answer,
            'Correct Answer': question['Answer'],
            'Explanation': question.get('Explanation', ''),
            'Domain': question.get('Question Domain', '')  # Updated to 'Question Domain'
        })

    # Display the final results
    print("\nFinal Results:")
    for result in results:
        print(f"\n{result['Question']}")
        print(f"Your Answer: {result['User Answer']}")
        print(f"Correct Answer: {result['Correct Answer']}")
        print(f"Explanation: {result['Explanation']}")
        print(f"Domain: {result['Domain']}")

    # Record the results in the progress DataFrame
    attempt_number = len(progress_df) + 1
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    passed = "Passed" if correct_answers >= total_questions * 0.7 else "Failed"

    progress_data = {
        'Attempt': attempt_number,
        'Date': date,
        'Correct Questions': f"{correct_answers}/{total_questions}",
        'Status': passed
    }

    # Count correct questions per domain
    domain_count = {}
    for result in results:
        domain = result['Domain']
        if domain:
            domain_count[domain] = domain_count.get(domain, 0) + 1

    # Add domain results to progress_data
    for domain in domain_count:
        progress_data[domain] = f"{domain_count[domain]}/{total_questions}"

    # Create a new DataFrame with the updated data
    progress_df = pd.concat([progress_df, pd.DataFrame([progress_data])], ignore_index=True)

    # Save the updated progress DataFrame to the progress.xlsx file
    progress_df.to_excel('progress.xlsx', index=False, header=not progress_file_exists)

def print_results():
    global progress_df  # Declare progress_df as a global variable
    # Load the progress DataFrame from progress.xlsx
    try:
        progress_df = pd.read_excel('progress.xlsx')
    except FileNotFoundError:
        print("Error: progress.xlsx not found.")
        print("No results available.")
        return

    # Print the results in a formatted table using PrettyTable
    if not progress_df.empty:
        print("\nProgress of your Attempts:\n")
        print(progress_df.to_markdown(index=False))
    else:
        print("No results available.")

# Main menu loop
while True:
    print("\nMenu:")
    print("1) Practice Tests")
    print("2) Review Content")
    print("3) Results")
    print("4) Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        practice_tests()
    elif choice == '2':
        print("You chose Review Content.")
        # Add your logic for Review Content here
    elif choice == '3':
        print_results()
    elif choice == '4':
        print("Exiting the script. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")