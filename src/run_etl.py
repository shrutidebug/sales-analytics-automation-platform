import subprocess
import sys
import re

print("\n==============================")
print("   SALES ETL PIPELINE START")
print("==============================")

# =========================
# STEP 1: FIND NEW FILES
# =========================

result = subprocess.run(
    [sys.executable, "src/find_input_files.py"],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.returncode != 0:
    print("File detection failed.")
    sys.exit(1)

# =========================
# STEP 2: EXTRACT NEW FILES
# =========================

new_files = re.findall(
    r"^- (.+\.xlsx)$",
    result.stdout,
    re.MULTILINE
)

if not new_files:
    print("\nNo new files found.")
    print("ETL pipeline finished.")
    sys.exit(0)

print("\nNew files detected:")
for file in new_files:
    print("-", file)

# =========================
# STEP 3: RUN ETL
# =========================

print("\nStarting database load...")

load_result = subprocess.run(
    [sys.executable, "src/load_dimensions.py", *new_files]
)

if load_result.returncode != 0:
    print("\nETL FAILED.")
    sys.exit(1)

print("\n==============================")
print("   SALES ETL PIPELINE COMPLETE")
print("==============================")