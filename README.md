# Anki Generated Flashcards
A python script that generates anki flashcards leveraging Gemini API.

## Installation
### Prerequisites
- A Gemini API key which you can get at [Google AI Studio](https://aistudio.google.com/apikey)
- Pip installed
- Python 3.13.3+

### Steps
1. `pip install -r requirements.txt`
2. Fill `new_words.txt` with words you would like to generate flashcards for. 
3. Fill `categories.txt` with Anki deck and subdeck names. This will be used to organize flashcards into appropriate buckets.
4. Create `api_keys.py` and store your Gemini API key there. You can also hard code a local variable in `main.py` if you aren't making your code public. 
5. Export your current Anki deck as `anki_deck.apkg` into your copied repo directory. This is used to check for duplicate words between your current deck and the list of new words.

## Usage
1. Run `python main.py` or `python3 main.py` depending on your system command.
2. Decide if you're creating files for the first time. If you're running this script for the first time, you should answer with "Y". This will create:
    - `generated_categories.txt` - Associates a deck name/category with each word in `new_words.txt` 
    - `generated_flashcard_metadata.txt` - A file used to store text output responses from the Gemini API. There is a limit to how much text can be sent as a response for the Free tier version of the Gemini API as of 5/26/2025. So this file is used to store unfinished outputs which is used in the script to figure out what words in `new_words.txt` still need to be processed. This file is constantly overriden to store new responses from the Gemini API and shouldn't be used to analyze final outputs. 
    - `flashcard_data.txt` - The final generated cleaned output from the Gemini API. This **can** be a summation of several `generated_flashcard_metadata.txt`
3. Analyze `flashcard_data.txt` as a preliminary check before generating flashcards
4. Decide if you want to continue and create anki flashcards.
5. Decide if you want to create test flashcards. This allows the imported file to create a new deck to ensure you don't mess up your current deck.
6. After creating `output.apkg` import the file into Anki.