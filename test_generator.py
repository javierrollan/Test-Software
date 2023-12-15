import pandas as pd

# Load the existing practice_test.xlsx file into a DataFrame
try:
    existing_df = pd.read_excel('practice_test.xlsx')
except FileNotFoundError:
    # If the file does not exist, create an empty DataFrame
    existing_df = pd.DataFrame()

# Create an empty list to store updated questions
questions_list = []

# Loop through each test
for test_number in range(1, 31):
    question_text = f"Test {test_number}\n"
    
    # Loop through answer options
    for option in ['A', 'B', 'C', 'D']:
        question_text += f"{option}) Answer {option}" + ("\n" if option != 'D' else "")
    
    # Add the question to the list
    questions_list.append({'Question': question_text})

# Create a DataFrame from the list of new questions
new_questions_df = pd.DataFrame(questions_list)

# Update the existing DataFrame with the new values in the "Question" column
existing_df['Question'] = new_questions_df['Question']

# Save the updated DataFrame to the practice_test.xlsx file
existing_df.to_excel('practice_test.xlsx', index=False)