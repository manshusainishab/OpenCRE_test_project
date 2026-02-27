import os
import json
import re
from google import genai

client = genai.Client(api_key="Not - public")
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are a security knowledge classifier for OWASP-style repositories.

Your task:
Determine whether a commit introduces meaningful new security knowledge.

Security knowledge includes:
- A new vulnerability type
- A new exploitation or bypass technique
- A new attack vector
- A new mitigation strategy
- A new detection or validation method
- A new structured security testing methodology
- A substantial expansion that materially improves how a security issue should be tested, detected, or mitigated

Important:
In documentation-heavy projects (like OWASP guides), adding a new structured test section,
new threat scenarios, or significantly expanding testing guidance counts as security knowledge.

Not security knowledge:
- Formatting changes
- Grammar fixes
- Contributor updates
- Dependency bumps
- Lint or workflow adjustments
- Pure restructuring without new technical insight

Decision rule:
If the commit meaningfully increases actionable security testing or defensive knowledge → TRUE.
If it is purely administrative or cosmetic → FALSE.

When unsure, prefer TRUE over FALSE.

Return JSON only:

[
  { "index": <number>, "is_security_knowledge": true or false }
]
"""

def classify_batch(commits):
    """
    commits: list of dicts
        each dict must contain:
            - message
            - added_lines
    """

    commits_text = ""

    for local_idx, commit in enumerate(commits):
        commits_text += f"""
Commit Index: {local_idx}
Message: {commit['message']}
Files Changed:
{", ".join(commit.get("files", []))}

Added Lines:
{str(commit['added_lines'])[:3000]}
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

    parsed = json.loads(match.group())

    # Safety validation
    if len(parsed) != len(commits):
        raise ValueError("Model returned mismatched batch size.")

    return parsed