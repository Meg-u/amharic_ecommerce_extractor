import os
import pandas as pd
import re

# Normalize common Amharic letters with variants
def normalize_amharic(text):
    text = re.sub('[ሃኃኻ]', 'ሀ', text)
    text = re.sub('[ሐሓኻ]', 'ሐ', text)
    text = re.sub('[ኸ]', 'ኀ', text)
    text = re.sub('[ዓኣዐ]', 'አ', text)
    text = re.sub('[ጸ]', 'ፀ', text)
    return text

# Remove symbols, emojis, hashtags, prices, URLs, English words, etc.
def clean_text(text):
    text = str(text)
    text = re.sub(r'http\S+', '', text)  # remove URLs
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # remove mentions
    text = re.sub(r'#\S+', '', text)  # remove hashtags
    text = re.sub(r'[^\u1200-\u137F\s]', '', text)  # keep only Amharic + space
    text = re.sub(r'\s+', ' ', text).strip()  # remove extra spaces
    return text

# Set your data folder
channels = ["zemenexpress", "nevacomputer", "leyueqa", "shewabrand", "fashiontera"]

for channel in channels:
    path = f"data/{channel}/messages.csv"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue

    df = pd.read_csv(path)

    # Clean + normalize
    df['clean_text'] = df['text'].fillna('').apply(normalize_amharic).apply(clean_text)

    # Save new version
    out_path = f"data/{channel}/messages_cleaned.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"✅ Cleaned data saved to: {out_path}")
