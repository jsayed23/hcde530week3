Competency Claims for Week 3

**C3 — Data Cleaning and File Handling**

This submission demonstrates competency in data cleaning and file handling by loading a messy CSV dataset, identifying inconsistent values, and transforming them into a structured format that can be analyzed reliably.

The script reads from week3_survey_messy.csv using Python’s csv module and processes each row to correct formatting issues. One issue in the dataset was inconsistent representations of experience values, including numbers written as words such as "two" or "three". To address this, I created a dictionary (NUMBER_WORDS) that converts written numbers into numeric values before processing them.

The script also standardizes role names and aggregates them using collections.Counter to produce a frequency table. After cleaning the data, the script generates two consistent output files:

week3_survey_cleaned.csv, which contains the cleaned dataset
week3_role_counts.csv, which summarizes the number of responses per role

By transforming inconsistent inputs into standardized outputs and ensuring the script runs without errors on the messy dataset, the submission demonstrates the ability to diagnose and correct real-world data problems.

**C2 — Code Literacy and Documentation**

This submission demonstrates code literacy and documentation through structured Python code, explanatory comments, and clear file outputs that make the workflow understandable to another reader.

The script uses several Python modules, including csv, pathlib, and collections.Counter, to read input data, process rows, and produce summarized outputs. File paths are handled using Path(__file__).resolve().parent, which ensures the script can locate the input file and write outputs relative to the project directory rather than relying on hardcoded paths.

Inline comments explain key steps in the data cleaning process, including the purpose of the NUMBER_WORDS dictionary and how role counts are calculated. The script also produces separate output files for cleaned data and aggregated counts, which makes the processing pipeline transparent and easy to verify.
