# ALL CREDIT GOES TO JASON LIN (https://jasonthel.in)

import csv
import re

# not in a context manager because indents are expensive around these parts
f = open('./f.csv', 'r')
reader = csv.DictReader(f)

for submission in reader:
    # assume we are given "Question X Weight", "Question X Student Response(s)", and "Question X Correct Response" for every valid question
    score = 0

    for key in submission.keys():
        # find each question by searching for "Question X Weight"
        question = re.match(r'Question (\d+) Weight', key)
        if not question:
            continue

        question = question.groups(1)[0]  # the question number

        weight = int(submission[f'Question {question} Weight'])

        correct_responses = submission[f'Question {question} Correct Response'].split(
            ', ')
        student_responses = submission[f'Question {question} Student Response(s)'].split(
            ', ')

        # print(f'{question=} {weight=} {correct_responses=} {student_responses=}')

        if len(correct_responses) == 1:
            # single choice answer, just add points if they match
            # assume student can't select more than 1 answer if it's single choice
            if correct_responses[0] == student_responses[0]:
                score += weight
        else:
            # assuming len(correct_response) == weight, and each correct response is worth 1 point
            # each incorrect response subtracts a point
            score_for_prob = 0
            for student_choice in student_responses:
                if student_choice in correct_responses:
                    score_for_prob += 1
                else:
                    score_for_prob -= 1

            # can't lose total points for getting multiple incorrect
            score += max(0, score_for_prob)

    print(f"{submission['Student ID']} {score=}")

f.close()
