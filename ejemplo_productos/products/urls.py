from django.urls import path
from .views import pokemon_list, pokemon_detail

urlpatterns = [
    path('', pokemon_list, name="pokemon_list"),  # Lista de Pokémon
    path("<str:name>/", pokemon_detail, name="pokemon_detail"),  # Detalle de Pokémon
]