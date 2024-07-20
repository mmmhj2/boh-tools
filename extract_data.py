import json, sys, sqlite3
import memories, skills

def extract_aspected_item_data(binary : bytearray, connection : sqlite3.Connection):
    raw_data = json.loads(binary)
    raw_data = raw_data['elements']
    
    memory_list = []
    
    for item in raw_data:
        if item["inherits"] == "_memory" or item["inherits"] == "_memory.persistent":
            memory_list.append(memories.parse_memory(item))
    
    
    memories.write_memory(memory_list, connection)

def extract_skill_data(binary : bytearray, connection : sqlite3.Connection):
    raw_data = json.loads(binary)
    raw_data = raw_data['elements']
    skill_list = []
    
    for item in raw_data:
        skill_list.append(skills.parse_skill(item))
    skills.write_skill(skill_list, connection)
    
if __name__ == "__main__":

    connection = sqlite3.connect("database.db")

    # Read utf-16 binary data
    with open("aspecteditems.json", 'rb') as f:
        extract_aspected_item_data(f.read(), connection)
    with open("skills.json", 'rb') as f:
        extract_skill_data(f.read(), connection)
    
