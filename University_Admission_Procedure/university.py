def mean(scores: list) -> float:
    """Return the mean of a list of numbers."""
    scores = [int(x) for x in scores]
    _mean = sum(scores) / len(scores)
    return round(_mean, 2)


def mean_score(applicant: list, department: str) -> float:
    """Return the mean score of the relevant exam scores of an applicant for the department he is applying for."""
    grade_indices = {"physics": 2,
                     "chemistry": 3,
                     "math": 4,
                     "cs": 5}

    relevant_grades = {"Biotech": ["chemistry", "physics"],
                       "Chemistry": ["chemistry"],
                       "Engineering": ["cs", "math"],
                       "Mathematics": ["math"],
                       "Physics": ["physics", "math"]}
    scores = []
    for grade in relevant_grades[department]:
        scores.append(applicant[grade_indices[grade]])
    return mean(scores)


def better_score(applicant: list, department: str) -> float:
    """Return the better score between the mean score for the department or the score from the special exam."""
    score = mean_score(applicant, department)
    special_score = int(applicant[6])
    return score if score >= special_score else special_score


def get_applicants(filename: str) -> list:
    """Return a list of all the applicants read from a file with passed filename."""
    with open(filename, "r") as file:
        return [applicant.strip("\n").split() for applicant in file]


def accept_applicants(departments: dict, max_per_department: int, applicant_list: list) -> dict:
    """Return a dictionary that represents the departments with their students.

    :param departments: A dictionary that contains all the departments with their students.
    :param max_per_department: The maximum number of students per department.
    :param applicant_list: A list of all the applicants.

    :return: A dictionary that contains all the departments with their students
    """
    for i in [7, 8, 9]:  # indices for the 1., 2. and 3. priority department per applicant

        # Sort by the grade relevant for the department (descending), first priority,
        # first name, last name, second priority, third priority
        sorted_applicant_list = sorted(applicant_list, key=lambda x: (-better_score(x, x[i]),
                                                                      x[7], x[0], x[1], x[8], x[9]))

        for applicant in sorted_applicant_list:
            if len(departments[applicant[i]]) < max_per_department:
                departments[applicant[i]].append(applicant)
                index = applicant_list.index(applicant)
                del applicant_list[index]

    return departments
    

def save_accepted_students(departments: dict) -> None:
    """Save the accepted students to a separate file for each department."""
    for key in departments.keys():
        departments[key] = sorted(departments[key], key=lambda x: (-better_score(x, key), x[0], x[1]))
        file_name = key + ".txt"
        with open(file_name, "w") as file:
            for student in departments[key]:
                file.write(f"{student[0]} {student[1]} {better_score(student, key)}\n")


def main():
    departments = {"Biotech": [],
                   "Chemistry": [],
                   "Engineering": [],
                   "Mathematics": [],
                   "Physics": []}

    max_students = int(input())
    applicant_list = get_applicants("applicant_list.txt")
    departments = accept_applicants(departments, max_students, applicant_list)
    save_accepted_students(departments)


if __name__ == "__main__":
    main()
