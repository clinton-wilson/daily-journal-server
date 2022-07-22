import sqlite3
import json
from models import Mood

def get_all_moods():
    """function to retrieve all moods"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        m.id,
        m.label
        From mood m
        """)

        moods = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)

    return json.dumps(moods)
