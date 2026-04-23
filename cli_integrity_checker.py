import hashlib
import json 
import os
from colorama import init, Fore, Style


init()
def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

BASELINE_FILE = "baseline.json"
CURRENT_DIRECTORY = None
CURRENT_SNAPSHOT = None

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
        print(color_text("[OK] No changes detected.", Fore.GREEN))

    for file in modified:
        print(color_text(f"[MODIFIED] {file}", Fore.YELLOW))

    for file in deleted:
        print(color_text(f"[DELETED] {file}", Fore.RED))

    for file in new:
        print(color_text(f"[NEW] {file}", Fore.CYAN))

    print("\n========== SUMMARY ==========")
    print(color_text(f"Modified files : {len(modified)}", Fore.YELLOW))
    print(color_text(f"Deleted files  : {len(deleted)}", Fore.RED))
    print(color_text(f"New files      : {len(new)}", Fore.CYAN))


def check_mode(directory_path):

    global CURRENT_DIRECTORY, CURRENT_SNAPSHOT

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
    
    CURRENT_DIRECTORY = directory_path
    CURRENT_SNAPSHOT = current_snapshot

    print("[*] Comparing snapshots...")

    modified, deleted, new = compare_snapshots(
        baseline,
        current_snapshot
    )

    print_results(modified, deleted, new)


def show_help():
    print("""
========== FILE INTEGRITY CHECKER ==========

Available commands:

  check <directory>    → Check file integrity
  update               → Update baseline with current state
  help                 → Show this help menu
  exit                 → Exit the tool

===========================================
""")
    
def update_baseline():

    global CURRENT_SNAPSHOT

    if CURRENT_SNAPSHOT is None:
        print("[ERROR] Run check first.")
        return

    save_baseline(CURRENT_SNAPSHOT)
    print("[+] Baseline updated successfully.")

def main():
    show_help()

    while True:

        try:
            cmd = input(color_text("fic > ", Fore.GREEN)).strip()

            if not cmd:
                continue

            parts = cmd.split()
            command = parts[0].lower()

            # ---------------- HELP ----------------
            if command == "help":
                show_help()


            # ---------------- CHECK ----------------
            elif command == "check":
                if len(parts) < 2:
                    print("Usage: check <directory>")
                    continue
                check_mode(parts[1])

            # ---------------- UPDATE ----------------
            elif command == "update":
                update_baseline()

            # ---------------- EXIT ----------------
            elif command == "exit":
                print("Exiting...")
                break

            else:
                print("Unknown command. Type 'help'.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
    

if __name__ == "__main__":
    main()