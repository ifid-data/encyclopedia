import os
import pandas as pd
import difflib

# --- CONFIGURATION ---
BASE_PATH = os.path.expanduser("~/encyclopedia/data/md")
DB_FILE = "v0.1-v0.2_audit.csv"

def get_all_canons():
    canons = []
    if not os.path.exists(BASE_PATH):
        print(f"❌ Error: Path not found: {BASE_PATH}")
        return []
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".md"):
                canons.append(file)
    return sorted(list(set(canons)))

def init_or_load_db():
    canons = get_all_canons()
    if not os.path.exists(DB_FILE):
        print(f"✨ Initializing audit table with {len(canons)} entries...")
        df = pd.DataFrame({'canon-slug': canons, 'status': 'approve', 'note': 'NONE'})
        df.to_csv(DB_FILE, index=False)
        return df
    df = pd.read_csv(DB_FILE)
    existing = set(df['canon-slug'].tolist())
    new_files = [f for f in canons if f not in existing]
    if new_files:
        print(f"Syncing: {len(new_files)} new files found.")
        new_df = pd.DataFrame({'canon-slug': new_files, 'status': 'approve', 'note': 'NONE'})
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
    return df

def main():
    df = init_or_load_db()
    if df.empty: return

    print("\n--- Bulk Encyclopedia Auditor ---")
    print("Tip: Enter ingredients separated by commas (e.g., fat, flour, fiber)")
    
    while True:
        raw_input = input("\nEnter ingredient(s) (or 'q' to quit): ").strip()
        if raw_input.lower() == 'q': break
        if not raw_input: continue

        queries = [q.strip() for q in raw_input.split(',') if q.strip()]
        selected_targets = []

        # 1. Selection Phase for each query
        for q in queries:
            all_slugs = df['canon-slug'].tolist()
            matches = difflib.get_close_matches(q, all_slugs, n=5, cutoff=0.2)

            if not matches:
                print(f"❌ No matches for '{q}'")
                continue

            print(f"\nResults for '{q}':")
            for i, m in enumerate(matches):
                curr = df.loc[df['canon-slug'] == m].iloc[0]
                print(f"[{i}] {m:<30} | {curr['status']} | {curr['note']}")
            
            choice = input(f"Select index for '{q}' (or 's' to skip): ")
            if choice.isdigit() and int(choice) < len(matches):
                selected_targets.append(matches[int(choice)])

        if not selected_targets:
            print("No items selected for update.")
            continue

        # 2. Bulk Action Phase
        print(f"\nSelected items: {selected_targets}")
        print("Apply to all: [a] Approve, [f] Flag, [m] Merge, [d] Delete")
        action = input("Choose action: ").lower()

        status, note = "approve", "NONE"

        if action == 'f':
            status, note = "flag", input("Reason for flag: ")
        elif action == 'd':
            status, note = "delete", input("Reason for delete: ")
        elif action == 'm':
            status = "merge"
            target = input("Merge all into (slug name): ")
            note = f"MERGE INTO {target}"
        elif action == 'a':
            status, note = "approve", "NONE"
        else:
            print("Skipping bulk update.")
            continue

        # 3. Batch Update
        for slug in selected_targets:
            df.loc[df['canon-slug'] == slug, 'status'] = status
            df.loc[df['canon-slug'] == slug, 'note'] = note
        
        df.to_csv(DB_FILE, index=False)
        print(f"✅ Batch updated {len(selected_targets)} items to {status.upper()}.")

if __name__ == "__main__":
    main()
