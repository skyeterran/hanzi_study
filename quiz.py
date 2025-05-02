import random
import json
from pypinyin import lazy_pinyin, Style
from chin_dict.chindict import ChinDict
cd = ChinDict()
from hanzipy.dictionary import HanziDictionary
hd = HanziDictionary()

note_file = "/Users/skye/Notes/Chinese/Known Hanzi.md"

with open(note_file) as file:
    note_text = file.read()

unique_hanzi = []
for c in note_text:
    if c not in unique_hanzi:
        unique_hanzi.append(c)
random.shuffle(unique_hanzi)

with open("statistics.json") as file:
    statistics = json.loads(file.read())

new_stats = {"scores": {}}

def stat_add(stats, word):
    if word not in stats["scores"]:
        stats["scores"][word] = 1
    else:
        stats["scores"][word] += 1

def stat_sub(stats, word):
    if word not in stats["scores"]:
        stats["scores"][word] = -1
    else:
        stats["scores"][word] -= 1

def mark_hit(word):
    if word not in new_stats:
        stat_add(statistics, word)
        stat_add(new_stats, word)

def mark_miss(word):
    if word not in new_stats:
        stat_sub(statistics, word)
        stat_sub(new_stats, word)

def get_recognizable_word(hanzi):
    search_results = hd.get_examples(hanzi)
    search_results = search_results["high_frequency"] + search_results["mid_frequency"]
    random.shuffle(search_results)
    for definition in search_results:
        word = definition["simplified"]

        # Check if I know all the hanzi in this word
        recognizable = True
        for char in word:
            if char not in unique_hanzi:
                recognizable = False
                break
        
        if recognizable:
            return definition

is_playing = True
for hanzi in unique_hanzi:
    if not is_playing: break

    definition = get_recognizable_word(hanzi)
    word = definition["simplified"]
    meanings = definition["definition"].split("/")
    print(f"{word}: {meanings[0]}")

    pinyin_tone = "".join(lazy_pinyin(word, Style.TONE))
    pinyin_tone_num = "".join(lazy_pinyin(word, Style.TONE3))
    pinyin_toneless = "".join(lazy_pinyin(word, Style.NORMAL))

    def print_meaning():
        for m in meanings:
            print(f"    - {m}")
 
    is_guessing = True
    just_won = False
    while is_guessing:
        if just_won:
            just_won = False
            is_guessing = False
            print_meaning()
            user_input = input()
            if user_input == "quit":
                is_guessing = False
                is_playing = False
            #os.system("cls||clear")
        else:
            user_input = input(f"> ")
            user_input_toneless = user_input
            if user_input != "":
                user_input_toneless = ""
                for letter in user_input:
                    if not letter.isdigit():
                        user_input_toneless += letter
            if user_input == "quit":
                is_guessing = False
                is_playing = False
            elif user_input == pinyin_tone_num:
                mark_hit(word)
                print(f"  {pinyin_tone} (Perfect!)")
                just_won = True
            elif user_input_toneless == pinyin_toneless:
                if user_input == pinyin_toneless:
                    mark_hit(word)
                    print(f"  {pinyin_tone} (Correct!)")
                    just_won = True
                else:
                    mark_miss(word)
                    # User guessed the wrong tone
                    print(f"  Close! Wrong tone.")
            elif user_input == "":
                print(f"{pinyin_tone}")
                just_won = True
            else:
                mark_miss(word)

print()
print("New scores:")
for word, new_score in new_stats["scores"].items():
    total_score = statistics["scores"][word]
    if new_score >= 0:
        change = f"+{new_score}"
    else:
        change = f"{new_score}"
    print(f"{word}: {total_score} ({change})")
print()

# Update stats
with open("statistics.json", "w", encoding = 'utf8') as file:
    json.dump(
        statistics,
        file,
        ensure_ascii = False,
        indent = 4
    )