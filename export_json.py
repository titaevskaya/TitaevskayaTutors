import json
import data

with open("goals.json", "w", encoding='utf-8') as f:
    json.dump(data.goals, f, ensure_ascii=False)


with open("profiles.json", 'w', encoding='utf-8') as f:
    json.dump(data.teachers, f, ensure_ascii=False)

