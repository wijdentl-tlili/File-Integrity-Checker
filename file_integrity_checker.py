import hashlib
import json 
import os

BASELINE_FILE = "baseline.json"
# Function to calculate SHA-256 hash of a file 
def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

# Load baseline from JSON
def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return None
    
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)
    
# Save baseline to JSON
def save_baseline(hash_value):
    with open(BASELINE_FILE, "w") as f:
        json.dump({"baseline_hash": hash_value}, f, indent=4)

def main():
    file_path = input("Enter the path of the file to monitor: ").strip()

    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return

    # Step 1: Calculate current file hash
    current_hash = calculate_hash(file_path)
    print(f"\nCurrent File Hash:\n{current_hash}\n")

    # Step 2: Load baseline (if exists)
    baseline = load_baseline()

    if baseline is None:
        print("📌 No baseline found. Creating a new baseline...")
        save_baseline(current_hash)
        print("✔ Baseline created successfully.")
        return

    baseline_hash = baseline["baseline_hash"]

    # Step 3: Compare hashes
    if current_hash == baseline_hash:
        print("🟢 File is clean. No modifications detected.")
    else:
        print("⚠️ WARNING: File HAS BEEN MODIFIED!")
        print("Previous Hash:", baseline_hash)
        print("New Hash:     ", current_hash)

    # Step 4: Update baseline
    save_baseline(current_hash)
    print("\n🔄 Baseline updated.")

if __name__ == "__main__":
    main()