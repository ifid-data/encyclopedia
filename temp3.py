import time
import os
import pandas as pd
from tqdm import tqdm
from google import genai
from google.genai import types
from api_key import api_key

# --- CONFIGURATION ---
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-2.0-flash"
CSV_FILE = "v0.1-v0.2_audit.csv"
FACET_LOG = "ingredient_facets_audit.log"
BATCH_SIZE = 25

SYSTEM_INSTRUCTION = """
<instruction_set name="FSSAI_PMEST_Facet_Extractor">
  <context>
    You are a food labeling consultant specializing in FSSAI and PMEST (Personality, Matter, Energy, Space, Time) classification. 
    Your goal is to standardize ingredient slugs and identify mandatory facets required for legal compliance.
  </context>

  <logic>
    1. Standard Slug: Strip "Functional Titles" (e.g., Acidity Regulator, Emulsifier) from the name to find the literal substance (Matter). 
       Example: "anti-foaming-agent-ins-900a" -> "dimethylpolysiloxane".
    2. Facets/Tags: Identify what must be declared by law:
       - #source: (e.g., for oils, lecithin, or gelatin)
       - #functional-class: (e.g., preservative, stabilizer)
       - #strain: (for probiotics/cultures)
       - #ins-number: (for additives)
       - #process: (e.g., roasted, cold-pressed, hydrolyzed)
  </logic>

  <output_protocol>
    Format: original-slug :: recommended-standard-slug :: facets/tags :: reasoning
    Strictly raw text. No markdown.
    Example: 
    anti-foaming-agent-ins-900a :: dimethylpolysiloxane :: #ins-900a, #functional-class:anti-foaming-agent :: FSSAI requires the specific name and functional class for additives.
    soy-lecithin :: lecithin :: #source:soy, #functional-class:emulsifier :: Source must be declared for allergen and identity.
  </output_protocol>
</instruction_set>
"""

def get_target_slugs():
    if not os.path.exists(CSV_FILE):
        return []
    df = pd.read_csv(CSV_FILE)
    # Auditing the same 621 items previously targeted
    targets = df[df['status'].str.lower().isin(['approve', 'flag'])]['canon-slug'].tolist()
    return targets

def call_gemini_facets(batch):
    wait_time = 5
    prompt = f"Extract facets and standardize these slugs:\n{', '.join(batch)}"
    
    for attempt in range(6):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0
                )
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                time.sleep(wait_time)
                wait_time *= 2
            else:
                time.sleep(wait_time)
    return ""

def run_facet_audit():
    slugs = get_target_slugs()
    if not slugs:
        return

    print(f"🚀 Extracting Facets for {len(slugs)} items...")
    
    with open(FACET_LOG, "w", encoding="utf-8") as f:
        f.write("--- INGREDIENT FACET AUDIT START ---\n")

    for i in tqdm(range(0, len(slugs), BATCH_SIZE), desc="Analyzing Facets"):
        batch = slugs[i : i + BATCH_SIZE]
        result = call_gemini_facets(batch)
        
        if result:
            with open(FACET_LOG, "a", encoding="utf-8") as f:
                f.write(result.strip() + "\n")
        
        time.sleep(1) # Flash 2.0 is fast, but let's keep it stable

    print(f"\n✨ Facet audit complete. Results saved to {FACET_LOG}")

if __name__ == "__main__":
    run_facet_audit()
