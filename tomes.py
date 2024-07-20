import sqlite3, json
import principles, wisdoms
import dataclasses

@dataclasses.dataclass
class Tome:
    id: str; name: str
    aspect: str; difficulty: int
    lesson: str; lesson_count: int
    period: str
    language: str
    memory: str
    
def extract_tome_data(binary : bytearray, connection : sqlite3.Connection):
    raw_data = json.loads(binary)
    raw_data = raw_data['elements']
    tome_list = []
    for item in raw_data:
        tome_list.append(parse_tome(item))
    write_tome(tome_list, connection)

def parse_tome(tome_entry) -> Tome:
    tome = Tome(tome_entry['ID'], tome_entry['Label'], '', 0, '', 0, '', '', '')
    print(f"Found tome {tome.id}")

    for a in tome_entry['aspects']:
        if a[:8] == 'mystery.':
            tome.aspect = a[8:]
            tome.difficulty = int(tome_entry['aspects'][a])
        elif a[:7] == 'period.':
            tome.period = a[7:]
        elif a[:2] == 'w.':
            tome.language = a[2:]
    
    trigger = tome_entry['xtriggers']
    assert len(trigger["mastering." + tome.aspect]) == 1
    tome.lesson = trigger["mastering." + tome.aspect][0]["id"]
    tome.lesson_count = trigger["mastering." + tome.aspect][0]["level"]
    
    if "reading." + tome.aspect in trigger:
        assert len(trigger["reading." + tome.aspect]) == 1
        tome.memory = trigger["reading." + tome.aspect][0]["id"]

    return tome

def write_tome(tome_list: list[Tome], connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS tome(id PRIMARY KEY, name, aspect, difficulty, lesson, lesson_count, period, language, memory)"
        )
    
    mapped_list = map(dataclasses.asdict, tome_list)
    cursor.executemany(
        "INSERT OR REPLACE INTO tome VALUES (:id, :name, :aspect, :difficulty, :lesson, :lesson_count, :period, :language, :memory)",
        mapped_list
    )
    connection.commit()

if __name__ == "__main__":

    connection = sqlite3.connect("tomes.db")
    with open("tomes.json", 'rb') as f:
        extract_tome_data(f.read(), connection)
