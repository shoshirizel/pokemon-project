import pymysql
import json

with open("poke_data.json") as the_file:
    pokemon_data = json.load(the_file)


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)



if connection.open:
    print("the connection is opened")


def insert_poke():
    for poke in pokemon_data:
        with connection.cursor() as poke_cursor:
            query = f"INSERT into pokemon (id, name, height, weight) values ('{poke['id']}', '{poke['name']}', '{poke['height']}', '{poke['weight']}')"
            poke_cursor.execute(query)
            connection.commit()
        
        with connection.cursor() as poke_cursor:
            query = f"INSERT into pokemon_type (pokemon_id, type) values ('{poke['id']}',  '{poke['type']}')"
            poke_cursor.execute(query)
            connection.commit()



def insert_owners(): 
    for poke in pokemon_data:
        for owner in poke["ownedBy"]:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM owners where name = '{owner['name']}'"
                cursor.execute(query)
                if not cursor.fetchone():
                    query = f"INSERT into owners (name, town) values ('{owner['name']}', '{owner['town']}')"
                    cursor.execute(query)
                    connection.commit()





def insert_pokemon_owned_by():
    for poke in pokemon_data:
        for owner in poke["ownedBy"]:
            with connection.cursor() as cursor:                
                query = f"INSERT into pokemon_owners (pokemon_id, owner_name) values ( '{poke['id']}', '{owner['name']}')"
                cursor.execute(query)
                connection.commit()


insert_poke()
insert_owners()
insert_pokemon_owned_by()

