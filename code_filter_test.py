import json
from router import route_commit
from code_filter import structural_code_filter

with open("data/labled_data.json") as f:
    data = json.load(f)

code_filtered = []

for commit in data:
    if route_commit(commit) == "code_filter":
        decision = structural_code_filter(commit)
        code_filtered.append({
            "hash": commit["hash"],
            "label": commit["label"],
            "kept": decision
        })

print("Code filter results:")
for item in code_filtered:
    print(item)