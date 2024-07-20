import sqlite3
import principles, wisdoms
from collections import namedtuple

Memory = namedtuple("memory", ["id", "name", "aspects", "is_persistent"])

def parse_memory (memory_entry) -> Memory:
    assert memory_entry["inherits"] == '_memory' \
        or memory_entry["inherits"] == '_memory.persistent'
    
    print (f"Found memory {memory_entry['ID']}")
    
    m = Memory(memory_entry["ID"], memory_entry["Label"], {}, memory_entry["inherits"] == '_memory.persistent')
    for key, item in memory_entry["aspects"].items():
        m.aspects[key] = item
    return m

def write_memory (memory_list : list[Memory], connection : sqlite3.Connection):
    '''Write a list of memory into a sqlite database for quick reference'''
    cursor = connection.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS memory")
    command = "CREATE TABLE IF NOT EXISTS memory(id PRIMARY KEY, name, persist" \
        + principles.comma_seperated_principles() \
        + wisdoms.comma_seperated_evolve_wisdoms() + ")"
    cursor.execute(command)
    
    memory_flattened_list = []
    for memory in memory_list:
        memory_flattened = {"id": memory.id, "name": memory.name, "persist": memory.is_persistent}

        for p in principles.PRINCIPLES:
            memory_flattened[p] = 0
        for e in wisdoms.WISDOMS:
            memory_flattened["e_" + e] = 0

        for aspect, magnitude in memory.aspects.items():
            memory_flattened[aspect.replace(".", "_")] = magnitude

        memory_flattened_list.append(memory_flattened)
    
    command = "INSERT INTO memory VALUES (:id, :name, :persist" \
        + principles.colon_seperated_principles() \
        + wisdoms.colon_seperated_evolve_wisdoms() + ")"
    cursor.executemany(
        command,
        memory_flattened_list)
    connection.commit()
