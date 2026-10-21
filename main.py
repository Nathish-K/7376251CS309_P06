
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


# MODULE 3: SEARCH AND CLASH DETECTION

def find_slot(timetable, section, day, period):
    for record in timetable:
        if (
            record["section"] == section
            and record["day"] == day
            and record["period"] == period
        ):
            return record
    return None


def check_clash(
    timetable, section, day, period, faculty, room,
    show_message=True
):
    for record in timetable: 
        if (
            record["day"] != day
            or record["period"] != period
            or record["section"] == section
        ):
            continue

        if record["faculty"].casefold() == faculty.casefold():
            if show_message:
                print(
                    f'Clash: {faculty} already teaches '
                    f'Section {record["section"]} on '
                    f'{day} period {period}.'
                )
            return True

        if record["room"].casefold() == room.casefold():
            if show_message:
                print(
                    f'Clash: {room} is booked by '
                    f'Section {record["section"]} on '
                    f'{day} period {period}.'
                )
            return True

    return False


# MODULE 4: ASSIGN A SLOT

def assign_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    if find_slot(timetable, section, day, period):
        print("This section already has an assignment in that slot.")
        print("Use Change Slot to replace it.")
        return

    subject = read_text("Enter subject: ").upper()
    faculty = read_text("Enter faculty name: ")
    room = read_text("Enter room: ")

    if check_clash(
        timetable, section, day, period, faculty, room
    ):
        print("Assignment rejected.")
        return

    timetable.append({
        "section": section,
        "day": day,
        "period": period,
        "subject": subject,
        "faculty": faculty,
        "room": room
    })

    save_timetable(timetable)
    print("Slot assigned successfully.")


# MODULE 5: DISPLAY SECTION TIMETABLE

def display_section_timetable(timetable):
    section = read_section()

    print(f"\nSECTION {section} TIMETABLE")
    print("-" * 105)

    print(f'{"DAY":<8}', end="")
    for period in PERIODS:
        print(f"P{period:<13}", end="")
    print()

    for day in DAYS:
        print(f"{day:<8}", end="")

        for period in PERIODS:
            record = find_slot(timetable, section, day, period)

            if record:
                cell = (
                    f'{record["subject"]} '
                    f'({record["faculty"]}, {record["room"]})'
                )
            else:
                cell = "---"

            print(f"{cell[:12]:<13}", end="")

        print()

    print("-" * 105)


# MODULE 6: FACULTY FREE PERIODS

def show_faculty_free_periods(timetable):
    faculty = read_text("Enter faculty name: ")

    faculty_entries = [
        record for record in timetable
        if record["faculty"].casefold() == faculty.casefold()
    ]

    if not faculty_entries:
        print("Faculty not found in the timetable.")
        return

    print(f"\nFREE PERIODS FOR {faculty}")

    for day in DAYS:
        occupied = [
            record["period"] for record in faculty_entries
            if record["day"] == day
        ]

        free = [
            period for period in PERIODS
            if period not in occupied
        ]

        if free:
            print(f"{day}: {', '.join(map(str, free))}")
        else:
            print(f"{day}: No free periods")


# MODULE 7: COUNT WEEKLY SUBJECT HOURS

def count_subject_hours(timetable):
    section = read_section()
    counts = {}

    for record in timetable:
        if record["section"] == section:
            subject = record["subject"].upper()
            counts[subject] = counts.get(subject, 0) + 1

    print(f"\nWEEKLY SUBJECT HOURS - SECTION {section}")
    print("-" * 40)

    if not counts:
        print("No subjects assigned.")
        return

    for subject, hours in sorted(counts.items()):
        print(f"{subject:<25} {hours} periods")

    print("-" * 40)
    print("Total periods:", sum(counts.values()))


# MODULE 8: CHANGE A SLOT

def change_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    old_record = find_slot(timetable, section, day, period)

    if old_record is None:
        print("No assignment exists in this slot.")
        return

    print(
        "Current:",
        old_record["subject"],
        "|", old_record["faculty"],
        "|", old_record["room"]
    )

    subject = read_text("Enter new subject: ").upper()
    faculty = read_text("Enter new faculty: ")
    room = read_text("Enter new room: ")

    # Temporarily remove the old entry for clash checking.
    timetable.remove(old_record)

    if check_clash(
        timetable, section, day, period, faculty, room
    ):
        timetable.append(old_record)
        print("Change rejected. Original slot restored.")
        return

    timetable.append({
        "section": section,
        "day": day,
        "period": period,
        "subject": subject,
        "faculty": faculty,
        "room": room
    })

    save_timetable(timetable)
    print("Slot changed successfully.")


# MODULE 9: CLEAR A SLOT

def clear_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    record = find_slot(timetable, section, day, period)

    if record is None:
        print("The selected slot is already empty.")
        return

    timetable.remove(record)
    save_timetable(timetable)
    print("Slot cleared successfully.")


# MODULE 10: FACULTY WORKLOAD REPORT

def faculty_workload_report(timetable):
    workload = {}

    for record in timetable:
        faculty = record["faculty"]
        workload[faculty] = workload.get(faculty, 0) + 1

    print("\nFACULTY WEEKLY WORKLOAD")
    print("-" * 40)

    if not workload:
        print("No assignments available.")
        return

    for faculty, periods in sorted(
        workload.items(), key=lambda item: item[0].casefold()
    ):
        print(f"{faculty:<25} {periods} periods")


# MODULE 11: EXPORT SECTION TIMETABLE

def export_section_timetable(timetable):
    section = read_section()
    filename = f"section_{section}_timetable.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"SECTION {section} TIMETABLE\n\n")
            file.write("DAY\t" + "\t".join(
                f"P{p}" for p in PERIODS
            ) + "\n")

            for day in DAYS:
                cells = []

                for period in PERIODS:
                    record = find_slot(
                        timetable, section, day, period
                    )

                    if record:
                        cells.append(
                            f'{record["subject"]} '
                            f'({record["faculty"]}, {record["room"]})'
                        )
                    else:
                        cells.append("---")

                file.write(day + "\t" + "\t".join(cells) + "\n")

        print("Timetable exported to", filename)

    except OSError as error:
        print("Export failed:", error)


# MODULE 12: MAIN MENU

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
