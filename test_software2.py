import pandas as pd
import random
from datetime import datetime

# Load the Excel file into a pandas DataFrame
try:
    df = pd.read_excel('practice_test.xlsx')
except FileNotFoundError:
    print("Error: practice_test.xlsx not found.")
    print("Please make sure the file exists and contains the necessary columns.")
    exit()

def practice_tests():
    # Welcome message for practice tests
    print("Welcome to the Practice Tests!")

    # Select a maximum of 10 random questions from the pool
    selected_questions = random.sample(range(len(df)), min(10, len(df)))

    # Initialize variables to track results
    correct_answers = 0
    results = []

    # Loop through selected questions
    for i, question_index in enumerate(selected_questions, start=1):
        question = df.iloc[question_index]

        # Display the question number and text
        print(f"\nQuestion {i}:\n{question['Question']}")

        # If it's a multiple-choice question
        if isinstance(question['Answer'], str) and ',' in question['Answer']:
            user_answer = input("Enter the letters of your choices (e.g., A, C): ")

            # Convert the user's answer to uppercase
            user_answer = user_answer.upper()

            # Check if the user's answer is correct
            if user_answer == question['Answer'].upper():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct answer is {question['Answer']}.")

        else:
            # If it's a unique solution question
            user_answer = input("Enter your answer: ")

            # Check if the user's answer is correct
            if user_answer.lower() == question['Answer'].lower():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct answer is {question['Answer']}.")

        # Store results for each question
        results.append({
            'Question': f"Question {i}:\n{question['Question']}",
            'User Answer': user_answer,
            'Correct Answer': question['Answer'],
            'Explanation': question.get('Explanation', '')
        })

    # Display the final results
    print("\nFinal Results:")
    for result in results:
        print(f"\n{result['Question']}")
        print(f"Your Answer: {result['User Answer']}")
        print(f"Correct Answer: {result['Correct Answer']}")
        print(f"Explanation: {result['Explanation']}")

    # Record the results in the progress.xlsx file
    attempt_number = len(pd.read_excel('progress.xlsx')) + 1
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_questions = len(selected_questions)
    passed = "Passed" if correct_answers >= total_questions * 0.7 else "Failed"

    progress_data = {
        'Attempt': attempt_number,
        'Date': date,
        'Correct Questions': correct_answers,
        'Passed': passed
    }

    progress_df = pd.DataFrame([progress_data])
    progress_df.to_excel('progress.xlsx', index=False, header=not bool(attempt_number))

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
        print("You chose Results.")
        # Add your logic for Results here
    elif choice == '4':
        print("Exiting the script. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")