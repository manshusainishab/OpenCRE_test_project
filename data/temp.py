import json

with open("./labled_data.json") as f:
    data = json.load(f)

print("Total commits:", len(data))

missing_fields = []
duplicate_hashes = set()
seen = set()

for commit in data:
    # Check required keys
    required = ["hash", "message", "files", "extensions", "added_lines", "label"]
    for key in required:
        if key not in commit:
            missing_fields.append((commit.get("hash"), key))

    # Check duplicate hashes
    if commit["hash"] in seen:
        duplicate_hashes.add(commit["hash"])
    seen.add(commit["hash"])

print("Missing fields:", missing_fields)
print("Duplicate hashes:", duplicate_hashes)

# Label distribution
labels = [c["label"] for c in data]
print("Label distribution:", {
    0: labels.count(0),
    1: labels.count(1)
})