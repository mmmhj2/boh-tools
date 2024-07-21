import sqlite3, json
import principles, wisdoms
import dataclasses

@dataclasses.dataclass
class AspectedItem:
    id: str
    name: str
    aspects: dict[str, int]
    inherited: str
    
def extract_aspected_item_data(binary : bytearray, connection : sqlite3.Connection):
    raw_data = json.loads(binary)
    raw_data = raw_data['elements']
    
    item_list = []
    
    for item in raw_data:
        item_list.append(parse_aspected_item(item))
    write_aspected_item(item_list, connection)

def parse_aspected_item (item_entry) -> AspectedItem:
    print (f"Found item {item_entry['ID']}, inherited from {item_entry['inherits']}")
    
    m = AspectedItem(item_entry["ID"], item_entry["Label"], {}, item_entry["inherits"])
    for key, item in item_entry["aspects"].items():
        # Ignore "boost." aspects
        if key[:6] == 'boost.':
            continue
        m.aspects[key] = int(item)
    return m

def write_aspected_item (item_list : list[AspectedItem], connection : sqlite3.Connection):
    cursor = connection.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS memory")
    command = "CREATE TABLE IF NOT EXISTS aspected_items(id PRIMARY KEY, name, inherited" \
        + principles.comma_seperated_principles() + ", other_aspects)"
    cursor.execute(command)
    
    item_flattened_list = []
    for item in item_list:
        item_flattened = {"id": item.id, "name": item.name, "inherited": item.inherited, "other_aspects": {}}

        for p in principles.PRINCIPLES:
            item_flattened[p] = 0

        aspect_dict = item.aspects
        for aspect, magnitude in aspect_dict.items():
            if aspect in principles.PRINCIPLES:
                item_flattened[aspect] = magnitude
            else:
                item_flattened["other_aspects"][aspect] = magnitude

        item_flattened["other_aspects"] = json.dumps(item_flattened["other_aspects"])
        item_flattened_list.append(item_flattened)
    
    command = "INSERT OR REPLACE INTO aspected_items VALUES (:id, :name, :inherited" \
        + principles.colon_seperated_principles() + ", :other_aspects)"
    cursor.executemany(
        command,
        item_flattened_list)
    connection.commit()

if __name__ == '__main__':
    connection = sqlite3.connect('items.db')
    with open("aspecteditems.json", 'rb') as f:
        extract_aspected_item_data(f.read(), connection)
