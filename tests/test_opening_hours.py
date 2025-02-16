import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.opening_hours import parse_opening_hours

@pytest.mark.parametrize("input_hours, expected_output", [
    # Testing normal overnight periods
    ("Fri - Sun 20:00 - 02:00", [
        ('Friday', '20:00', '24:00'),
        ('Saturday', '00:00', '02:00'),
        ('Saturday', '20:00', '24:00'),
        ('Sunday', '00:00', '02:00'),
        ('Sunday', '20:00', '24:00'),
        ('Monday', '00:00', '02:00')
    ]),

    # Test single day overnight
    ("Mon 23:00 - 02:00", [
        ('Monday', '23:00', '24:00'),
        ('Tuesday', '00:00', '02:00')
    ]),

    # Test normal time period (not overnight)
    ("Wed 08:00 - 12:00", [
        ('Wednesday', '08:00', '12:00')
    ]),

    # Test multiple days without overnight
    ("Tue - Thu 09:00 - 18:00", [
        ('Tuesday', '09:00', '18:00'),
        ('Wednesday', '09:00', '18:00'),
        ('Thursday', '09:00', '18:00')
    ]),

    # Test weekend overnight
    ("Sat - Sun 22:00 - 03:00", [
        ('Saturday', '22:00', '24:00'),
        ('Sunday', '00:00', '03:00'),
        ('Sunday', '22:00', '24:00'),
        ('Monday', '00:00', '03:00')
    ]),
    
    # Multiple days separated by different days
    ("Mon - Wednesday 08:00 - 17:00 / Sat, Sun 08:00 - 12:00", [
        ('Monday', '08:00', '17:00'),
        ('Tuesday', '08:00', '17:00'),
        ('Wednesday', '08:00', '17:00'),
        ('Saturday', '08:00', '12:00'),
        ('Sunday', '08:00', '12:00'),
    ]),
    
    # Multiple days separated by different days and overnight
    ("Mon - Wed 08:00 - 17:00 / Thur, Sat 20:00 - 02:00", [
        ('Monday', '08:00', '17:00'),
        ('Tuesday', '08:00', '17:00'),
        ('Wednesday', '08:00', '17:00'),
        ('Thursday', '20:00', '24:00'),
        ('Friday', '00:00', '02:00'),
        ('Saturday', '20:00', '24:00'),
        ('Sunday', '00:00', '02:00'),
    ]),

    # Fail
    ("Invalid Data", [])
])
def test_parse_opening_hours(input_hours, expected_output):
    result = parse_opening_hours(input_hours)
    
    try:
        assert result == expected_output
    except AssertionError:
        print("\n❌ 測試失敗！")
        print(f"🔹 測試輸入: {input_hours}")
        print(f"🔹 預期輸出: {expected_output}")
        print(f"🔹 實際輸出: {result}")
        raise  # AssertionError

if __name__ == "__main__":
    pytest.main()
