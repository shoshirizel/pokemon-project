from flask import Flask, Response, request
import pymysql
import requests
import json
import pokemon
import poke_api
import owner

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
    pokemon.add(poke)


@app.route('/pokemons', methods = ["POST"])
def add_pokemon():
    poke = request.get_json()
    if not (poke.get("id") and poke.get("name") and poke.get("height") and poke.get("types")):
        return "Not correct input", 400
    try:
        insert_pokemon(poke) 
    except Exception:
            return "We had it before", 409         
    return "Added", 201
    

@app.route('/pokemons')
def get_pokemon():
    type_ = request.args.get('type')
    id = request.args.get('id')
    owner_ = request.args.get('owner')
    poke_name = request.args.get('name')
    if type_:
        res = pokemon.by_type(type_)
        return json.dumps({"The pokemons": res}), 202
    elif id:
        res =  pokemon.by_id(id)
        if res:
            return json.dumps({"The pokemon": res}), 202
        return json.dumps({"The pokemon": "Any"}), 404
    elif poke_name:
        res = pokemon.by_name(poke_name)
        if res:
            return json.dumps({"The pokemon id": res}), 202
        return json.dumps({"The pokemon": "Any"}), 404
    elif owner_:
        res = owner.by_owner(owner_)
        return json.dumps({"The pokemons": res}), 202



    return json.dumps({"Message":"You didnt give us any information about the pokemon."}), 400

    


@app.route('/pokemons/<owner>/<pokemon_id>', methods=["DELETE"])
def delete_owner_pokemon(owner, pokemon_id):
    if not pokemon.is_owners_pokemon(owner, pokemon_id):
        return "You cant delete something that not exist.", 400
    pokemon.delete(owner, pokemon_id)
    return "Deleted", 200


@app.route('/evolve/<owner_>/<pokemon_>', methods=["PUT"])
def evolve(owner_, pokemon_):
    poke_id = pokemon.by_name(pokemon_)
    if not pokemon.is_owners_pokemon(owner_, poke_id):
        return "Its not your pokemon.", 404
    chain = poke_api.chain(pokemon_)
    new_poke = poke_api.evolve_to(chain, pokemon_)
    if not new_poke:
        return "Pokemon cant evolve.", 400
    try:
        insert_pokemon(new_poke)
    except Exception:
        pass

    try:
        owner.update_pokemon(owner_, poke_id, new_poke['id'])
    except Exception:
        return f"Hi {owner_}! you cant evolve your pokemon to pokemon you alredy have.", 400
   
    return f"Hi {owner_}! your pokemon {pokemon_} evolved to {new_poke['name']}.", 200

@app.route('/owners/<owner_>')
def valid_owner(owner_):
    if owner.valid_owner(owner_):
        return f"Hei {owner_}", 202
    return "You are not an owner", 404


if __name__ == '__main__':
    app.run(port=port_number)
