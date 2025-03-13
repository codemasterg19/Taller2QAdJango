import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404 , redirect
from .services.product_service import get_pokemons, get_pokemon
from .models import Pokemon
from .forms import PokemonForm
from django.urls import reverse

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
    pokemon = get_object_or_404(Pokemon, name=name)
    return render(request, "products/product.html", {"pokemon": pokemon})



def pokemon_create(request):
    if request.method == "POST":
        form = PokemonForm(request.POST)
        if form.is_valid():
            pokemon = form.save()
            # Contamos el total de pokémon y calculamos la última página
            total = Pokemon.objects.count()
            limit = 20  # Debe coincidir con el límite usado en la paginación
            last_page = math.ceil(total / limit)
            # Construimos la URL de la lista con el parámetro ?page=last_page
            url = reverse('pokemon_list') + f'?page={last_page}'
            return redirect(url)
    else:
        form = PokemonForm()
    return render(request, "products/pokemon_form.html", {"form": form})

def pokemon_update(request, name):
    pokemon = get_object_or_404(Pokemon, name=name)
    # Obtenemos el valor 'next' ya sea de GET o POST; si no existe, usamos la lista de pokémon
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('pokemon_list')
    
    if request.method == 'POST':
        form = PokemonForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = PokemonForm(instance=pokemon)
    
    return render(request, 'products/pokemon_form.html', {'form': form, 'next': next_url})

def pokemon_delete(request, name):
    pokemon = get_object_or_404(Pokemon, name=name)
    if request.method == "POST":
        pokemon.delete()
        return redirect('pokemon_list')
    return render(request, "products/pokemon_confirm_delete.html", {"pokemon": pokemon})