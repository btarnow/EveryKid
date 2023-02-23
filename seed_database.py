"""Script to seed database from books_database.json"""

import os
import json
import crud 
import model
from server import app

os.system("dropdb books_db")
os.system("createdb books_db")

# Prevents error: 
app.app_context().push() 

model.connect_to_db(app)
model.db.create_all()

with open('static/books_database.json') as file:
    book_data = json.loads(file.read())


def seed_books():
    """Seeds books into database"""
    
    for key in book_data.keys():
        book_id = key
        isbn_13 = book_data[key]["isbn_13"]
        title = book_data[key]["title"]
        year_published = book_data[key]["year_published"]
        cover_path = book_data[key]["Cover Path"]
        overview = book_data[key]["overview"]

        book_to_add = crud.create_book(book_id, isbn_13, title, year_published, 
                                       cover_path, overview)
        
        model.db.session.add(book_to_add)


def seed_characters():
    """Seeds characters into database"""

    for key in book_data.keys():
        book_id = key
        gender_identity = book_data[key]["gender_identity"]
        racial_identity = book_data[key]["racial_identity"]
     
        if type(gender_identity) == str:
             character_to_add = crud.create_character(book_id, gender_identity, 
                                              racial_identity)
             model.db.session.add(character_to_add)
        elif type(gender_identity) == list:
            for index in range(len(gender_identity)):
                char_gender = gender_identity[index]
                char_race = racial_identity[index]
                character_to_add = crud.create_character(book_id, char_gender, char_race)
                model.db.session.add(character_to_add)

        
def seed_authors():
    """Seeds authors into database"""

    for key in book_data.keys():
        book_id = key
        author_name = book_data[key]["author_name"]
        for author in author_name:
            author_to_add = crud.create_author(book_id, author)
            model.db.session.add(author_to_add)


def seed_database():
    """Run all seed functions to seed database """
    seed_books()
    seed_characters()
    seed_authors()
    model.db.session.commit() 
    print("All seed functions ran.")

seed_database()


# To Test that these functions are working correctly, execute 
# pg_dump books_db > books_practice.sql






