import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_tables(conn):
    try:
        c = conn.cursor()

        # Drop old tables if they exist
        c.execute("DROP TABLE IF EXISTS users")
        c.execute("DROP TABLE IF EXISTS videos")
        c.execute("DROP TABLE IF EXISTS tags")
        c.execute("DROP TABLE IF EXISTS videotags")
        c.execute("DROP TABLE IF EXISTS thumbnails")
        c.execute("DROP TABLE IF EXISTS votes")

        # Create tables
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT
            )
        """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS videos (
                video_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT
            )
        """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE
            )
        """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS videotags (
                video_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (video_id, tag_id),
                FOREIGN KEY (video_id) REFERENCES videos (video_id),
                FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
            )
        """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS thumbnails (
                thumbnail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                thumbnail_path TEXT,
                FOREIGN KEY (video_id) REFERENCES videos (video_id)
            )
        """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS votes (
                vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                video_id INTEGER,
                thumbnail_id INTEGER,
                tag_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (video_id) REFERENCES videos (video_id),
                FOREIGN KEY (thumbnail_id) REFERENCES thumbnails (thumbnail_id),
                FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
            )
        """
        )

        conn.commit()
    except sqlite3.Error as e:
        print(e)


def main():
    print("Creating database and tables...")
    conn = create_connection("app.db")
    create_tables(conn)
    conn.close()


if __name__ == "__main__":
    main()
