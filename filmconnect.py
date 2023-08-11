import sqlite3


conn = sqlite3.connect('film_database.db')


cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS films (
                    filmID INTEGER PRIMARY KEY,
                    title TEXT,
                    yearReleased INTEGER,
                    rating TEXT,
                    duration INTEGER,
                    genre TEXT)''')

# Add data 
filmData = [
    # Film data
]

for film in filmData:
    cursor.execute('''INSERT INTO films (filmID, title, yearReleased, rating, duration, genre)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (film['filmID'], film['title'], film['yearReleased'], film['rating'], film['duration'], film['genre']))

# save the changing
conn.commit()
conn.close()

print("Data add succesfully.")


import sqlite3

def createConnection(db_file):
    """connection """
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database successful.")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def createTable(conn):
    """Create table """
    createTableSql = """
        CREATE TABLE IF NOT EXISTS tblfilms (
            filmID INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            yearReleased INTEGER NOT NULL,
            rating TEXT NOT NULL,
            duration INTEGER NOT NULL,
            genre TEXT NOT NULL
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(createTableSql)
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)

def addFilm(conn, film_data):
 
    insert_sql = "INSERT INTO tblfilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?);"
    try:
        cursor = conn.cursor()
        cursor.execute(insert_sql, film_data)
        conn.commit()
        print("Film added successfully.")
    except sqlite3.Error as e:
        print("Error:", e)

def updateFilm(conn, film_id, film_data):
    """Update an existing film record """
    updateSql = "UPDATE tblfilms SET title=?, yearReleased=?, rating=?, duration=?, genre=? WHERE filmID=?;"
    try:
        cursor = conn.cursor()
        cursor.execute(updateSql, (*film_data, film_id))
        conn.commit()
        print("Film updated successfully.")
    except sqlite3.Error as e:
        print("Error:", e)

def deleteFilm(conn, film_id):
    """Delete a film"""
    delete_sql = "DELETE FROM tblfilms WHERE filmID=?;"
    try:
        cursor = conn.cursor()
        cursor.execute(delete_sql, (film_id,))
        conn.commit()
        print("Film deleted successfully.")
    except sqlite3.Error as e:
        print("Error:", e)

def printAllFilms(conn):
    """Print all films """
    selectAllSql = "SELECT * FROM tblfilms;"
    try:
        cursor = conn.cursor()
        cursor.execute(selectAllSql)
        films = cursor.fetchall()
        for film in films:
            print(film)
    except sqlite3.Error as e:
        print(e)

def PrintFilmsByTitle(conn, title):
    """Print particular title."""
    selectSql= "SELECT * FROM tblfilms WHERE title = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(selectSql, (title,))
        films = cursor.fetchall()
        for film in films:
            print(film)
    except sqlite3.Error as e:
        print(e)

def print_films_by_genre(conn, genre):
    """Print  genre."""
    selectSql= "SELECT * FROM tblfilms WHERE genre = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(selectSql, (genre,))
        films = cursor.fetchall()
        for film in films:
            print(film)
    except sqlite3.Error as e:
        print(e)

def print_films_by_year(conn, year):
    """Print year."""
    selectSql= "SELECT * FROM tblfilms WHERE yearReleased = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(selectSql, (year,))
        films = cursor.fetchall()
        for film in films:
            print(film)
    except sqlite3.Error as e:
        print(e)

def print_films_by_rating(conn, rating):
    """Print  rating."""
    selectSql= "SELECT * FROM tblfilms WHERE rating = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(selectSql, (rating,))
        films = cursor.fetchall()
        for film in films:
            print(film)
    except sqlite3.Error as e:
        print(e)

def search_films(conn, search_option):
    """Search for criteria."""
    if search_option == "1":
        title = input("Enter the film title to search for: ")
        PrintFilmsByTitle(conn, title)
    elif search_option == "2":
        genre = input("Enter the genre to search for: ")
        print_films_by_genre(conn, genre)
    elif search_option == "3":
        year = int(input("Enter the year to search for: "))
        print_films_by_year(conn, year)
    elif search_option == "4":
        rating = input("Enter the rating to search for: ")
        print_films_by_rating(conn, rating)
    else:
        print("Invalid search option.")

def main():
    db_file = "filmflix.db"
    conn = createConnection(db_file)
    createTable(conn)

    main_option = ""
    while main_option != "6":
        print("\nOptions menu:")
        print("1. Add a record")
        print("2. Delete a record")
        print("3. Amend a record")
        print("4. Print all records")
        print("5. Search films")
        print("6. Exit")

        main_option = input("Choose an option (1-6): ")

        if main_option == "1":  # Add a record
            title = input("Enter film title: ")
            # control film name
            selectSql= "SELECT * FROM tblfilms WHERE title = ?;"
            cursor = conn.cursor()
            cursor.execute(selectSql, (title,))
            existing_film = cursor.fetchone()

            if existing_film:
                print("A film with the same title already exists:")
                print(existing_film)
                choice = input("Do you want to continue adding? (yes/no): ")
                if choice.lower() != "yes":
                    continue
  
            else:
                addFilm(conn, film_data)

            yearReleased = int(input("Enter year released: "))
            rating = input("Enter rating: ")
            duration = int(input("Enter duration (in minutes): "))
            genre = input("Enter genre: ")
            film_data = (title, yearReleased, rating, duration, genre)

            addFilm(conn, film_data)

        elif main_option == "2":  # Delete a record
            film_id = int(input("Enter film ID to delete: "))
            deleteFilm(conn, film_id)

        elif main_option == "3":  # Amend a record
            film_id = int(input("Enter film ID to update: "))
            title = input("Enter new film title: ")
            yearReleased = int(input("Enter new year released: "))
            rating = input("Enter new rating: ")
            duration = int(input("Enter new duration (in minutes): "))
            genre = input("Enter new genre: ")
            film_data = (title, yearReleased, rating, duration, genre)

            # same name
            selectSql= "SELECT * FROM tblfilms WHERE title = ?;"
            cursor = conn.cursor()
            cursor.execute(selectSql, (title,))
            existing_film = cursor.fetchone()

            if existing_film:
                print("A film with the same title already exists:")
                print(existing_film)
                choice = input("Do you want to continue updating? (yes/no): ")
                if choice.lower() != "yes":
                    continue

            updateFilm(conn, film_id, film_data)

        elif main_option == "4":  # Print all records
            printAllFilms(conn)

        elif main_option == "5":  # Search films
            print("\nSearch menu:")
            print("1. Search by film title")
            print("2. Search by genre")
            print("3. Search by year")
            print("4. Search by rating")
            search_option = input("Choose a search option (1-4): ")
            search_films(conn, search_option)

    conn.close()
    print("Exiting FilmFlix application.")

if __name__ == "__main__":
    main()
