import sys, sqlite3, json
import memories, skills, tomes, aspected_items, leveled_recipe

if __name__ == "__main__":
    
    path = ''
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if path[-1] != '/' and path[-1] != '\\' :
            path += '/'
        path += 'bh_Data/StreamingAssets/bhcontent/core/elements/'

    connection = sqlite3.connect("database.db")

    # Read utf-16 binary data
    with open(path + "aspecteditems.json", 'rb') as f:
        b = json.loads(f.read())
        memories.extract_memories(b, connection)
        aspected_items.extract_aspected_item_data(b, connection)
    with open(path + "skills.json", 'rb') as f:
        skills.extract_skill_data(json.loads(f.read()), connection)
    with open(path + "tomes.json", 'rb') as f:
        tomes.extract_tome_data(json.loads(f.read()), connection)
    with open('crafting_2_keeper.json', 'rb') as f:
        leveled_recipe.extract_leveled_recipe(json.loads(f.read()), connection)
    with open('crafting_3_scholar.json', 'rb') as f:
        leveled_recipe.extract_leveled_recipe(json.loads(f.read()), connection)
    with open('crafting_4b_prentice.json', 'rb') as f:
        leveled_recipe.extract_leveled_recipe(json.loads(f.read()), connection)
    
