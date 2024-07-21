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
    tally: int
    other_aspects: dict
    
def extract_tome_data(raw_data : dict, connection : sqlite3.Connection):
    raw_data = raw_data['elements']
    tome_list = []
    for item in raw_data:
        tome_list.append(parse_tome(item))
    write_tome(tome_list, connection)

def parse_tome(tome_entry) -> Tome:
    tome = Tome(tome_entry['ID'], tome_entry['Label'], '', 0, '', 0, '', '', '', 0, {})
    print(f"Found tome {tome.id}")

    aspect_dict = tome_entry['aspects']
    for key, value in aspect_dict.items():
        if key[:8] == 'mystery.':
            assert key[8:] in principles.PRINCIPLES
            tome.aspect = key[8:]
            tome.difficulty = int(value)
        elif key[:7] == 'period.':
            tome.period = key[7:]
        elif key[:2] == 'w.':
            tome.language = key[2:]
        elif key == 'cost.tally':
            tome.tally = int(value)
        else:
            tome.other_aspects[key] = value
    
    triggers = tome_entry['xtriggers']
    assert len(triggers["mastering." + tome.aspect]) == 1
    mastering = triggers["mastering." + tome.aspect][0]
    # strip x. prefix
    tome.lesson = mastering["id"][2:]
    tome.lesson_count = mastering["level"]
    if "reading." + tome.aspect in triggers:
        assert len(triggers["reading." + tome.aspect]) == 1
        reading = triggers["reading." + tome.aspect][0]
        tome.memory = reading["id"]
    
    # strip r. aspect
    assert 'r.' + tome.lesson in tome.other_aspects
    del tome.other_aspects['r.' + tome.lesson]
    # strip soph aspect
    assert tome.other_aspects['soph'] == tome.difficulty
    del tome.other_aspects['soph']

    return tome

def write_tome(tome_list: list[Tome], connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS tome(id PRIMARY KEY, 
        name, aspect, difficulty, lesson, lesson_count, 
        period, language, memory, tally, other_aspects)
        ''')
    
    def fn(x):
        x = dataclasses.asdict(x)
        x['other_aspects'] = json.dumps(x['other_aspects'])
        return x
    
    mapped_list = map(fn, tome_list)
    cursor.executemany(
        '''INSERT OR REPLACE INTO tome VALUES 
        (:id, :name, :aspect, :difficulty, :lesson, 
        :lesson_count, :period, :language, :memory, 
        :tally, :other_aspects)''',
        mapped_list
    )
    connection.commit()

if __name__ == "__main__":

    connection = sqlite3.connect("tomes.db")
    with open("tomes.json", 'rb') as f:
        extract_tome_data(json.loads(f.read()), connection)
