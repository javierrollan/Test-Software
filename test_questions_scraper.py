from bs4 import BeautifulSoup

# Read HTML from file
with open('test_questions.html', 'r', encoding='utf-8') as file:
    html_code = file.read()

# Parse the HTML
soup = BeautifulSoup(html_code, 'html.parser')

# Find the container for all questions
questions_container = soup.find('div', class_='questions_container')

# Find all question cards within the container
question_cards = questions_container.find_all('div', class_='card question_card')

# List to store question information
questions_list = []

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
        'question_text_with_choices': question_text_with_choices,
        'correct_answer': correct_answer
    }

    # Append the dictionary to the list
    questions_list.append(question_info)

# Print or use the list of questions as needed
for i, question_info in enumerate(questions_list, start=1):
    print(f"\nQuestion {i} Text with Choices:")
    print(question_info['question_text_with_choices'])
    print("Correct Answer:", question_info['correct_answer'])
