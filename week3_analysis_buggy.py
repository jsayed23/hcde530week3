import csv
from collections import Counter
from pathlib import Path
import sys


# Get the directory where this script is located
# This lets the script reliably find input/output files in the same folder
BASE_DIR = Path(__file__).resolve().parent

# File paths for input and output CSV files
INPUT_FILE = BASE_DIR / "week3_survey_messy.csv"
CLEANED_FILE = BASE_DIR / "week3_survey_cleaned.csv"
ROLE_COUNTS_FILE = BASE_DIR / "week3_role_counts.csv"

# Dictionary that maps written numbers (e.g., "five") to integers
# This helps clean messy survey data where users typed numbers as words
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


# Convert numeric values stored as text into integers
# Handles values like "5", "five", or "twenty"
# Returns None if the value cannot be converted
def parse_int_flexible(raw_value: str) -> int | None:
    value = (raw_value or "").strip()
    if not value:
        return None

    # If the value is already numeric (e.g., "5")
    if value.isdigit():
        return int(value)

    # Normalize text values like "five" or "twenty-one"
    normalized = value.lower().replace("-", " ")
    if normalized in NUMBER_WORDS:
        return NUMBER_WORDS[normalized]

    # Return None if the value cannot be converted
    return None


# Load the CSV file and perform basic cleaning
def load_and_clean_rows(input_file: str) -> tuple[list[dict], list[str]]:
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # Ensure the CSV has a header row
        if not fieldnames:
            raise ValueError("Input CSV has no header row.")

        # Verify that required columns exist in the dataset
        required = {
            "response_id",
            "participant_name",
            "role",
            "experience_years",
            "satisfaction_score",
        }

        missing = sorted(required - set(fieldnames))
        if missing:
            raise ValueError(
                f"Input CSV is missing required columns: {', '.join(missing)}"
            )

        cleaned_rows = []

        # Loop through each row in the CSV and clean the values
        for row in reader:
            # Remove extra spaces from participant name
            name_value = (row.get("participant_name") or "").strip()

            # Skip rows with no participant name
            if not name_value:
                continue

            # Standardize the participant name
            row["participant_name"] = name_value

            # Standardize role values by trimming spaces and converting to uppercase
            row["role"] = (row.get("role") or "").strip().upper()

            # Add cleaned row to the list
            cleaned_rows.append(row)

        return cleaned_rows, fieldnames


# Write the cleaned survey data into a new CSV file
def write_cleaned_rows(rows: list[dict], fieldnames: list[str], output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)

        # Write the column headers
        writer.writeheader()

        # Write each cleaned row to the output file
        writer.writerows(rows)


# Count how many responses belong to each role
def count_roles(rows: list[dict]) -> Counter:
    counts = Counter()

    # Loop through rows and increment count for each role
    for row in rows:
        role = (row.get("role") or "").strip()
        if role:
            counts[role] += 1

    return counts


# Save role counts to a CSV file for analysis
def write_role_counts(counts: Counter, output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)

        # Write column headers
        writer.writerow(["role", "count"])

        # Write each role and its count
        for role, count in sorted(counts.items()):
            writer.writerow([role, count])


# Print role counts to the terminal
def print_role_counts(counts: Counter) -> None:
    print("Responses by role:")
    for role, count in sorted(counts.items()):
        print(f"  {role}: {count}")


# Calculate and print the average years of experience
def print_average_experience(rows: list[dict]) -> None:
    numeric_values = []
    invalid_rows = []

    # Convert experience values into numbers when possible
    for row in rows:
        value = row.get("experience_years") or ""
        parsed = parse_int_flexible(value)

        if parsed is not None:
            numeric_values.append(parsed)
        elif value.strip():
            # Track rows that contain invalid experience values
            invalid_rows.append((row.get("response_id", "UNKNOWN"), value.strip()))

    # Compute the average if valid values exist
    if numeric_values:
        avg_experience = sum(numeric_values) / len(numeric_values)
        print(f"\nAverage years of experience: {avg_experience:.1f}")
    else:
        print("\nAverage years of experience: N/A (no valid numeric values)")

    # Show which rows had invalid data
    if invalid_rows:
        print("\nInvalid experience_years values (ignored):")
        for response_id, value in invalid_rows:
            print(f"  {response_id}: {value}")


# Identify the top 5 highest satisfaction scores
def print_top_5_satisfaction(rows: list[dict]) -> None:
    scored_rows = []
    invalid_rows = []

    # Parse satisfaction scores into numeric values
    for row in rows:
        score_value = row.get("satisfaction_score") or ""
        parsed = parse_int_flexible(score_value)

        if parsed is not None:
            scored_rows.append((row["participant_name"], parsed))
        elif score_value.strip():
            invalid_rows.append((row.get("response_id", "UNKNOWN"), score_value.strip()))

    # Sort scores from highest to lowest
    scored_rows.sort(key=lambda x: x[1], reverse=True)

    # Select the top 5 scores
    top5 = scored_rows[:5]

    print("\nTop 5 satisfaction scores:")
    for name, score in top5:
        print(f"  {name}: {score}")

    # Show rows with invalid satisfaction values
    if invalid_rows:
        print("\nInvalid satisfaction_score values (ignored):")
        for response_id, value in invalid_rows:
            print(f"  {response_id}: {value}")


# Main function that runs the full data cleaning pipeline
def main() -> None:
    try:
        # Load and clean the messy survey data
        rows, fieldnames = load_and_clean_rows(INPUT_FILE)

        # Write cleaned dataset to a new CSV
        write_cleaned_rows(rows, fieldnames, CLEANED_FILE)

        # Count responses by role
        role_counts = count_roles(rows)

        # Print role counts to console
        print_role_counts(role_counts)

        # Save role counts to a CSV file
        write_role_counts(role_counts, ROLE_COUNTS_FILE)

        # Compute statistics from cleaned data
        print_average_experience(rows)
        print_top_5_satisfaction(rows)

        print(f"\nCleaned data written to {CLEANED_FILE}")
        print(f"Role counts written to {ROLE_COUNTS_FILE}")

    # Error handling if the input file is missing
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        print("Make sure week3_survey_messy.csv is in the same folder as this script.")
        sys.exit(1)

    # Error handling for missing columns or invalid structure
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    # Error handling for CSV parsing problems
    except csv.Error as exc:
        print(f"ERROR: CSV parsing failed: {exc}")
        sys.exit(1)


# Run the program only when the script is executed directly
if __name__ == "__main__":
    main()
