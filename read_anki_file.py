import re
import anki_export
import json 

CARD_LIST = []
APKG = anki_export.ApkgReader('anki_spanish_deck.apkg')

def create_clean_card(flashcard):
    card_front = list(flashcard['data']['note']['data']['record'].values())[0]
    card_front = re.sub(r'<span[^>]*>', '', card_front)
    card_front = re.sub(r'</span>', '', card_front) 
    return card_front

def get_flashcards_from_apkg():
    for card in APKG.cards:
        card_front = create_clean_card(card)
        CARD_LIST.append(card_front)

def check_card_in_deck(word: str) :
    for card in APKG.cards:
        if word in card:
            print(f"'{word}' was found. Please remove from the list of words to add.")
            return True
    return False

def create_new_words_list():
    string_list = []
    with open('new_spanish_words.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # Remove any leading/trailing whitespace and newline characters. Also removes any translation or notes I may have written.
            string_list.append(line.split('-')[0].strip())
    return string_list

def card_check_test():
        test_set = create_new_words_list()
        print(test_set)
        for word in test_set: 
           check_card_in_deck(word)

# Uncomment to run card test
# get_flashcards_from_apkg()
# card_check_test()
categories = set()
for card in APKG.cards:
    categories.add(json.dumps((card['data']['deck']['name']).encode('utf-8').decode('utf-8'), ensure_ascii=False, indent = 4))

print(categories)