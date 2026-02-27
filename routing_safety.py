import json
from router import route_commit

with open("data/labled_data.json") as f:
    data = json.load(f)

false_negative_risk = []

for commit in data:
    decision = route_commit(commit)

    if decision == "discard" and commit["label"] == 1:
        false_negative_risk.append(commit["hash"])

print("Potential false negatives due to routing:", false_negative_risk)