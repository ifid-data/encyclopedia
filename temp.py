import pandas as pd
import os

# --- CONFIGURATION ---
CSV_FILE = "v0.1-v0.2_audit.csv"

def print_state_stats():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found. Run the initializer or ingester first.")
        return

    # Load the state machine
    df = pd.read_csv(CSV_FILE)
    
    # Ensure status is string and handled consistently
    df['status'] = df['status'].fillna('unknown').astype(str).str.lower()
    
    total_entries = len(df)
    status_counts = df['status'].value_counts()

    print("\n" + "="*45)
    print(f"📊 ENCYCLOPEDIA STATE SUMMARY: {CSV_FILE}")
    print("="*45)
    print(f"{'STATUS':<15} | {'COUNT':<10} | {'PROGRESS'}")
    print("-" * 45)

    # We iterate through a specific order to make the report readable
    # Approve first (the 'Done' pile), then the 'To-Do' piles
    target_statuses = ['approve', 'flag', 'merge', 'delete']
    
    # Track which statuses exist in the file but aren't in our target list
    found_statuses = status_counts.index.tolist()

    for status in target_statuses:
        count = status_counts.get(status, 0)
        percentage = (count / total_entries) * 100
        # Simple text-based progress bar
        bar = "█" * int(percentage / 5)
        print(f"{status.upper():<15} | {count:<10} | {percentage:>5.1f}% {bar}")

    # Catch-all for any weird statuses that might have snuck in
    other_statuses = [s for s in found_statuses if s not in target_statuses]
    for s in other_statuses:
        count = status_counts[s]
        print(f"{s.upper():<15} | {count:<10} | (Non-standard status)")

    print("-" * 45)
    print(f"{'TOTAL ENTRIES':<15} | {total_entries:<10}")
    print("="*45)

    # Actionable Advice
    if status_counts.get('flag', 0) > 0 or status_counts.get('merge', 0) > 0:
        print(f"💡 You still have {status_counts.get('flag', 0) + status_counts.get('merge', 0)} items to resolve before V0.2 is clean.")
    else:
        print("🚀 Everything is either Approved or marked for Deletion. Ready for the final Cleanup!")

if __name__ == "__main__":
    print_state_stats()
