import csv
from collections import Counter
from pathlib import Path
import sys


# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# File paths
INPUT_FILE = BASE_DIR / "week3_survey_messy.csv"
CLEANED_FILE = BASE_DIR / "week3_survey_cleaned.csv"
ROLE_COUNTS_FILE = BASE_DIR / "week3_role_counts.csv"

# Dictionary for converting word numbers to integers
NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}


# Convert numeric text to integer
def parse_int_flexible(raw_value: str) -> int | None:
    value = (raw_value or "").strip()
    if not value:
        return None

    if value.isdigit():
        return int(value)

    normalized = value.lower().replace("-", " ")
    if normalized in NUMBER_WORDS:
        return NUMBER_WORDS[normalized]

    return None


# Clean role values (NEW FUNCTION)
def clean_role(raw_role: str) -> str:
    """
    Standardize a participant role value.

    Parameters:
        raw_role (str): Original role value from CSV.

    Returns:
        str: Cleaned role (trimmed and uppercase).
    """
    return (raw_role or "").strip().upper()


# NEW FUNCTION: dataset summary
def summarize_data(rows: list[dict]) -> dict:
    """
    Create a plain-language summary of the cleaned dataset.

    Includes:
    - total row count
    - unique roles
    - number of empty name fields

    Parameters:
        rows (list[dict]): Cleaned survey data

    Returns:
        dict: Summary statistics
    """

    row_count = len(rows)
    unique_roles = set()
    empty_name_count = 0

    for row in rows:
        role = (row.get("role") or "").strip()
        if role:
            unique_roles.add(role)

        name = (row.get("participant_name") or "").strip()
        if not name:
            empty_name_count += 1

    return {
        "row_count": row_count,
        "unique_roles": sorted(unique_roles),
        "empty_name_count": empty_name_count,
    }


# Load + clean dataset
def load_and_clean_rows(input_file: str) -> tuple[list[dict], list[str]]:
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        if not fieldnames:
            raise ValueError("Input CSV has no header row.")

        required = {
            "response_id",
            "participant_name",
            "role",
            "experience_years",
            "satisfaction_score",
        }

        missing = sorted(required - set(fieldnames))
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        cleaned_rows = []

        for row in reader:
            name_value = (row.get("participant_name") or "").strip()

            if not name_value:
                continue

            row["participant_name"] = name_value
            row["role"] = clean_role(row.get("role"))

            cleaned_rows.append(row)

        return cleaned_rows, fieldnames


# Write cleaned CSV
def write_cleaned_rows(rows: list[dict], fieldnames: list[str], output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# Count roles
def count_roles(rows: list[dict]) -> Counter:
    counts = Counter()

    for row in rows:
        role = (row.get("role") or "").strip()
        if role:
            counts[role] += 1

    return counts


# Save role counts
def write_role_counts(counts: Counter, output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["role", "count"])

        for role, count in sorted(counts.items()):
            writer.writerow([role, count])


# Print role counts
def print_role_counts(counts: Counter) -> None:
    print("Responses by role:")
    for role, count in sorted(counts.items()):
        print(f"  {role}: {count}")


# Average experience
def print_average_experience(rows: list[dict]) -> None:
    numeric_values = []
    invalid_rows = []

    for row in rows:
        value = row.get("experience_years") or ""
        parsed = parse_int_flexible(value)

        if parsed is not None:
            numeric_values.append(parsed)
        elif value.strip():
            invalid_rows.append((row.get("response_id", "UNKNOWN"), value.strip()))

    if numeric_values:
        avg = sum(numeric_values) / len(numeric_values)
        print(f"\nAverage years of experience: {avg:.1f}")
    else:
        print("\nAverage years of experience: N/A")

    if invalid_rows:
        print("\nInvalid experience values:")
        for rid, val in invalid_rows:
            print(f"  {rid}: {val}")


# Top satisfaction
def print_top_5_satisfaction(rows: list[dict]) -> None:
    scored_rows = []
    invalid_rows = []

    for row in rows:
        value = row.get("satisfaction_score") or ""
        parsed = parse_int_flexible(value)

        if parsed is not None:
            scored_rows.append((row["participant_name"], parsed))
        elif value.strip():
            invalid_rows.append((row.get("response_id", "UNKNOWN"), value.strip()))

    scored_rows.sort(key=lambda x: x[1], reverse=True)

    print("\nTop 5 satisfaction scores:")
    for name, score in scored_rows[:5]:
        print(f"  {name}: {score}")

    if invalid_rows:
        print("\nInvalid satisfaction values:")
        for rid, val in invalid_rows:
            print(f"  {rid}: {val}")


# MAIN
def main() -> None:
    try:
        rows, fieldnames = load_and_clean_rows(INPUT_FILE)

        write_cleaned_rows(rows, fieldnames, CLEANED_FILE)

        role_counts = count_roles(rows)
        print_role_counts(role_counts)
        write_role_counts(role_counts, ROLE_COUNTS_FILE)

        print_average_experience(rows)
        print_top_5_satisfaction(rows)

        # NEW: dataset summary
        summary = summarize_data(rows)

        print("\nDataset Summary:")
        print(f"  Row count: {summary['row_count']}")
        print(f"  Unique roles: {', '.join(summary['unique_roles'])}")
        print(f"  Empty name fields: {summary['empty_name_count']}")

        print(f"\nCleaned data written to {CLEANED_FILE}")
        print(f"Role counts written to {ROLE_COUNTS_FILE}")

    except FileNotFoundError:
        print(f"ERROR: Missing file {INPUT_FILE}")
        sys.exit(1)

    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    except csv.Error as exc:
        print(f"ERROR: CSV issue: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
