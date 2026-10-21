# Class Timetable Manager

A Python console application for managing academic timetables for multiple sections. It allows you to assign, edit, view, and export timetable entries while automatically checking for scheduling clashes.

## Features

- Manage timetable records for sections A, B, and C
- Work with weekdays from Monday to Friday
- Support periods 1 through 7
- Assign subjects, faculty members, and rooms to timetable slots
- Prevent duplicate entries and scheduling conflicts
- Display the weekly timetable for a selected section
- View free periods for a faculty member
- Count total weekly subject hours per section
- Change or clear existing slots
- Generate workload summaries by faculty
- Export a section timetable to a text file
- Save/load timetable data from `timetable.txt`

## Project Purpose

This project is designed to help academic departments organize class schedules efficiently. It keeps timetable information consistent and prevents common issues such as:

- Two classes assigned to the same section, same day, and same period
- A faculty member being assigned to two classes at the same time
- A room being double-booked for the same time slot

## How to Run

1. Open a terminal in the project folder.
2. Run:

```bash
python main.py
```

## Main Menu Options

The application provides the following menu:

1. Assign a slot
2. Display section timetable
3. Show faculty free periods
4. Count subject hours
5. Change a slot
6. Clear a slot
7. Faculty workload report
8. Export section timetable
9. Save timetable
0. Exit

## Data Format

The timetable data is stored in a pipe-separated text file named `timetable.txt`.

Example format:

```text
Section|Day|Period|Subject|Faculty|Room
A|MON|1|DBMS|Dr. Smith|LAB-101
```

## Notes

- The program validates input before accepting values.
- Invalid section/day/period values are rejected.
- Empty values and values containing `|` are not allowed.
- The timetable file is created or updated automatically when saving.

## File Structure

- `main.py` — main application logic
- `timetable.txt` — timetable data file generated/used by the program
- `README.md` — project documentation

## Example Workflow

- Add a timetable slot for a section
- View the timetable for that section
- Check faculty availability
- Update or remove a class if needed
- Export the section timetable for printing or sharing
