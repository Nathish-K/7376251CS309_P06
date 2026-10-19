
# P06: CLASS TIMETABLE MANAGER

# MODULE 1: CONSTANTS AND INPUT VALIDATION

SECTIONS = ["A", "B", "C"]
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
PERIODS = [1, 2, 3, 4, 5, 6, 7]
FILENAME = "timetable.txt"


def read_section():
    while True:
        section = input("Enter section (A/B/C): ").upper().strip()
        if section in SECTIONS:
            return section
        print("Invalid section. Try again.")


def read_day():
    while True:
        day = input("Enter day (MON-FRI): ").upper().strip()
        if day in DAYS:
            return day
        print("Invalid day. Try again.")


def read_period():
    while True:
        try:
            period = int(input("Enter period (1-7): "))
            if period in PERIODS:
                return period
            print("Period must be between 1 and 7.")
        except ValueError:
            print("Please enter a valid number.")


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value and "|" not in value:
            return value
        print("Value cannot be empty or contain |.")


# MODULE 2: FILE HANDLING

def load_timetable():
    timetable = []

    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split("|")

                # Skip the header and malformed rows.
                if len(fields) != 6 or fields[0] == "Section":
                    continue

                try:
                    period = int(fields[2])
                except ValueError:
                    continue

                section, day, _, subject, faculty, room = fields

                if (
                    section not in SECTIONS
                    or day not in DAYS
                    or period not in PERIODS
                    or not subject.strip()
                    or not faculty.strip()
                    or not room.strip()
                ):
                    continue

                record = {
                    "section": section,
                    "day": day,
                    "period": period,
                    "subject": subject.strip(),
                    "faculty": faculty.strip(),
                    "room": room.strip()
                }

                # Do not load duplicate slots or clashes.
                if find_slot(
                    timetable, section, day, period
                ) is not None:
                    print("Warning: Duplicate slot skipped.")
                    continue

                if check_clash(
                    timetable, section, day, period,
                    faculty, room, show_message=False
                ):
                    print("Warning: Conflicting entry skipped.")
                    continue

                timetable.append(record)

    except FileNotFoundError:
        print("No timetable file found. Starting empty.")

    return timetable


def save_timetable(timetable):
    with open(FILENAME, "w", encoding="utf-8") as file:
        file.write("Section|Day|Period|Subject|Faculty|Room\n")

        for record in sorted(
            timetable,
            key=lambda r: (
                SECTIONS.index(r["section"]),
                DAYS.index(r["day"]),
                r["period"]
            )
        ):
            line = (
                record["section"] + "|"
                + record["day"] + "|"
                + str(record["period"]) + "|"
                + record["subject"] + "|"
                + record["faculty"] + "|"
                + record["room"] + "\n"
            )
            file.write(line)







def main():
    timetable = load_timetable()
    print("Records loaded:", len(timetable))

    while True:
        print("\n===== CLASS TIMETABLE MANAGER =====")
        print("1. Assign a slot")
        print("2. Display section timetable")
        print("3. Show faculty free periods")
        print("4. Count subject hours")
        print("5. Change a slot")
        print("6. Clear a slot")
        print("7. Faculty workload report")
        print("8. Export section timetable")
        print("9. Save timetable")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                assign_slot(timetable)

            elif choice == "2":
                display_section_timetable(timetable)

            elif choice == "3":
                show_faculty_free_periods(timetable)

            elif choice == "4":
                count_subject_hours(timetable)

            elif choice == "5":
                change_slot(timetable)

            elif choice == "6":
                clear_slot(timetable)

            elif choice == "7":
                faculty_workload_report(timetable)

            elif choice == "8":
                export_section_timetable(timetable)

            elif choice == "9":
                save_timetable(timetable)
                print("Timetable saved.")

            elif choice == "0":
                save_timetable(timetable)
                print("Exiting program. Goodbye!")
                break

            else:
                print("Invalid choice. Enter a number from 0 to 9.")

        except OSError as error:
            print("File operation failed:", error)


if __name__ == "__main__":
    main()
