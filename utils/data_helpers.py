import pandas as pd
import re

def compare_answers(solution_list, student_answers):
    output = []
    for solution, student in zip(solution_list, student_answers):
        if student == "NA":
            output.append("Not Attempted")
        elif student == solution:
            output.append("Correct")
        else:
            output.append("Incorrect")
    return output

def generate_student_responses(num_students=100):
    import random
    total_questions = 90
    numeric_ranges = [(20, 30), (50, 60), (80, 90)]

    responses = []

    for _ in range(num_students):
        student_response = []
        for q in range(1, total_questions + 1):
            if any(start <= q <= end for start, end in numeric_ranges):
                student_response.append("NA")
            else:
                student_response.append(random.randint(1, 4))

        available_positions = [pos for start, end in numeric_ranges for pos in range(start, end)]
        selected_positions = random.sample(available_positions, 5)

        for pos in selected_positions:
            student_response[pos - 1] = round(random.uniform(-100, 100), 1)

        responses.append(student_response)

    return responses

def extract_solution_list(solution_text):
    return [int(num) for num in re.findall(r'\((\d+)\)', solution_text)]
