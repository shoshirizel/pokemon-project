
from flask import Flask, Response, request
import requests

def chain(pokemon_name):
    url_ = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    species = requests.get(url=url_, verify=False).json()
    species_url = species['species']['url'] 
    evolution_chain_url = requests.get(url=species_url, verify=False).json()['evolution_chain']['url']
    return requests.get(url=evolution_chain_url, verify=False).json()['chain']

def evolve_to(chain, name):
    while chain['species']['name'] != name:
        chain = chain['evolves_to'][0]
    if not chain.get('evolves_to'):
        return None
    new_name = chain['evolves_to'][0]['species']['name']
    new_poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{new_name}", verify=False).json()
    return new_poke
