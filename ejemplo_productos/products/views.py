from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .services.product_service import get_pokemons, get_pokemon
from .models import Pokemon

def pokemon_list(request):
    offset = int(request.GET.get("offset", 0))
    limit = 20

    # Obtener los datos de la API
    data = get_pokemons(offset=offset, limit=limit)
    pokemons = data.get("results", [])
    count = data.get("count", 0)

    # Calcular los valores para la paginación
    next_offset = offset + limit if offset + limit < count else None
    previous_offset = offset - limit if offset - limit >= 0 else None

    return render(request, "products/products.html", {
        "pokemons": pokemons,
        "offset": offset,
        "next_offset": next_offset,
        "previous_offset": previous_offset,
    })

def pokemon_detail(request, name):
    pokemon = get_pokemon(name)
    return render(request, "products/product.html", {"pokemon": pokemon})