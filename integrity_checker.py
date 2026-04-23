import hashlib
import json 
import os

BASELINE_FILE = "baseline.json"

# ==========================================
# HASHING FUNCTION
# ==========================================
def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================
# SCAN DIRECTORY
# ==========================================
def scan_directory(directory):
    files_data = {}

    for root, dirs, files in os.walk(directory):

        # Ignore symbolic links
        dirs[:] = [
            d for d in dirs
            if not os.path.islink(os.path.join(root, d))
        ]

        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))

            # Ignore symlinks
            if os.path.islink(file_path):
                continue

            try:
                file_hash = calculate_hash(file_path)

                if file_hash is None:
                    continue

                files_data[file_path] = {
                    "hash": file_hash,
                    "size": os.path.getsize(file_path)
                }

            except Exception as e:
                print(f"[WARNING] Cannot access {file_path}: {e}")

    return files_data


# ==========================================
# SAVE BASELINE
# ==========================================
def save_baseline(snapshot):

    with open(BASELINE_FILE, "w") as f:
        json.dump(snapshot, f, indent=4)

    print(f"[+] Baseline saved to {BASELINE_FILE}")


# ==========================================
# LOAD BASELINE
# ==========================================
def load_baseline():

    if not os.path.exists(BASELINE_FILE):
        print("[ERROR] baseline.json not found.")
        return None

    with open(BASELINE_FILE, "r") as f:
        return json.load(f)
    

# ==========================================
# COMPARE SNAPSHOTS
# ==========================================
def compare_snapshots(old_snapshot, current_snapshot):

    modified_files = []
    deleted_files = []
    new_files = []

    # Detect modified and deleted files
    for file_path in old_snapshot:

        if file_path not in current_snapshot:
            deleted_files.append(file_path)

        elif (
            old_snapshot[file_path]["hash"]
            != current_snapshot[file_path]["hash"]
        ):
            modified_files.append(file_path)

    # Detect new files
    for file_path in current_snapshot:

        if file_path not in old_snapshot:
            new_files.append(file_path)

    return modified_files, deleted_files, new_files
        

# ==========================================
# PRINT RESULTS
# ==========================================
def print_results(modified, deleted, new):

    print("\n========== RESULTS ==========\n")

    if not modified and not deleted and not new:
        print("[OK] No changes detected.")

    for file in modified:
        print(f"[MODIFIED] {file}")

    for file in deleted:
        print(f"[DELETED] {file}")

    for file in new:
        print(f"[NEW] {file}")

    print("\n========== SUMMARY ==========")
    print(f"Modified files : {len(modified)}")
    print(f"Deleted files  : {len(deleted)}")
    print(f"New files      : {len(new)}")


def main():
    directory_path = input("Enter the path of the directory to monitor: ").strip()

    if not os.path.exists(directory_path):
        print("Directory does not exist.")
        return

    print("[*] Scanning current files...")

    current_snapshot = scan_directory(directory_path)

    print("[*] Loading baseline...")

    baseline = load_baseline()

    if baseline is None:
        print("📌 No baseline found. Creating a new baseline...")
        save_baseline(current_snapshot)
        print("✔ Baseline created successfully.")
        print(f"[+] {len(current_snapshot)} files indexed.")
        return

    print("[*] Comparing snapshots...")

    modified, deleted, new = compare_snapshots(
        baseline,
        current_snapshot
    )

    print_results(modified, deleted, new)

if __name__ == "__main__":
    main()