import random
from pypinyin import lazy_pinyin, Style
from chin_dict.chindict import ChinDict
cd = ChinDict()

note_file = "/Users/skye/Notes/Chinese/Known Hanzi.md"

with open(note_file) as file:
    note_text = file.read()

hanzi = []
for c in note_text:
    if c not in hanzi:
        hanzi.append(c)

is_playing = True
for c in hanzi:
    if not is_playing: break
    user_input = input("Type words: ")

    if user_input == "quit":
        is_playing = False

    for c in user_input:
        h = cd.lookup_char(c)
        if h.pinyin:
            if c not in hanzi:
                hanzi.append(c)
                print(f"Added {c}!")
    print()

# Sort hanzi
hanzi = sorted(hanzi)

# Update file
new_text = "".join(hanzi)
with open(note_file, "w") as file:
    file.write(new_text)