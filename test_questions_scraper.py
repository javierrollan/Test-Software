import pandas as pd
from bs4 import BeautifulSoup

# Read HTML from file
with open('test_questions.html', 'r', encoding='utf-8') as file:
    html_code = file.read()

# Parse the HTML
soup = BeautifulSoup(html_code, 'html.parser')

# Find all containers for questions
all_questions_containers = soup.find_all('div', class_='questions_container')

# Load existing data from the Excel file
try:
    existing_data = pd.read_excel('practice_test.xlsx')
    question_id_start = existing_data['Question ID'].max() + 1
    print("Existing Data:")
    print(existing_data)
except FileNotFoundError:
    # If the file doesn't exist, start from Question ID 1
    question_id_start = 1
    existing_data = pd.DataFrame(columns=['Question ID', 'Question Weight', 'Question Domain',
                                          'Question Origin', 'Question', 'Answer', 'Explanation'])
    print("No existing data found.")

# List to store question information
questions_list = []

# Iterate through each questions_container
for questions_container in all_questions_containers:
    # Find all question cards within the container
    question_cards = questions_container.find_all('div', class_='card question_card')

    # Iterate through each question card
    for i, question_card in enumerate(question_cards, start=1):
        # Find the question text
        question_text = question_card.find('div', class_='question_text').find('p').get_text(strip=True)

        # Find the choices
        choices_list = question_card.find('ul', class_='choices-list')
        choices = [choice.get_text(strip=True) for choice in choices_list.find_all('li')]

        # Join choices with newline characters
        choices_text = '\n'.join(choices)

        # Append choices to the end of the question text
        question_text_with_choices = f"{question_text}\n{choices_text}"

        # Find the correct answer
        correct_answer = question_card.find('div', class_='answer_block').get('data-answer')

        # Store question information in a dictionary
        question_info = {
            'Question ID': question_id_start,
            'Question Weight': None,
            'Question Domain': None,
            'Question Origin': 'CEHv12 Certlibrary',
            'Question': question_text_with_choices,
            'Answer': correct_answer,
            'Explanation': None
        }

        # Append the dictionary to the list
        questions_list.append(question_info)

        # Increment the Question ID for the next question
        question_id_start += 1

# Append new data to the existing DataFrame
existing_data = pd.concat([existing_data, pd.DataFrame(questions_list)], ignore_index=True)

# Save the updated DataFrame to the Excel file
existing_data.to_excel('practice_test.xlsx', index=False)
print("Updated Data:")
print(existing_data)