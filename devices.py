import sqlite3
import principles
from collections import namedtuple

Device = namedtuple("Device", ["id", "name", "aspects", "is_persistent"])
