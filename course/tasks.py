from datetime import datetime
from course.models import CourseSession
from django.db.models import Q


def get_current_month():
    """
    Returns the current month as an integer (1 for January, 12 for December).
    """
    return datetime.now().month


def get_all_session_for_current_month():
    """Get all sessions that the started in the current month"""

    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        start_of_next_month = datetime(now.year + 1, 1, 1)
    else:
        start_of_next_month = datetime(now.year, now.month + 1, 1)

    return CourseSession.objects.filter(
        Q(start_date__gte=start_of_month, start_date__lt=start_of_next_month)
    )


def calculate_tutor_payment_for_month():
    # - get the number of students that was active for more that 3 weeks for a course with active session
    # - multiply the amount for the course by the number of students
    # - calculate 15% of the total amount
    # - once payment is been made record for the course session is recorded in paid table
    # - get all sessions that started in the current month, if session not has been paid for include
    pass
