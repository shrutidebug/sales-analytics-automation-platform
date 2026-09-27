from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed_files.txt"

files = sorted(
    file.name
    for file in RAW_DATA.glob("*.xlsx")
)

print("\nINPUT FILE CHECK")
print("----------------")

print("Files found:", len(files))

processed_files = set()

if PROCESSED_FILE.exists():
    with open(PROCESSED_FILE, "r") as file:
        processed_files = {
            line.strip()
            for line in file
            if line.strip()
        }

new_files = [
    file
    for file in files
    if file not in processed_files
]

print("Already processed:", len(files) - len(new_files))
print("New files:", len(new_files))

print("\nNew files to process:")

for file in new_files:
    print("-", file)