from django.urls import path
from .views import pokemon_list, pokemon_detail, pokemon_create, pokemon_update, pokemon_delete

urlpatterns = [
    path('', pokemon_list, name="pokemon_list"),  # Lista de Pokémon
    path("<str:name>/", pokemon_detail, name="pokemon_detail"),  # Detalle de Pokémon
    path('pokemon/create/', pokemon_create, name='pokemon_create'),
    path('pokemon/<str:name>/update/', pokemon_update, name='pokemon_update'),
    path('pokemon/<str:name>/delete/', pokemon_delete, name='pokemon_delete'),
]