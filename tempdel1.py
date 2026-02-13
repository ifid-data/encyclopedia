import os
import re
from collections import Counter

# --- CONFIGURATION ---
LOG_FILE = "ingredient_facets_audit.log"

def analyze_facet_complexity():
    if not os.path.exists(LOG_FILE):
        print(f"❌ Error: {LOG_FILE} not found.")
        return

    stats = {
        "Clean (No facets)": 0,
        "Complex (Requires Facets)": 0
    }
    
    # Track the most common required facets
    facet_distribution = Counter()
    
    # Tracking samples for review
    samples_clean = []
    samples_complex = []

    # Regex to handle the 4-part format: 
    # original :: standard :: facets :: reasoning
    pattern = re.compile(r"^(.*?) :: (.*?) :: (.*?) :: (.*)$", re.IGNORECASE)

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or "---" in line:
                continue
            
            match = pattern.search(line)
            if match:
                original = match.group(1).strip()
                facets = match.group(3).strip()
                
                # Check for "no specific facets" or empty tags
                is_clean = any(phrase in facets.lower() for phrase in [
                    "no specific facets", "none", "n/a", "no facets required"
                ]) or facets == ""

                if is_clean:
                    stats["Clean (No facets)"] += 1
                    if len(samples_clean) < 5:
                        samples_clean.append(original)
                else:
                    stats["Complex (Requires Facets)"] += 1
                    # Extract individual #tags if present
                    tags = re.findall(r"#[\w-]+(?::[\w-]+)?", facets)
                    for tag in tags:
                        facet_distribution[tag] += 1
                    
                    if len(samples_complex) < 5:
                        samples_complex.append(f"{original} -> {facets}")

    total = sum(stats.values())
    
    print("\n" + "="*60)
    print(f"📊 INGREDIENT FACET COMPLEXITY REPORT")
    print("="*60)
    
    if total == 0:
        print("No valid entries found. Check your log format.")
        return

    for category, count in stats.items():
        pct = (count / total) * 100
        print(f"{category:<30} | {count:>4} ({pct:>5.1f}%)")

    print("-" * 60)
    
    print("\n🏷️  MOST COMMON REQUIRED FACETS:")
    for tag, count in facet_distribution.most_common(10):
        print(f"  {tag:<30} : {count}")

    print("-" * 60)
    print("\n✨ SAMPLE CLEAN ITEMS (Low Maintenance):")
    for s in samples_clean:
        print(f"  - {s}")

    print("\n🔍 SAMPLE COMPLEX ITEMS (Requires Specification):")
    for s in samples_complex:
        print(f"  - {s}")
    
    print("="*60)

if __name__ == "__main__":
    analyze_facet_complexity()
