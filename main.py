# CLASS TIMETABLE MANAGER

SECTIONS = ["A", "B", "C"]
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
PERIODS = [1, 2, 3, 4, 5, 6, 7]
FILENAME = "timetable.txt"


# 1. GET VALID INPUT

def read_section():
    while True:
        section = input("Enter section (A/B/C): ").strip().upper()
        if section in SECTIONS:
            return section
        print("Invalid section. Try again.")


def read_day():
    while True:
        day = input("Enter day (MON-FRI): ").strip().upper()
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
            print("Please enter a number.")


def read_text(message):
    while True:
        value = input(message).strip()
        if value != "" and "|" not in value:
            return value
        print("Value cannot be empty or contain |.")


# 2. FIND A TIMETABLE SLOT

def find_slot(timetable, section, day, period):
    for record in timetable:
        if (record["section"] == section
                and record["day"] == day
                and record["period"] == period):
            return record
    return None


# 3. CHECK FACULTY AND ROOM CLASHES

def check_clash(timetable, section, day, period, faculty, room,
                show_message=True):
    for record in timetable:
        if record["day"] != day or record["period"] != period:
            continue
        if record["section"] == section:
            continue

        if record["faculty"].lower() == faculty.lower():
            if show_message:
                print(f"Clash: {faculty} is already teaching "
                      f"Section {record['section']} at {day}, period {period}.")
            return True

        if record["room"].lower() == room.lower():
            if show_message:
                print(f"Clash: room {room} is already booked "
                      f"by Section {record['section']} at {day}, period {period}.")
            return True

    return False


def load_timetable():
    timetable = []

    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.strip().split("|")

                # Each valid row must contain six values.
                if len(fields) != 6 or fields[0] == "Section":
                    continue

                section = fields[0]
                day = fields[1]
                subject = fields[3].strip()
                faculty = fields[4].strip()
                room = fields[5].strip()

                try:
                    period = int(fields[2])
                except ValueError:
                    continue

                if section not in SECTIONS or day not in DAYS:
                    continue
                if period not in PERIODS:
                    continue
                if subject == "" or faculty == "" or room == "":
                    continue

                # Do not load a slot that is already occupied.
                if find_slot(timetable, section, day, period) is not None:
                    print("Warning: duplicate slot skipped.")
                    continue

                # Do not load entries with faculty or room clashes.
                if check_clash(timetable, section, day, period,
                               faculty, room, False):
                    print("Warning: conflicting entry skipped.")
                    continue

                record = {
                    "section": section,
                    "day": day,
                    "period": period,
                    "subject": subject,
                    "faculty": faculty,
                    "room": room
                }
                timetable.append(record)

    except FileNotFoundError:
        print("No timetable file found. Starting with an empty timetable.")

    return timetable


def save_timetable(timetable):
    # Save records in section, day, and period order.
    sorted_timetable = []

    for section in SECTIONS:
        for day in DAYS:
            for period in PERIODS:
                record = find_slot(timetable, section, day, period)
                if record is not None:
                    sorted_timetable.append(record)

    with open(FILENAME, "w", encoding="utf-8") as file:
        file.write("Section|Day|Period|Subject|Faculty|Room\n")

        for record in sorted_timetable:
            line = (
                record["section"] + "|"
                + record["day"] + "|"
                + str(record["period"]) + "|"
                + record["subject"] + "|"
                + record["faculty"] + "|"
                + record["room"] + "\n"
            )
            file.write(line)


# 5. ASSIGN A NEW SLOT

def assign_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    if find_slot(timetable, section, day, period) is not None:
        print("This section already has a class in that slot.")
        print("Use Change a slot to replace it.")
        return

    subject = read_text("Enter subject: ").upper()
    faculty = read_text("Enter faculty name: ")
    room = read_text("Enter room: ")

    if check_clash(timetable, section, day, period, faculty, room):
        print("Assignment rejected.")
        return

    record = {
        "section": section,
        "day": day,
        "period": period,
        "subject": subject,
        "faculty": faculty,
        "room": room
    }
    timetable.append(record)
    save_timetable(timetable)
    print("Slot assigned successfully.")


# 6. DISPLAY A SECTION'S TIMETABLE

def display_section_timetable(timetable):
    section = read_section()

    print(f"\nTIMETABLE FOR SECTION {section}")
    print("-" * 105)

    print(f"{'DAY':<8}", end="")
    for period in PERIODS:
        print(f"{('P' + str(period)):<13}", end="")
    print()

    for day in DAYS:
        print(f"{day:<8}", end="")

        for period in PERIODS:
            record = find_slot(timetable, section, day, period)

            if record is None:
                cell = "---"
            else:
                cell = record["subject"] + " (" + record["room"] + ")"

            print(f"{cell[:12]:<13}", end="")
        print()

    print("-" * 105)
    print("Note: each timetable cell shows the subject and room.")


# 7. SHOW A FACULTY MEMBER'S FREE PERIODS

def show_faculty_free_periods(timetable):
    faculty = read_text("Enter faculty name: ")
    found = False

    for record in timetable:
        if record["faculty"].lower() == faculty.lower():
            found = True
            break

    if not found:
        print("Faculty not found in the timetable.")
        return

    print(f"\nFREE PERIODS FOR {faculty}")

    for day in DAYS:
        occupied_periods = []

        for record in timetable:
            if (record["faculty"].lower() == faculty.lower()
                    and record["day"] == day):
                occupied_periods.append(record["period"])

        free_periods = []
        for period in PERIODS:
            if period not in occupied_periods:
                free_periods.append(str(period))

        if len(free_periods) > 0:
            print(day + ": " + ", ".join(free_periods))
        else:
            print(day + ": No free periods")


# 8. COUNT WEEKLY SUBJECT PERIODS

def count_subject_hours(timetable):
    section = read_section()
    subject_counts = {}

    for record in timetable:
        if record["section"] == section:
            subject = record["subject"].upper()

            if subject not in subject_counts:
                subject_counts[subject] = 0
            subject_counts[subject] += 1

    print(f"\nWEEKLY SUBJECT HOURS - SECTION {section}")
    print("-" * 40)

    if len(subject_counts) == 0:
        print("No subjects assigned.")
        return

    total = 0
    for subject in sorted(subject_counts):
        hours = subject_counts[subject]
        print(f"{subject:<25} {hours} periods")
        total += hours

    print("-" * 40)
    print("Total periods:", total)


# 9. CHANGE AN EXISTING SLOT

def change_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    old_record = find_slot(timetable, section, day, period)

    if old_record is None:
        print("No class is assigned to this slot.")
        return

    print("Current class:", old_record["subject"],
          "|", old_record["faculty"], "|", old_record["room"])

    subject = read_text("Enter new subject: ").upper()
    faculty = read_text("Enter new faculty name: ")
    room = read_text("Enter new room: ")

    # Remove the old class temporarily while checking clashes.
    timetable.remove(old_record)

    if check_clash(timetable, section, day, period, faculty, room):
        timetable.append(old_record)
        print("Change rejected. The original class has been restored.")
        return

    new_record = {
        "section": section,
        "day": day,
        "period": period,
        "subject": subject,
        "faculty": faculty,
        "room": room
    }
    timetable.append(new_record)
    save_timetable(timetable)
    print("Slot changed successfully.")


# 10. CLEAR A SLOT

def clear_slot(timetable):
    section = read_section()
    day = read_day()
    period = read_period()

    record = find_slot(timetable, section, day, period)

    if record is None:
        print("This slot is already empty.")
        return

    timetable.remove(record)
    save_timetable(timetable)
    print("Slot cleared successfully.")


# 11. SHOW FACULTY WORKLOAD

def faculty_workload_report(timetable):
    workload = {}

    for record in timetable:
        faculty = record["faculty"]

        if faculty not in workload:
            workload[faculty] = 0
        workload[faculty] += 1

    print("\nFACULTY WEEKLY WORKLOAD")
    print("-" * 40)

    if len(workload) == 0:
        print("No assignments available.")
        return

    for faculty in sorted(workload, key=str.lower):
        print(f"{faculty:<25} {workload[faculty]} periods")


# 12. EXPORT A SECTION'S TIMETABLE

def export_section_timetable(timetable):
    section = read_section()
    filename = "section_" + section + "_timetable.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"TIMETABLE FOR SECTION {section}\n\n")
            file.write("DAY\t" + "\t".join(
                ["P" + str(period) for period in PERIODS]
            ) + "\n")

            for day in DAYS:
                cells = []

                for period in PERIODS:
                    record = find_slot(timetable, section, day, period)

                    if record is None:
                        cells.append("---")
                    else:
                        cell = (record["subject"] + " ("
                                + record["faculty"] + ", "
                                + record["room"] + ")")
                        cells.append(cell)

                file.write(day + "\t" + "\t".join(cells) + "\n")

        print("Timetable exported to", filename)

    except OSError as error:
        print("Export failed:", error)


# 13. MAIN MENU

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
2
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
