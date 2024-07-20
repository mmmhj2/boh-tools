import json, sys, sqlite3
import memories

def extract_data(string):
    raw_data = json.loads(string)
    raw_data = raw_data['elements']
    
    memory_list = []
    
    for item in raw_data:
        if item["inherits"] == "_memory" or item["inherits"] == "_memory.persistent":
            memory_list.append(memories.parse_memory(item))
    
    connection = sqlite3.connect("database.db")
    memories.write_memory(memory_list, connection)

    
if __name__ == "__main__":
    file = "aspecteditems.json"
    if (len(sys.argv) == 2):
        file = sys.argv[1]
    
    # Read utf-16 binary data
    with open(file, 'rb') as f:
        extract_data(f.read())
    
