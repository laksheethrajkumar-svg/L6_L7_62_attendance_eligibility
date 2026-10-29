import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning,
)


# Attendance percentage tests

def test_normal_attendance():
    assert attendance_percent(30, 40, 0) == 75


def test_zero_total_classes():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)


def test_negative_total_classes():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, -5, 0)


def test_negative_attended_classes():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_attended_exceeds_total():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(41, 40, 0)


def test_medical_leave_above_five_days():
    assert attendance_percent(20, 40, 6) == 62


def test_medical_leave_at_five_days():
    assert attendance_percent(20, 40, 5) == 62


def test_medical_leave_below_five_days():
    assert attendance_percent(20, 40, 2) == 55


def test_credited_attendance_capped():
    assert attendance_percent(39, 40, 5) == 100


# Exam eligibility tests

def test_fees_pending():
    assert exam_eligibility(90, False, False) == "fees pending"


def test_eligible_above_75():
    assert exam_eligibility(80, False, True) == "eligible"


def test_eligible_at_75():
    assert exam_eligibility(75, False, True) == "eligible"


def test_condonation_eligible():
    assert exam_eligibility(70, True, True) == "eligible"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_detained():
    assert exam_eligibility(60, True, True) == "detained"


# Attendance warning tests

def test_no_warning():
    assert attendance_warning(90, 2) is None


def test_no_warning_at_85():
    assert attendance_warning(85, 5) is None


def test_critical_warning():
    assert attendance_warning(60, 5) == "critical"


def test_final_notice():
    assert attendance_warning(60, 3) == "final notice"


def test_reminder():
    assert attendance_warning(80, 3) == "reminder"