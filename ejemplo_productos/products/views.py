from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .services.product_service import get_pokemons, get_pokemon
from .models import Pokemon

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Pokemon

def pokemon_list(request):
    pokemons = Pokemon.objects.all()  # O la fuente que uses
    limit = 20
    paginator = Paginator(pokemons, limit)
    
    # Usamos el parámetro "page" en la URL
    page = request.GET.get('page', 1)
    try:
        pokemons_page = paginator.page(page)
    except PageNotAnInteger:
        pokemons_page = paginator.page(1)
    except EmptyPage:
        pokemons_page = paginator.page(paginator.num_pages)

    current_page = pokemons_page.number
    max_pages_to_show = 5  # Cantidad máxima de números a mostrar en la paginación
    half_range = max_pages_to_show // 2

    if paginator.num_pages <= max_pages_to_show:
        display_page_range = paginator.page_range
    else:
        start = current_page - half_range
        end = current_page + half_range
        if start < 1:
            start = 1
            end = max_pages_to_show
        if end > paginator.num_pages:
            end = paginator.num_pages
            start = paginator.num_pages - max_pages_to_show + 1
        display_page_range = range(start, end + 1)

    context = {
        'pokemons': pokemons_page,
        'current_page': current_page,
        'page_range': display_page_range,
        'total_pages': paginator.num_pages,
    }
    return render(request, "products/products.html", context)


def pokemon_detail(request, name):
    pokemon = get_pokemon(name)
    return render(request, "products/product.html", {"pokemon": pokemon})