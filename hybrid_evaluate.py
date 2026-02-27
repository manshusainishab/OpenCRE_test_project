import json
import time
from router import route_commit
from code_filter import structural_code_filter
from gemini_classifier import classify_batch
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Load dataset
with open("data/labled_data.json") as f:
    data = json.load(f)

y_true = []
y_pred = []

to_classify = []
index_mapping = []

# Step 1: Routing + Structural filtering
for idx, commit in enumerate(data):
    y_true.append(commit["label"])
    decision = route_commit(commit)

    if decision == "discard":
        y_pred.append(0)

    elif decision == "code_filter":
        if structural_code_filter(commit):
            index_mapping.append(len(y_pred))
            to_classify.append(commit)
            y_pred.append(None)
        else:
            y_pred.append(0)

    elif decision == "gemini_direct":
        index_mapping.append(len(y_pred))
        to_classify.append(commit)
        y_pred.append(None)

# Step 2: Batch Gemini Classification
BATCH_SIZE = 10

for start in range(0, len(to_classify), BATCH_SIZE):
    batch = to_classify[start:start+BATCH_SIZE]

    results = classify_batch(batch)

    for result in results:
        local_index = result["index"]
        global_index = index_mapping[start + local_index]
        y_pred[global_index] = int(result["is_security_knowledge"])

    time.sleep(3)

# Safety check
assert None not in y_pred
assert len(y_pred) == len(y_true)

# Metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
cm = confusion_matrix(y_true, y_pred)

print("\n===== HYBRID RESULTS =====")
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("\nConfusion Matrix:")
print(cm)