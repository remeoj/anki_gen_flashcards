import re
import anki_export
import pyexcel_xlsxwx
import json 

# with ZipFile("anki_spanish_deck.apkg") as zf:
#             zf.extractall()

with anki_export.ApkgReader('anki_spanish_deck.apkg') as apkg:
    # pyexcel_xlsxwx.save_data('test.xlsx', apkg.export(), config={'format': None})
    deck_sets = apkg.export()
    # pretty_json = json.dumps(export, indent=4)
    # print(pretty_json)
    # print(export)

    card_list = []
    # for deck_name in deck_sets:
    #     for card in deck_sets[deck_name]:
    #         card_list.append(card[0])
    # print(card_list)
    for card in apkg.cards:
        card_front = list(card['data']['note']['data']['record'].values())[0]
        card_front = re.sub(r'<span[^>]*>', '', card_front)
        card_front = re.sub(r'</span>', '', card_front) 
        card_list.append(card_front)
        
        # pretty_json = json.dumps(card, indent=4)
        # print(pretty_json)
        # break
    print(card_list)

# import sqlite3
# import os
# import tempfile
# import zipfile

# def read_collection_anki2(apkg_path):
#     """
#     Reads data directly from the collection.anki2 file within an .apkg.

#     Args:
#         apkg_path (str): The path to the .apkg file.
#     """
#     try:
#         with tempfile.TemporaryDirectory() as tmpdir:
#             with zipfile.ZipFile(apkg_path, 'r') as apk_file:
#                 apk_file.extract('collection.anki21', tmpdir)
#                 db_path = os.path.join(tmpdir, 'collection.anki21')

#             conn = sqlite3.connect(db_path)
#             cursor = conn.cursor()

#             # Now you can execute SQL queries on the 'cursor' object
#             # to read data from the tables in the database.

#             # Example: Get a list of all tables
#             cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             tables = [row[0] for row in cursor.fetchall()]
#             print("Tables in the database:", tables)

#             # Example: Get the number of notes
#             cursor.execute("SELECT COUNT(*) FROM notes")
#             note_count = cursor.fetchone()[0]
#             print(f"Number of notes: {note_count}")

#             # Example: Fetch the first 10 notes (id, guid, mid, flds)
#             cursor.execute("SELECT id, guid, mid, flds FROM notes LIMIT 10")
#             first_notes = cursor.fetchall()
#             for note in first_notes:
#                 print(f"Note ID: {note[0]}, GUID: {note[1]}, Model ID: {note[2]}, Fields: {note[3]}")

#             # Remember to close the connection
#             conn.close()

#     except zipfile.BadZipFile:
#         print(f"Error: Invalid .apkg file: {apkg_path}")
#     except sqlite3.Error as e:
#         print(f"Error accessing the Anki database: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     apkg_file_path = 'anki_spanish_deck.apkg'  # Replace with the actual path
#     read_collection_anki2(apkg_file_path)