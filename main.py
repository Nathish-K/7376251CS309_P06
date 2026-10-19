# Module 1: Constants and Input Validation

SECTIONS = ["A", "B", "C"]
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
PERIODS = [1, 2, 3, 4, 5, 6, 7]


def read_section():
    while True:
        section = input("Enter section (A/B/C): ").upper().strip()

        if section in SECTIONS:
            return section
        else:
            print("Invalid section. Try again.")


def read_day():
    while True:
        day = input("Enter day (MON-FRI): ").upper().strip()

        if day in DAYS:
            return day
        else:
            print("Invalid day. Try again.")


def read_period():
    while True:
        try:
            period = int(input("Enter period (1-7): "))

            if period in PERIODS:
                return period
            else:
                print("Period must be between 1 and 7.")

        except ValueError:
            print("Please enter a valid number.")



section = read_section()
day = read_day()
period = read_period()

print("Section:", section)
print("Day:", day)
print("Period:", period)