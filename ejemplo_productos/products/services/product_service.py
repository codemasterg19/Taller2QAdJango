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
    try:
        response = requests.get(f"{API_URL}{param}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error obteniendo el Pokémon {param}: {e}")
        return {}



def load_pokemons():
    if not Pokemon.objects.exists():
        offset = 0
        limit = 20
        pokemons_to_create = []
        
        while True:
            print(f"Cargando pokemons con offset {offset}")
            data = get_pokemons(offset=offset, limit=limit)
            results = data.get("results", [])
            if not results:
                break
            for pokemon in results:
                details = get_pokemon(pokemon["name"])
                if details:
                    sprites = details.get("sprites", {})
                    image_url = sprites.get("front_default") or "https://via.placeholder.com/150"
                    pokemons_to_create.append(Pokemon(
                        name=details.get("name"),
                        weight=details.get("weight"),
                        height=details.get("height"),
                        image=image_url
                    ))
            offset += limit
            if not data.get("next"):
                break
        
        Pokemon.objects.bulk_create(pokemons_to_create)
        return f"{len(pokemons_to_create)} pokémons cargados"
    return "Pokémons ya cargados"

