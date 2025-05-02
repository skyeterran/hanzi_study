import json

with open("statistics.json") as file:
    statistics = json.loads(file.read())

scores = statistics["scores"]
sorted_scores = sorted(
    scores.items(),
    key = lambda x : x[1],
    reverse = True
)
for word, score in sorted_scores:
    print(f"{word}: {scores[word]}")