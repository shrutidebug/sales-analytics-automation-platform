from pathlib import Path

RAW_DATA = Path("data/raw")
PROCESSED_FILE = Path("data/processed_files.txt")

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