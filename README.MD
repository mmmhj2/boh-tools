Book of Hours tool scripts
===

Tired of taking notes mannually, I created these scripts to keep various things in the game in track.
These scripts create a SQLite database by taking in JSON files containing game data, and the database can be used to look up stuffs easily.

Usage:
```
python -m extract_data "<Game Installation Folder>"
```
Should it works, a database file named `database.db` would be created.

However, as of writing, it seems that game file `tomes.json` is corrupted and JSON parser fails to produce any result.
You might have to fix this manually by deleting the last element in the file.

### SQLite quick reference

1. Find memories to upgrade a certain skill:
`SELECT name FROM memory WHERE edge > 0 or moon > 0;`
2. Find books which produce memory to upgrade a skill:
`SELECT name FROM tome WHERE memory in (SELECT id FROM memory WHERE lantern > 0 or sky > 0);`
3. Find devices and inks that aid in reading a book:
`SELECT name FROM aspected_items WHERE (inherited == '_device' or json_extract(aspected_items.other_aspects, '$.ink')) and lantern > 0;`
3. Count number of books written in certain language:
`SELECT count(*) FROM tome WHERE language == 'vak';`
