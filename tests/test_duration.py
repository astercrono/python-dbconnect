import datetime
from context import dbconnect
Duration = dbconnect.models.Duration

# Test adding and subtracting
def test_duration_add_new():
	expected_duration = Duration(datetime.timedelta(hours=1, minutes=5, seconds=1))
	zero_duration = Duration(datetime.timedelta(0))

	new_duration = zero_duration.add_new(expected_duration)
	assert expected_duration == new_duration

def test_duration_add():
	expected_duration = Duration(datetime.timedelta(hours=1, minutes=5, seconds=1))
	test_duration = Duration(datetime.timedelta(0))

	test_duration.add(expected_duration)
	assert expected_duration == test_duration

def test_duration_sub_new():
	sub_duration = Duration(datetime.timedelta(hours=1, minutes=5, seconds=1))
	expected_duration = Duration(datetime.timedelta(0))

	new_duration = sub_duration.sub_new(sub_duration)
	assert expected_duration == new_duration

def test_duration_sub():
	sub_duration = Duration(datetime.timedelta(hours=1, minutes=5, seconds=1))
	expected_duration = Duration(datetime.timedelta(0))

	sub_duration.sub(sub_duration)
	assert expected_duration == sub_duration

# Test standard "precise" format
def test_format_hour_precise():
	delta = datetime.timedelta(hours=2, minutes=30, seconds=47)
	duration = Duration(delta)
	expected = "2h 30m 47s"

	assert expected == duration.format()

def test_format_minute_precise():
	delta = datetime.timedelta(minutes=30, seconds=47)
	duration = Duration(delta)
	expected = "0h 30m 47s"

	assert expected == duration.format()

def test_format_second_precise():
	delta = datetime.timedelta(seconds=47)
	duration = Duration(delta)
	expected = "0h 0m 47s"

	assert expected == duration.format()

# Test "rounded" format - only shows the higheset value.
def test_format_hour_rounded():
	delta = datetime.timedelta(hours=2, minutes=50, seconds=51)
	duration = Duration(delta)
	expected = "3h"

	assert expected == duration.format_rounded()

def test_format_minute_rounded():
	delta = datetime.timedelta(minutes=30, seconds=52)
	duration = Duration(delta)
	expected = "31m"

	assert expected == duration.format_rounded()

def test_format_second_rounded():
	delta = datetime.timedelta(seconds=47)
	duration = Duration(delta)
	expected = "47s"

	assert expected == duration.format_rounded()
