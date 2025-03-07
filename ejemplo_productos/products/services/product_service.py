from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import requests
from ..models import Pokemon

API_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemons(offset=0, limit=20):
    response = requests.get(f"{API_URL}?offset={offset}&limit={limit}")
    if response.status_code == 200:
        data = response.json()
        # Agregar la URL de la imagen a cada Pokémon
        for pokemon in data.get("results", []):
            pokemon_id = pokemon["url"].split("/")[-2]  # Extraer el ID de la URL
            pokemon["image_url"] = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        return data
    print("Error al obtener los Pokémon")
    return {}

def get_pokemon(param):
    response = requests.get(f"{API_URL}{param}")
    if response.status_code == 200:
        return response.json()
    print(f"Error al obtener el Pokémon con ID/nombre: {param}")
    return {}



