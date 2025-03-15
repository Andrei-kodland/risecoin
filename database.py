import sqlite3

# Create or connect to a SQLite database
def create_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Create a table for storing user data if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            referred_by TEXT,
            referral_count INTEGER
        )
    ''')
    
    # Commit changes and close the connection
    connection.commit()
    connection.close()

# Function to add a user to the database
def add_user(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Check if the user already exists
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    # If the user doesn't exist, add them with a referral count of 0
    if user is None:
        cursor.execute('INSERT INTO users (user_id, referred_by, referral_count) VALUES (?, ?, ?)', (user_id, None, 0))
        connection.commit()

    connection.close()

# Function to update referral count
def update_referral_count(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Increment the referral count for the user
    cursor.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (user_id,))
    connection.commit()

    connection.close()

# Function to get referral count
def get_referral_count(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Retrieve the referral count for the user
    cursor.execute('SELECT referral_count FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    connection.close()
    
    if result:
        return result[0]
    else:
        return 0
