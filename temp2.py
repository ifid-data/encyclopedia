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
LOG_FILE = "fssai_audit_results.log"
BATCH_SIZE = 50

# The XML Instruction Set you provided
SYSTEM_INSTRUCTION = """
<instruction_set name="FSSAI_Ingredient_Classifier">
  <context>
    You are a technical auditor for Indian FMCG labels. Your task is to filter ingredient lists into three distinct legal/biological statuses to determine if an item is a "Literal Ingredient" or "Labeling Fluff."
  </context>

  <logic_framework>
    Evaluate each input against the following definitions:

    1. [APPROVE]: A standalone, literal ingredient. 
       - Biological/Agricultural products (e.g., Mango, Wheat Flour, Turmeric).
       - Specific chemicals/additives when listed by their precise legal name (e.g., Sodium Bicarbonate, Citric Acid).
       - Rule: If you can buy it as a single raw material without further processing, it is APPROVE.

    2. [DELETE]: A functional descriptor or class title.
       - These describe what the ingredient DOES, not what it IS.
       - Examples: Shortening, Acidity Regulator, Flour Treatment Agent, Humectant, Antioxidant, Raising Agent.
       - Rule: If the word describes a 'job title' that requires a sub-ingredient in brackets to be legally complete, it is DELETE.

    3. [FLAG]: High-risk ambiguous terms or composite blends.
       - Use this for "Seasoning," "Masala," "Flavoring," or "Vegetable Fat" without source.
       - Use this when an ingredient name is technically a "Marketing Name" (e.g., "Health Blend").
       - Rule: If a human researcher must check the sub-recipe or specific source oil to confirm its legal identity, it is FLAG.
  </logic_framework>

  <output_protocol>
    Output must be strictly raw text with no Markdown formatting (no bold, no headers, no bullet points).
    Format: canon-slug :: status :: one liner explanation
  </output_protocol>
</instruction_set>
"""

def get_target_slugs():
    if not os.path.exists(CSV_FILE):
        return []
    df = pd.read_csv(CSV_FILE)
    # Only send items currently marked as 'approve' or 'flag'
    # This ignores 'delete' and 'merge' entries entirely.
    targets = df[df['status'].str.lower().isin(['approve', 'flag'])]['canon-slug'].tolist()
    return targets

def call_gemini_with_backoff(batch):
    wait_time = 5
    prompt = f"Audit these ingredients:\n{', '.join(batch)}"
    
    for attempt in range(6): # Exponential backoff up to 6 retries
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
                print(f"\n⚠️ Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                print(f"\n❌ API Error: {e}")
                time.sleep(wait_time)
    return ""

def run_fssai_audit():
    slugs = get_target_slugs()
    if not slugs:
        print("✅ No target ingredients (Approve/Flag) found to process.")
        return

    print(f"🚀 Starting audit of {len(slugs)} items using Gemini 2.0 Flash...")
    
    # Initialize Log File
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("--- FSSAI AUDIT SESSION START ---\n")

    # Use tqdm for a clean progress bar
    for i in tqdm(range(0, len(slugs), BATCH_SIZE), desc="Auditing Batches"):
        batch = slugs[i : i + BATCH_SIZE]
        result = call_gemini_with_backoff(batch)
        
        if result:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(result + "\n")
        
        # Respectful gap between batches to prevent immediate 429s
        time.sleep(2)

    print(f"\n✨ Audit complete. Results saved to {LOG_FILE}")

if __name__ == "__main__":
    run_fssai_audit()
