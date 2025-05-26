import genanki
import generate_content as gc
import random;

deck_id = 1420189368
# deck_name = "Español::sdahiu"

def create_anki_model():
  note_type_name = "PyGeneratedNoteType_v1"
  card_style = """
  .card {
    font-family: arial;
    font-size: 45px;
    text-align: center;
    color: black;
    background-color: white;
  }
  """

  anki_model = genanki.Model(
    deck_id,
    note_type_name,
    fields=[
      {'name': 'question'},
      {'name': 'answer'},
      {'name': 'spanish_example'},
      {'name': 'english_example'},
    ],
    templates=[
      {
        'name': 'PyGeneratedCardType_v1',
        'qfmt': '{{question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{answer}}<div style="font-family: \'Arial\'; font-size: 20px;">{{spanish_example}}</div><div style="font-family: \'Arial\'; font-size: 20px;">{{english_example}}</div>',
      },
    ],
    css=card_style)
  return anki_model

def should_create_test_flashcards():
  user_input = input("Do you want to create test flashcards. We recommend doing this as a first run import to avoid wrong flashcards being added to your main deck (Y/N)? ")
  user_input = user_input.lower()
  if(user_input == 'y'):
    return True
  return False

def create_anki_notes(flashcards:list):
  enable_test_flashcards = should_create_test_flashcards()
  print("Creating anki notes...")
  decks = {}

  for card in flashcards:      
    category = card['category']
    if enable_test_flashcards:
      category = "Test::" + category
    question = card['question']
    answer = card['answer']
    spanish_example = card['spanish_example']
    english_example = card['english_example']
    note = genanki.Note(
      model=create_anki_model(),
      fields=[question, answer, spanish_example, english_example])
    if category in decks:
      deck = decks[category]
      deck.add_note(note)
    else:
      random_model_id = random.randrange(1 << 30, 1 << 31)
      deck = genanki.Deck(random_model_id, category)
      deck.add_note(note)
      decks[category] = deck
  deck_list = list(decks.values())

  genanki.Package(deck_list).write_to_file('output.apkg')
  print("Created anki notes and stored them in output.apkg")

def initial_setup():
  user_input = input("Do you want to create generated files (Y/N)? ")
  user_input = user_input.lower()
  if(user_input == 'y'):
    gc.create_generated_categories()
    gc.create_flashcard_file()

  user_input = input("Please check flashcard_data.txt to see if the generated content is good. If it is, would you like to continue. This will create anki flashcards in output.apkg (Y/N)? ")

  if(user_input == 'y'):
    flashcards = gc.create_flashcards_with_categories()
    create_anki_notes(flashcards)
  elif(user_input == 'n'):
    print("Cancelling program. Please restart the script if you'd like to create anki flashcards.")

if __name__ == "__main__":
  initial_setup()