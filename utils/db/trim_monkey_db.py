import time
from os import stat
from shutil import copy

from core_database import SQLiteDB

infile = "db.sqlite3"
outfile = f"db_{round(time.time())}.sqlite3"

copy(infile, outfile)

db = SQLiteDB(infile)

start_size = stat(infile).st_size

# Non-best tables for GITADORA and IIDX are not used in game
for table in ("guitarfreaks_scores", "drummania_scores", "iidx_scores"):
    db.drop_table(table)
    print("Dropped", table)

db.close()

end_size = stat(infile).st_size

print(f"{infile} {round((start_size - end_size) / 1024 / 1024, 2)} MiB trimmed")
