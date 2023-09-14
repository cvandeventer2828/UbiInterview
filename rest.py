from flask import Flask, jsonify, request
import sqlite3
import random
from datetime import date

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('engines.db')
cursor = conn.cursor()

# Create the 'engines' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS engines (
        id INTEGER PRIMARY KEY,
        name TEXT,
        manufacture_date TEXT
    )
''')

# Helper function to generate a random date for testing purposes
def random_manufacture_date():
    year = random.randint(2000, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Assuming a max of 28 days per month
    return f"{year}-{month:02d}-{day:02d}"

@app.route('/engines', methods=['GET'])
def get_engines():
    conn = sqlite3.connect('engines.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM engines')
    engines = [{'id': row[0], 'name': row[1], 'manufacture_date': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({'engines': engines})

@app.route('/engines/<int:engine_id>', methods=['PUT'])
def update_manufacture_date(engine_id):
    new_manufacture_date = request.json.get('manufacture_date')
    conn = sqlite3.connect('engines.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE engines SET manufacture_date = ? WHERE id = ?', (new_manufacture_date, engine_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Manufacture date updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
