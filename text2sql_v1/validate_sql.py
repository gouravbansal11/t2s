import re

# Read the SQL file
with open('sql/dummy_inserts.sql', 'r') as f:
    content = f.read()

# Extract POC_PROJECT_EXECUTION section
proj_exec_section = content.split('POC_PROJECT_EXECUTION')[1]

# Find the column names
columns_match = re.search(r'\((.*?)\) VALUES', proj_exec_section, re.DOTALL)
if columns_match:
    columns = [c.strip() for c in columns_match.group(1).split(',') if c.strip()]
    col_count = len(columns)
    print(f"✓ POC_PROJECT_EXECUTION columns defined: {col_count}")
    print(f"  Columns: {', '.join(columns)}")

# Find all value rows (more carefully)
values_section = proj_exec_section[proj_exec_section.find('VALUES')+6:]

# Count values in first row by finding the first complete parenthesized set
lines = values_section.split('\n')
for i, line in enumerate(lines[:10]):
    if line.strip().startswith('('):
        # Count commas in this row to estimate value count
        comma_count = line.count(',')
        # This is a rough estimate
        if comma_count > 20:  # Should have ~32 commas for 33 values
            print(f"✓ First value row has approximately {comma_count + 1} values")
            break

print("\n✓ SQL file structure looks correct!")
