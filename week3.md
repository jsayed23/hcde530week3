Competency Claims for Week 3

**C3 — Data Cleaning and File Handling**

This submission demonstrates competency in data cleaning and file handling by loading a messy CSV dataset, identifying inconsistent values, and transforming them into a structured format that can be analyzed reliably.

The script reads from week3_survey_messy.csv using Python’s csv module and processes each row to correct formatting issues. One issue in the dataset was inconsistent representations of experience values, including numbers written as words such as "fifteen". 

By transforming inconsistent inputs into standardized outputs and ensuring the script runs without errors on the messy dataset, the submission demonstrates the ability to diagnose and correct real-world data problems.

**C2 — Code Literacy and Documentation**

This submission demonstrates code literacy and documentation through structured Python code, explanatory comments, and clear file outputs that make the workflow understandable to another reader.

Inline comments explain key steps in the data cleaning process, including the purpose of the NUMBER_WORDS dictionary and how role counts are calculated. The script also produces separate output files for cleaned data and aggregated counts, which makes the processing pipeline transparent and easy to verify.

I refactored the script to include a helper function clean_role() with a docstring describing its input and output. This isolates the logic for standardizing role values and keeps the main cleaning loop easier to read.
