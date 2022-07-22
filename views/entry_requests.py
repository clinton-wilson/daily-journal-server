import sqlite3
import json
from models import Entry, Mood


def get_all_entries():
    """
    Gets all entries from the table entry
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        a.id,
        a.concept,
        a.entry,
        a.mood_id,
        a.date,
        m.id,
        m.label
        FROM entry a
        JOIN mood m
            ON m.id = a.mood_id
        """)

        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row ['date'])

            mood = Mood(row['id'], row['label'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect ("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        a.id,
        a.concept,
        a.entry,
        a.mood_id,
        a.date,
        m.id,
        m.label
        FROM entry a
        JOIN mood m
            ON m.id = a.mood_id
        WHERE a.id = ?                    
        """, (id, ))

        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['label'])

        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'], data['date'])

        entry.mood = mood.__dict__

    return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def search_entries(search_term):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entry a
        WHERE a.entry LIKE ?
        """, ( f"%{search_term[0]}%", ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row ['date'])

            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_journal_entry(new_entry):
    """function to create new journal entry"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO entry
        ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?)
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date']))

        id = db_cursor.lastrowid

        new_entry['id'] = id

    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect('./dailyjournal.sqlite3') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE entry
                SET
                    concept =?,
                    entry = ?,
                    mood_id = ?,
                    date = ?
                WHERE id =?
                """, (new_entry['concept'], new_entry['entry'],
                    new_entry['mood_id'], new_entry['date'], id, ))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False
        else:
            return True
        