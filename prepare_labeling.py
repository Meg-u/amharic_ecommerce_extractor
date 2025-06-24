import pandas as pd
import os

# SETTINGS 
CSV_PATH = 'data/zemenexpress/messages_cleaned.csv'  
SAVE_PATH = 'labels/label_template.txt'
NUM_MESSAGES = 30  

# Load Messages 
df = pd.read_csv(CSV_PATH)

# Ensure clean_text column exists
if 'clean_text' not in df.columns:
    raise ValueError("The column 'clean_text' was not found in the CSV.")

# Take only the first N clean messages
messages = df['clean_text'].dropna().head(NUM_MESSAGES)

# Tokenize and Format into CoNLL Style ===
formatted_lines = []

for msg in messages:
    tokens = msg.split()  
    for token in tokens:
        formatted_lines.append(f"{token} O")  # Default label is 'O'
    formatted_lines.append("")  # Blank line to separate messages

#  Save to a labeling file
os.makedirs("labels", exist_ok=True)

with open(SAVE_PATH, "w", encoding="utf-8") as f:
    for line in formatted_lines:
        f.write(line + "\n")

print(f"Template saved to: {SAVE_PATH}")

