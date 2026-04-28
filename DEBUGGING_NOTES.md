# Debugging Notes – Week 3 Survey Analysis

## Issue 1: ValueError when parsing experience_years

Original code attempted to convert values using:

int(row["experience_years"])

However the dataset contains text numbers such as:

"fifteen"

This caused:

ValueError: invalid literal for int() with base 10: 'fifteen'

### Fix
Created `parse_int_flexible()` which:
- accepts numeric strings
- converts word numbers to integers
- safely handles blank values

---

## Issue 2: Satisfaction sorting bug

Initial implementation sorted rows incorrectly, producing alphabetical order instead of numeric score ranking.

### Fix
Updated sorting logic:

scored_rows.sort(key=lambda x: x[1], reverse=True)

This ensures the highest satisfaction scores appear first.

---

## Issue 3: Role normalization

Roles contained inconsistent formatting such as:

designer  
Designer  
DESIGNER

### Fix
Created `clean_role()` to normalize role values using:

.strip().upper()
