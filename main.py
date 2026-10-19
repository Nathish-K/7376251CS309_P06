# # Module 1: Constants and Input Validation

SECTIONS = ["A", "B", "C"]
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
PERIODS = [1, 2, 3, 4, 5, 6, 7]


def main():
    timetable = load_timetable()

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
        print("9. Exit")

        choice = input("Enter choice: ").strip()

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
            print("Exiting program. Goodbye!")
            break