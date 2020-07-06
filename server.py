from flask import Flask, Response, request
import pymysql
import requests
import json

app = Flask(__name__)
port_number = 3000


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


def insert_pokemon(poke):
    if not (poke.get("id") and poke.get("name") and poke.get("height") and poke.get("types")):
        return "Not correct input", 409
    with connection.cursor() as poke_cursor:
        query = f"INSERT into pokemon (id, name, height, weight) values ('{poke['id']}', '{poke['name']}', '{poke['height']}', '{poke['weight']}')"
        poke_cursor.execute(query)
        for type in set(poke["types"]):
            query = f"INSERT into pokemon_type (pokemon_id, type) values ('{poke['id']}',  '{type}')"
            poke_cursor.execute(query)
            connection.commit()


@app.route('/add', methods = ["POST"])
def add_pokemon():
    poke = request.get_json()
    insert_pokemon(poke)          
    return "Added", 201
    

@app.route('/pokemon_by_type/<type>')
def get_pokemon_by_type(type):
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
        return json.dumps({"The pokemons": l})


@app.route('/delete', methods=["DELETE"])
def delete_owner_pokemon():
    pair = request.get_json()
    with connection.cursor() as cursor:
        query =f"""DELETE FROM pokemon_owners 
        WHERE owner_name = '{pair['owner']}' and pokemon_id in
        (SELECT id as pokemon_id FROM pokemon WHERE name = '{pair['pokemon']}') """
        cursor.execute(query)
        connection.commit()
    return "Deleted"


@app.route('/evolved/<owner>', methods=["PUT"])
def evolve(owner):
    pokemon = request.get_json()
    url_ = f"https://pokeapi.co/api/v2/pokemon/{pokemon['name']}"
    species = requests.get(url=url_, verify=False).json()
    species_url = species['species']['url'] 
    evolution_chain_url = requests.get(url=species_url, verify=False).json()['evolution_chain']['url']
    chain = requests.get(url=evolution_chain_url, verify=False).json()['chain']
    while chain['species']['name'] != pokemon['name']:
        chain = chain['evolves_to'][0]
    if not chain.get('evolves_to'):
        return "Can't evolve", 400
    name = chain['evolves_to'][0]['species']['name']
    print(name)
    poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", verify=False).json()
    try:
        insert_pokemon(poke)
    except Exception:
        pass

    with connection.cursor() as cursor:
        query =f"""UPDATE FROM pokemon_owners 
        SET pokemon_id = '{poke['id']}'
        WHERE owner_name = '{owner}' and pokemon_id = '{pokemon['id']}'
        """
        cursor.execute(query)
        connection.commit()


    return ""


if __name__ == '__main__':
    app.run(port=port_number)
