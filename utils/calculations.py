
# Calculation functions for Good Grade


def calculate_current_grade(evaluations):
    """
    Calculates the student's current grade using only
    the evaluations that already have a grade.
    """

    accumulated_points = 0
    evaluated_percentage = 0

    for evaluation in evaluations:

        grade = evaluation.get("grade")
        weight = evaluation.get("weight", 0)

        if grade is not None:
            accumulated_points += grade * (weight / 100)
            evaluated_percentage += weight

    if evaluated_percentage == 0:
        return 0.0

    current_grade = (
        accumulated_points / evaluated_percentage
    ) * 100

    return round(current_grade, 2)


def calculate_accumulated_points(evaluations):
    """
    Calculates how many points the student has already
    secured toward the final grade.
    """

    accumulated_points = 0

    for evaluation in evaluations:

        grade = evaluation.get("grade")
        weight = evaluation.get("weight", 0)

        if grade is not None:
            accumulated_points += grade * (weight / 100)

    return round(accumulated_points, 2)


def calculate_evaluated_percentage(evaluations):
    """
    Calculates what percentage of the course
    has already been graded.
    """

    evaluated_percentage = 0

    for evaluation in evaluations:

        if evaluation.get("grade") is not None:
            evaluated_percentage += evaluation.get("weight", 0)

    return round(evaluated_percentage, 2)


def calculate_remaining_percentage(evaluations):
    """
    Calculates what percentage of the course
    is still pending.
    """

    evaluated = calculate_evaluated_percentage(evaluations)

    return round(100 - evaluated, 2)


def calculate_needed_grade(target_grade, evaluations):
    """
    Calculates the average grade needed in the remaining
    evaluations to finish the course with the desired target.
    """

    accumulated = calculate_accumulated_points(evaluations)

    evaluated_percentage = calculate_evaluated_percentage(
        evaluations
    )

    remaining_percentage = 100 - evaluated_percentage

    if remaining_percentage <= 0:
        return None

    needed_grade = (
        target_grade - accumulated
    ) / (remaining_percentage / 100)

    return round(needed_grade, 2)


def is_target_possible(target_grade, evaluations, max_grade=10):
    """
    Checks whether the desired final grade
    is still mathematically possible.
    """

    needed = calculate_needed_grade(
        target_grade,
        evaluations
    )

    if needed is None:
        final_grade = calculate_accumulated_points(evaluations)
        return final_grade >= target_grade

    return needed <= max_grade


def calculate_best_possible_grade(evaluations, max_grade=10):
    """
    Calculates the highest possible final grade assuming
    the student gets the maximum grade in everything remaining.
    """

    accumulated = calculate_accumulated_points(evaluations)

    remaining_percentage = calculate_remaining_percentage(
        evaluations
    )

    best_grade = accumulated + (
        max_grade * (remaining_percentage / 100)
    )

    return round(best_grade, 2)
