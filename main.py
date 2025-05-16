from google import genai
from google.genai import types
import genanki

deck_id = 1420189368
deck_name = "Español::sdahiu"

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
  deck_name,
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Example'},
  ],
  templates=[
    {
      'name': 'PyGeneratedv1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<div style="font-family: \'Arial\'; font-size: 20px;">{{Example}}</div>',
    },
  ],
  css=card_style)

my_note = genanki.Note(
  model=anki_model,
  fields=['Capital of Argentina', 'Buenos Aires', 'hello this is examplessa'])

my_deck = genanki.Deck(
  1420189368,
  deck_name)

my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file('output.apkg')


def run_gemini():
    client = genai.Client(api_key="")
    system_instruction = "You are a flashcard generator."

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        config = types.GenerateContentConfig(system_instruction=system_instruction),
        contents="Explain how AI works in a few words"
    )
    print(response.text)
    if response.usage_metadata is not None:
      print(response.usage_metadata.prompt_token_count)