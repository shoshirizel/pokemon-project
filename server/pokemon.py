
import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def add(pokemon):
    with connection.cursor() as poke_cursor:
        query = f"INSERT into pokemon (id, name, height, weight) values ('{pokemon['id']}', '{pokemon['name']}', '{pokemon['height']}', '{pokemon['weight']}')"
        poke_cursor.execute(query)
        for type in set(pokemon["types"]):
            query = f"INSERT into pokemon_type (pokemon_id, type) values ('{pokemon['id']}',  '{type}')"
            poke_cursor.execute(query)
        connection.commit()


def by_type(type):
    with connection.cursor() as cursor:
        query = f"""select pokemon.name 
        from pokemon join pokemon_type 
        on pokemon.id = pokemon_type.pokemon_id 
        where type = '{type}'"""
        cursor.execute(query)
        res = cursor.fetchall()
    l = []
    
    for poke in res:
        l.append(poke['name'])
    
    return l




def by_id(id):
    with connection.cursor() as cursor:
        query = f"""select pokemon.name 
        from pokemon
        where id = '{id}'"""
        cursor.execute(query)
        res = cursor.fetchone()
    return res['name']


def by_name(name):
    with connection.cursor() as cursor:
        query = f"""select id 
        from pokemon
        where name = '{name}'"""
        cursor.execute(query)
        res = cursor.fetchone()
    if res is not None:
        return res['id']
    return None


def delete(owner, pokemon):
    with connection.cursor() as cursor:
        query =f"""DELETE FROM pokemon_owners 
        WHERE owner_name = '{owner}' and pokemon_id = '{pokemon}' """
        cursor.execute(query)
        connection.commit()


def is_owners_pokemon(owner, pokemon):
    with connection.cursor() as cursor:
        query = f"""SELECT * FROM pokemon_owners
        WHERE owner_name = '{owner}' and pokemon_id = '{pokemon}'"""
        cursor.execute(query)
        res = cursor.fetchone()
    return res is not None




