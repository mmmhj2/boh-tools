import sqlite3
import principles, wisdoms
import dataclasses

@dataclasses.dataclass
class Skill:
    id: str
    name: str
    aspects: dict[str, str]
    wisdoms: list[str]
    is_language: bool

def parse_skill (skill_entry) -> Skill:
    assert skill_entry['aspects']['skill'] == 1
    skill = Skill(skill_entry['id'], skill_entry['Label'], {}, [], False)
    print(f"Found skill {skill.id}")

    for k, v in skill_entry['aspects'].items():
        if k[:2] == 'w.':
            skill.wisdoms.append(k[2:])
        elif k == 'skill.language':
            skill.is_language = True
        else:
            skill.aspects[k] = v
    return skill

def write_skill (skill_list: list[Skill], connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS skill")
    command = "CREATE TABLE IF NOT EXISTS skill(id PRIMARY KEY, name, language" \
        + principles.comma_seperated_principles() \
        + wisdoms.comma_seperated_skill_wisdoms() + ")"
    cursor.execute(command)
    
    skill_flattened_list = []
    for skill in skill_list:
        skill_flattened = {"id": skill.id, "name": skill.name, "language": skill.is_language}

        for p in principles.PRINCIPLES:
            skill_flattened[p] = 0
        for e in wisdoms.WISDOMS:
            skill_flattened["w_" + e] = 0

        for aspect, magnitude in skill.aspects.items():
            skill_flattened[aspect] = magnitude
        for wisdom in skill.wisdoms:
            skill_flattened["w_" + wisdom] = 1

        skill_flattened_list.append(skill_flattened)
    
    command = "INSERT INTO skill VALUES (:id, :name, :language" \
        + principles.colon_seperated_principles() \
        + wisdoms.colon_seperated_skill_wisdoms() + ")"
    cursor.executemany(
        command,
        skill_flattened_list)
    connection.commit()
