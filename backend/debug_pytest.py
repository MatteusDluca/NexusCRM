import sys

with open('pytest_out.txt', 'r', encoding='utf-16le', errors='ignore') as f:
    lines = f.readlines()
    
# Extract failures section
in_failures = False
for line in lines:
    if "====== FAILURES ======" in line:
        in_failures = True
    if "====== short test summary info ======" in line:
        break
    if in_failures:
        print(line, end="")
