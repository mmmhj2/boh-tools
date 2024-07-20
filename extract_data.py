import json, sys, sqlite3
import memories, skills, tomes

if __name__ == "__main__":

    connection = sqlite3.connect("database.db")

    # Read utf-16 binary data
    with open("aspecteditems.json", 'rb') as f:
        memories.extract_aspected_item_data(f.read(), connection)
    with open("skills.json", 'rb') as f:
        skills.extract_skill_data(f.read(), connection)
    with open("tomes.json", 'rb') as f:
        tomes.extract_tome_data(f.read(), connection)
    
