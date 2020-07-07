import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def update_pokemon(owner, old_poke_id, new_poke_id):
    with connection.cursor() as cursor:
        query =f"""UPDATE pokemon_owners 
        SET pokemon_id = '{new_poke_id}'
        WHERE owner_name = '{owner}' and pokemon_id = '{old_poke_id}'
        """   
        cursor.execute(query) 
        connection.commit()  



def by_owner(owner):
    with connection.cursor() as cursor:
        query = f"""select pokemon.name 
        from pokemon join pokemon_owners 
        on pokemon.id = pokemon_owners.pokemon_id 
        where owner_name = '{owner}'"""
        cursor.execute(query)
        res = cursor.fetchall()
    l = []
    
    for poke in res:
        l.append(poke['name'])
    
    return l

def valid_owner(owner):
    with connection.cursor() as cursor:
        query = f"""select * 
        from owners
        where name = '{owner}'"""
        cursor.execute(query)
        res = cursor.fetchone()
    return res is not None
