import json
from router import route_commit

with open("data/labled_data.json") as f:
    data = json.load(f)

counts = {
    "discard": 0,
    "code_filter": 0,
    "gemini_direct": 0
}

for commit in data:
    decision = route_commit(commit)
    counts[decision] += 1

print("Routing distribution:")
print(counts)