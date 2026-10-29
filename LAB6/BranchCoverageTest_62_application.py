import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning,
)


# Attendance percentage: validation branches

def test_total_zero():
    with pytest.raises(ValueError):
        attendance_percent(10, 0, 0)


def test_total_negative():
    with pytest.raises(ValueError):
        attendance_percent(10, -1, 0)


def test_attended_negative():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)


def test_attended_exceeds_total():
    with pytest.raises(ValueError):
        attendance_percent(41, 40, 0)


def test_attended_valid():
    assert attendance_percent(20, 40, 0) == 50


# Medical leave boundary tests

def test_medical_leave_above_five():
    assert attendance_percent(20, 40, 6) == 62


def test_medical_leave_equal_to_five():
    assert attendance_percent(20, 40, 5) == 62


def test_medical_leave_below_five():
    assert attendance_percent(20, 40, 2) == 55


# Credited attendance boundary tests

def test_credited_above_total():
    assert attendance_percent(39, 40, 5) == 100


def test_credited_below_total():
    assert attendance_percent(20, 40, 2) == 55


# Exam eligibility branches

def test_fees_not_paid():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_attendance_above_75():
    assert exam_eligibility(80, False, True) == "eligible"


def test_attendance_equal_to_75():
    assert exam_eligibility(75, False, True) == "eligible"


def test_attendance_between_65_and_75_with_condonation():
    assert exam_eligibility(70, True, True) == "eligible"


def test_attendance_between_65_and_75_without_condonation():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_attendance_equal_to_65():
    assert exam_eligibility(65, True, True) == "eligible"


def test_attendance_below_65():
    assert exam_eligibility(64, True, True) == "detained"


# Attendance warning branches

def test_warning_above_85():
    assert attendance_warning(90, 2) is None


def test_warning_equal_to_85():
    assert attendance_warning(85, 5) is None


def test_critical_when_more_than_four_weeks():
    assert attendance_warning(74, 5) == "critical"


def test_final_notice_at_four_weeks():
    assert attendance_warning(74, 4) == "final notice"


def test_final_notice_below_four_weeks():
    assert attendance_warning(60, 2) == "final notice"


def test_reminder_at_75():
    assert attendance_warning(75, 2) == "reminder"


def test_reminder_below_85():
    assert attendance_warning(80, 3) == "reminder"