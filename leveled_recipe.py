import sqlite3, json
import dataclasses
import principles

@dataclasses.dataclass
class LeveledRecipe:
    id: str
    name: str
    skill: str
    principle: str
    level: int
    precursor: str
    production: str
    time: int

def extract_leveled_recipe(raw_data : dict, connection : sqlite3.Connection):
    raw_data = raw_data['recipes']
    
    recipe_list = []
    
    for item in raw_data:
        recipe_list.append(parse_leveled_recipe(item))
    write_leveled_recipe(recipe_list, connection)

def parse_leveled_recipe(recipe) -> LeveledRecipe:
    assert recipe['craftable'] == True
    leveledRecipe = LeveledRecipe(recipe['id'], recipe['Label'], '', '', 0, '', '', recipe['warmup'])
    print(f"Found recipe {leveledRecipe.id}")
    
    for aspect, magnitude in recipe['reqs'].items():
        if aspect == 'ability':
            continue
        if aspect[:2] == 's.':
            leveledRecipe.skill = aspect
        elif aspect in principles.PRINCIPLES:
            assert leveledRecipe.principle == ''
            leveledRecipe.principle = aspect
            leveledRecipe.level = magnitude
        else:
            assert leveledRecipe.precursor == ''
            leveledRecipe.precursor = aspect
    
    for aspect, magnitude in recipe['effects'].items():
        if magnitude > 0:
            assert leveledRecipe.production == ''
            leveledRecipe.production = aspect
    
    return leveledRecipe

def write_leveled_recipe(recipe_list: list[LeveledRecipe], connection: sqlite3.Connection):
    cursor = connection.cursor()
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS leveled_recipe(id PRIMARY KEY, name, skill, principle, level, precursor, production, time)"
        )
    mapped_list = map(dataclasses.asdict, recipe_list)
    cursor.executemany(
        "INSERT OR REPLACE INTO leveled_recipe VALUES (:id, :name, :skill, :principle, :level, :precursor, :production, :time)",
        mapped_list
    )
    connection.commit()

if __name__ == '__main__':
    connection = sqlite3.connect("recipes.db")
    with open('crafting_2_keeper.json', 'rb') as f:
        extract_leveled_recipe(json.loads(f.read()), connection)
    with open('crafting_3_scholar.json', 'rb') as f:
        extract_leveled_recipe(json.loads(f.read()), connection)
    with open('crafting_4b_prentice.json', 'rb') as f:
        extract_leveled_recipe(json.loads(f.read()), connection)
