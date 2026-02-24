import os
import json
import re
import time
import pandas as pd
from google import genai
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Configure client
client = genai.Client(api_key=("API_KEY"))
MODEL = "gemini-2.5-flash"

BATCH_SIZE = 10
RATE_LIMIT_SECONDS = 3

SYSTEM_PROMPT = """
You are a strict security commit classifier.

For each commit:

Step 1: Determine if the commit introduces NEW technical security knowledge.
Step 2: If it only clarifies, restructures, rephrases, or slightly expands existing content without introducing a new attack, mitigation, or testing method → classify as FALSE.

Security knowledge means introduction of:
- A new vulnerability type
- A new exploitation technique
- A new bypass method
- A new attack vector
- A new mitigation strategy
- A new detection mechanism
- A new structured testing methodology

Not security knowledge:
- Rewording explanations
- Expanding descriptions of existing attacks
- Minor example additions
- Formatting changes
- Markdown edits
- Documentation restructuring
- Grammar fixes
- Dependency updates
- Administrative updates

Important rule:
If the commit does NOT introduce a fundamentally new security concept or method → FALSE.

Be conservative.

Return JSON only as:

[
  { "index": <number>, "is_security_knowledge": true or false }
]
"""

def classify_batch(batch_df):
    commits_text = ""

    for local_idx, (_, row) in enumerate(batch_df.iterrows()):
        commits_text += f"""
Commit Index: {local_idx}
Message: {row['message']}
Added Lines:
{str(row['added_lines'])[:3000]}
---
"""

    prompt = f"""
{SYSTEM_PROMPT}

Classify the following commits:

{commits_text}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"temperature": 0}
    )

    text = response.text.strip()

    match = re.search(r'\[.*\]', text, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid JSON response:\n{text}")

    return json.loads(match.group())


# Load dataset
df = pd.read_csv("data/gold_dataset.csv")

y_true = df["label"].astype(int).tolist()
y_pred = []

print("Running batch evaluation...\n")

for start in range(0, len(df), BATCH_SIZE):
    batch_df = df.iloc[start:start+BATCH_SIZE]

    try:
        results = classify_batch(batch_df)

        # Map predictions back
        for result in results:
            idx = result["index"]
            pred = int(result["is_security_knowledge"])
            y_pred.append(pred)

        print(f"Processed commits {start+1} to {start+len(batch_df)}")

        # Rate limiting
        time.sleep(RATE_LIMIT_SECONDS)

    except Exception as e:
        raise RuntimeError(f"Batch failed: {e}")


# Metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
cm = confusion_matrix(y_true, y_pred)

print("\n===== RESULTS =====")
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("\nConfusion Matrix:")
print(cm)