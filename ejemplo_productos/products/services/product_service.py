from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import requests
from ..models import Pokemon

API_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemons(offset=0, limit=20):
    response = requests.get(f"{API_URL}?offset={offset}&limit={limit}")
    if response.status_code == 200:
        data = response.json()
        # Agregar la URL de la imagen a cada Pokémon (opcional)
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
        count = 0
        
        while True:
            print(f"Cargando pokemons con offset {offset}")
            data = get_pokemons(offset=offset, limit=limit)
            results = data.get("results", [])
            if not results:
                break
            
            for pokemon in results:
                details = get_pokemon(pokemon["name"])
                if details:
                    # Usar el sprite frontal para la imagen
                    sprites = details.get("sprites", {})
                    image_url = sprites.get("front_default") or "https://via.placeholder.com/150"
                    
                    # Crear el Pokémon con los campos básicos
                    new_pokemon = Pokemon.objects.create(
                        name=details.get("name"),
                        weight=details.get("weight"),
                        height=details.get("height"),
                        base_experience=details.get("base_experience", 0),
                        order=details.get("order", 0),
                        image=image_url,
                    )
                    
                    # Asignar habilidades y tipos como listas de nombres
                    abilities_list = [ability_data["ability"]["name"] for ability_data in details.get("abilities", [])]
                    new_pokemon.abilities = abilities_list

                    types_list = [type_data["type"]["name"] for type_data in details.get("types", [])]
                    new_pokemon.types = types_list

                    # Procesar las estadísticas y asignarlas a los campos individuales
                    for stat in details.get("stats", []):
                        stat_name = stat["stat"]["name"]
                        base_stat = stat["base_stat"]
                        if stat_name == "hp":
                            new_pokemon.hp = base_stat
                        elif stat_name == "attack":
                            new_pokemon.attack = base_stat
                        elif stat_name == "defense":
                            new_pokemon.defense = base_stat
                        elif stat_name == "special-attack":
                            new_pokemon.special_attack = base_stat
                        elif stat_name == "special-defense":
                            new_pokemon.special_defense = base_stat
                        elif stat_name == "speed":
                            new_pokemon.speed = base_stat

                    new_pokemon.save()  # Guardar los cambios tras asignar listas y estadísticas
                    count += 1
            
            offset += limit
            if not data.get("next"):
                break
        
        return f"{count} pokémons cargados"
    return "Pokémons ya cargados"
