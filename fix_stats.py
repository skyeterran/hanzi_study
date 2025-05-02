import json

with open("statistics.json") as file:
    stats = json.loads(file.read())

scores = {}

for name, score in stats["hits"].items():
    scores[name] = score

for name, score in stats["misses"].items():
    if name in scores:
        scores[name] -= score
    else:
        scores[name] = -score

with open("statistics.json", "w", encoding = 'utf8') as file:
    json.dump(
        {"scores": scores},
        file,
        ensure_ascii = False,
        indent = 4
    )