import api_keys
import json
from google.genai import types
from google import genai
import re
import read_anki_file as raf
import time

client = genai.Client(api_key=api_keys.GEMINI_API)

def create_generated_categories():
  """
  Generates a category for each word in `new_words_list` and stores the array of json objects in generated_categories.txt
  """
  print("Generating categories for list of new words...")
  all_categories = ""
  with open('categories.txt', 'r', encoding='utf-8') as file:
      for line in file:
        all_categories += line.strip() + "\n"

  system_instruction = f'''You will be given words that are meant to be added to flashcards. A flashcard has a category which we are trying to decide. Here's the list of categories:\n{all_categories}\nYou must choose a category for each word. The final format should be a list of json objects in this format: {{word: word given, category: category picked}}. So for example, if the word is Bailar. The output would be {{'Bailar':'Español::Verbos'}}. Ensure that every word given keeps the same format and isn't grammatically changed.'''

  new_words = raf.create_new_words_list()
  new_words_string = ", ".join(new_words)
  generated_categories = run_gemini(system_instruction, new_words_string)
  file_name = "generated_categories.txt"
  try:
    with open(file_name, 'w', encoding='utf-8') as file:
      file.write(generated_categories)
      print("Done generating categories!")
  except IOError as e:
    print(f"Error: Could not write to file '{file_name}'. {e}")

def generate_flashcard_content(words:str):
  """
  Calls Gemini API to create flashcard content for a list of words in the form of a string. If there are a lot of words, the generated text output may not show all the words in the list.

  Args:
    words: A list of words in the form of a string. 
  """

  system_instruction = f'''You are a spanish flashcard maker. I am an English student trying to learn spanish. I am going to give you a list of words. Create flashcards in the order of the words that I give you. For each word given, create a card with the format below. For example, if the word given is bano, the output would look like this:

  {{"word": "Bano", "question" : "Bano", "answer" : "Bathroom", "spanish_example" : "El bano es grande.", "english_example" : The bathroom is big."}}

  If a spanish infinitive verb is given, for example bailar, output objects for the infinitive verb and the conjugations. You can group el/ella/usted and ellos/ellas/ustedes. Do not create an object for the vosotros conjugation. Only give the objects asked for in the final output. For example:

  {{"word": "Bailar", "question" : "Bailar", "answer" : "To dance", "spanish_example" : "Ella sabe bailar muy bien.", "english_example" : "She knows how to dance very well."}}

  {{"word": "Bailar","question" : "Bailar (yo)", "answer" : "Bailo", "spanish_example" : "A veces bailo en la cocina mientras cocino.", "english_example" : "Sometimes I dance in the kitchen while I cook."}}

  {{"word": "Bailar", "question" : "Bailar (tu)", "answer" : "Bailas", "spanish_example" : "¿Bailas salsa?", "english_example" : "Do you dance salsa?"}}

  {{"word": "Bailar", "question" : "Bailar (nosotros)", "answer" : "Bailamos", "spanish_example" : "En la boda de mi amigo, nosotros bailamos toda la noche.", "english_example" : "At my friend's wedding, we danced all night."}}

  {{"word": "Bailar", "question" : "Bailar (el/ella/usted)", "answer" : "Baila", "spanish_example" : "Mi hermano baila con su novia.", "english_example" : "My brother dances with his girlfriend."}}

  {{"word": "Bailar", "question" : "Bailar (ellos/ellas/ustedes)", "answer" : "Bailan",spanish_example "Los niños bailan cuando escuchan su canción favorita.", "english_example" : "The children dance when they hear their favorite song."}}

  Output rules:
  - Vosotros should not be mentioned at all.
  - If an infinitive verb is the word we are creating flashcards for, list all conjugations in the described format.
  - Ensure that every word given keeps the same format and isn't grammatically changed. Don't add any slashes. 
  - When creating the json objects, the closing brace follow by the comma shouldn't have a space in between them. For example, the string should be "{"},"} and not {"} ,"}". 
  - If you identify that the list of words is in a different language than spanish, for example japanese, modify this prompt to work for that language.
  '''
  generated_flashcards = run_gemini(system_instruction, words)
  print(generated_flashcards)
  file_name = "generated_flashcard_metadata.txt"
  try:
    # Open the file in write mode ('w')
    # If the file doesn't exist, it will be created.
    # If the file exists, its content will be truncated (overwritten).
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(generated_flashcards)
    print(f"String successfully saved to '{file_name}'")
  except IOError as e:
    print(f"Error: Could not write to file '{file_name}'. {e}")

def run_gemini(system_instruction:str, content:str):
   response = client.models.generate_content(
        model="gemini-2.0-flash", 
        config = types.GenerateContentConfig(system_instruction=system_instruction),
        contents=content
    )
   return response.text

def create_json_object(json_str:str): 
  try:
      json_object = json.loads(json_str)
      return json_object
  except json.JSONDecodeError as e:
      print(f"Error decoding JSON from regex match: {e}")
      return ""
  
def load_json_from_file(file_name: str):
  """
  Returns a list of dictionary objects from `file_name`.
  """
  with open(file_name, 'r', encoding='utf-8') as file:
      # Load the JSON data from the file
      # json_data = json.load(file)
      file_content = file.read()
      match = re.search(r'\[.*\]', file_content, re.DOTALL) # re.DOTALL allows '.' to match newlines
      if match:
        json_array_string = match.group(0) # Get the matched string
        return create_json_object(json_array_string)

def clean_flashcards(flashcard_list:list, last_word:str):
  cleaned_flashcards = []
  for card in flashcard_list:
    flashcard_word = card['word']
    if last_word != flashcard_word:
      cleaned_flashcards.append(card)
  return cleaned_flashcards

def process_flashcards_and_leftovers():
  """
  Cleans up the potentially broken json object in generated_flashcard_metadata.txt and returns a proper json object. Additionally, if the json object is broken, this function returns what words still need to be printed out.
  """
  file_name = "generated_flashcard_metadata.txt"
  partial_flashcards = []
  try:
    with open(file_name, 'r', encoding='utf-8') as file:
        file_content = file.read()
        match = re.search(r'\[.*', file_content, re.DOTALL)
        json_match = re.search(r'\[.*\]', file_content, re.DOTALL) 
        if json_match:
          print("JSON object is complete!")
          complete_json_obj = json_match.group(0) 
          partial_flashcards = create_json_object(complete_json_obj)
          return partial_flashcards, []
        elif match:
          # Take an incomplete json object and make it complete.
          incomplete_json_obj = match.group(0) 
          last_brace_index = incomplete_json_obj.rfind('},')
          proper_json_obj = incomplete_json_obj[:last_brace_index +1] + "]"
          print(f"Extracted JSON string (regex): {proper_json_obj}")
          partial_flashcards = create_json_object(proper_json_obj)
  except Exception as e :
    print(f"Error: The file '{file_name}' was not found.")

  # Find what was the last word generated and create a list that still needs to be generated. 
  new_words = raf.create_new_words_list()
  last_generated_word = ""
  for word in reversed(new_words):
    if last_generated_word:
       # If we found the last generated word, stop searching.
       break
    for card in partial_flashcards:
      flashcard_word = card['word']
      if word == flashcard_word:
        last_generated_word = word
        break
  if not last_generated_word:
    return [], []
  print("last word: ", last_generated_word)
  print(new_words)
  Last_word_index = new_words.index(last_generated_word)
  last_word = new_words[Last_word_index]
  print("PARTIAL CARDS: ", partial_flashcards)
  print(partial_flashcards.__class__)
  partial_flashcards = clean_flashcards(partial_flashcards, last_word)
  print("CLEANED PARTIAL CARDS: ", partial_flashcards)
  print(partial_flashcards.__class__)
  leftover_words = new_words[Last_word_index:]
  print(leftover_words)
  return partial_flashcards, leftover_words

def create_flashcard_file():
  print("Generating flashcard content and storing in flashcard_data.txt...")
  card_list = []
  new_words = raf.create_new_words_list()
  request_sent = False
  while new_words:
    new_words_string = ", ".join(new_words)
    if request_sent:
      print("Giving model a break for 60 seconds...")
      time.sleep(60)
      print("Continuing...")
    else:
      request_sent = True
    generate_flashcard_content(new_words_string)
    flashcard_list, leftover_words = process_flashcards_and_leftovers()
    new_words = leftover_words
    card_list += flashcard_list

  print(card_list)

  file_path = "flashcard_data.txt"

  with open(file_path, 'w', encoding='utf-8') as file:
    inner_content = ', '.join(json.dumps(item, ensure_ascii=False) for item in card_list)
    print(inner_content)
    full_file_content = '[' + inner_content + ']'
    file.write(full_file_content) 
    print("Stored generated content in flashcard_data.txt!")

def create_generated_categories_dict():
  parsed_data = load_json_from_file("generated_categories.txt")

  category = {}
  for json_obj in parsed_data:
     for key,value in json_obj.items():
        category[key] = value
  return category

def create_flashcards_with_categories():
  print("Combining categories and flashcard content...")
  flashcards = load_json_from_file("flashcard_data.txt")
  categories = create_generated_categories_dict()
  for flashcard in flashcards:
     word = flashcard['word']
     flashcard['category'] = categories[word]
  print("Combined categories and flashcard content!")
  return flashcards

def create_generated_flashcards():
  flashcards = create_flashcards_with_categories()