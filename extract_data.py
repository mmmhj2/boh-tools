import sys, sqlite3
import memories, skills, tomes

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
        memories.extract_aspected_item_data(f.read(), connection)
    with open(path + "skills.json", 'rb') as f:
        skills.extract_skill_data(f.read(), connection)
    with open(path + "tomes.json", 'rb') as f:
        tomes.extract_tome_data(f.read(), connection)
    
