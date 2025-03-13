import json
from django import forms
from django.core.exceptions import ValidationError
from .models import Pokemon
# Listas estáticas de habilidades y tipos
ABILITIES_CHOICES = [
    ('adaptability', 'Adaptability'),
    ('aerilate', 'Aerilate'),
    ('analytic', 'Analytic'),
    ('anger-point', 'Anger Point'),
    ('anticipation', 'Anticipation'),
    ('arena-trap', 'Arena Trap'),
    ('aroma-veil', 'Aroma Veil'),
    ('bad-dreams', 'Bad Dreams'),
    ('battery', 'Battery'),
    ('battle-armor', 'Battle Armor'),
    ('big-pecks', 'Big Pecks'),
    ('blaze', 'Blaze'),
    ('bulletproof', 'Bulletproof'),
    ('cheek-pouch', 'Cheek Pouch'),
    ('chlorophyll', 'Chlorophyll'),
    ('clear-body', 'Clear Body'),
    ('cloud-nine', 'Cloud Nine'),
    ('color-change', 'Color Change'),
    ('compound-eyes', 'Compound Eyes'),
    ('contrary', 'Contrary'),
    ('corrosion', 'Corrosion'),
    ('cursed-body', 'Cursed Body'),
    ('cute-charm', 'Cute Charm'),
    ('damp', 'Damp'),
    ('dancer', 'Dancer'),
    ('dark-aura', 'Dark Aura'),
    ('defeatist', 'Defeatist'),
    ('defiant', 'Defiant'),
    ('delicate-touch', 'Delicate Touch'),
    ('download', 'Download'),
    ('drizzle', 'Drizzle'),
    ('drought', 'Drought'),
    ('dry-skin', 'Dry Skin'),
    ('early-bird', 'Early Bird'),
    ('effect-spore', 'Effect Spore'),
    ('electric-surge', 'Electric Surge'),
    ('emergency-exit', 'Emergency Exit'),
    ('flame-body', 'Flame Body'),
    ('flame-boost', 'Flame Boost'),
    ('flare-boost', 'Flare Boost'),
    ('flash-fire', 'Flash Fire'),
    ('flower-gift', 'Flower Gift'),
    ('flower-veil', 'Flower Veil'),
    ('fluffy', 'Fluffy'),
    ('forecast', 'Forecast'),
    ('forewarn', 'Forewarn'),
    ('friend-guard', 'Friend Guard'),
    ('frisk', 'Frisk'),
    ('full-metal-body', 'Full Metal Body'),
    ('fur-coat', 'Fur Coat'),
    ('gale-wings', 'Gale Wings'),
    ('gluttony', 'Gluttony'),
    ('gooey', 'Gooey'),
    ('guts', 'Guts'),
    ('harvest', 'Harvest'),
    ('healer', 'Healer'),
    ('heatproof', 'Heatproof'),
    ('heavy-metal', 'Heavy Metal'),
    ('honey-gather', 'Honey Gather'),
    ('huge-power', 'Huge Power'),
    ('hustle', 'Hustle'),
    ('hydration', 'Hydration'),
    ('hyper-cutter', 'Hyper Cutter'),
    ('ice-body', 'Ice Body'),
    ('illuminate', 'Illuminate'),
    ('illusion', 'Illusion'),
    ('immunity', 'Immunity'),
    ('imposter', 'Imposter'),
    ('infiltrator', 'Infiltrator'),
    ('inner-focus', 'Inner Focus'),
    ('insomnia', 'Insomnia'),
    ('intimidate', 'Intimidate'),
    ('iron-barbs', 'Iron Barbs'),
    ('iron-fist', 'Iron Fist'),
    ('justified', 'Justified'),
    ('keen-eye', 'Keen Eye'),
    ('klutz', 'Klutz'),
    ('leaf-guard', 'Leaf Guard'),
    ('levitate', 'Levitate'),
    ('light-metal', 'Light Metal'),
    ('lightning-rod', 'Lightning Rod'),
    ('limber', 'Limber'),
    ('liquid-ooze', 'Liquid Ooze'),
    ('long-reach', 'Long Reach'),
    ('magic-bounce', 'Magic Bounce'),
    ('magic-guard', 'Magic Guard'),
    ('magician', 'Magician'),
    ('mega-launcher', 'Mega Launcher'),
    ('mirror-armor', 'Mirror Armor'),
    ('misty-surge', 'Misty Surge'),
    ('mold-breaker', 'Mold Breaker'),
    ('moody', 'Moody'),
    ('motor-drive', 'Motor Drive'),
    ('moxie', 'Moxie'),
    ('multiscale', 'Multiscale'),
    ('multitype', 'Multitype'),
    ('mummy', 'Mummy'),
    ('natural-cure', 'Natural Cure'),
    ('neuroforce', 'Neuroforce'),
    ('no-guard', 'No Guard'),
    ('normalize', 'Normalize'),
    ('oblivious', 'Oblivious'),
    ('overcoat', 'Overcoat'),
    ('overgrow', 'Overgrow'),
    ('own-tempo', 'Own Tempo'),
    ('pickpocket', 'Pickpocket'),
    ('pickup', 'Pickup'),
    ('pixilate', 'Pixilate'),
    ('plus', 'Plus'),
    ('poison-heal', 'Poison Heal'),
    ('poison-point', 'Poison Point'),
    ('poison-touch', 'Poison Touch'),
    ('prankster', 'Prankster'),
    ('pressure', 'Pressure'),
    ('pure-power', 'Pure Power'),
    ('quick-feet', 'Quick Feet'),
    ('rain-dish', 'Rain Dish'),
    ('rattled', 'Rattled'),
    ('reckless', 'Reckless'),
    ('refrigerate', 'Refrigerate'),
    ('regenerator', 'Regenerator'),
    ('ripen', 'Ripen'),
    ('rks-system', 'RKS System'),
    ('rock-head', 'Rock Head'),
    ('rough-skin', 'Rough Skin'),
    ('run-away', 'Run Away'),
    ('sand-force', 'Sand Force'),
    ('sand-rush', 'Sand Rush'),
    ('sand-veil', 'Sand Veil'),
    ('sap-sipper', 'Sap Sipper'),
    ('scrappy', 'Scrappy'),
    ('screen-cleaner', 'Screen Cleaner'),
    ('serene-grace', 'Serene Grace'),
    ('shadow-shield', 'Shadow Shield'),
    ('shadow-tag', 'Shadow Tag'),
    ('shed-skin', 'Shed Skin'),
    ('sheer-force', 'Sheer Force'),
    ('shell-armor', 'Shell Armor'),
    ('shield-dust', 'Shield Dust'),
    ('simple', 'Simple'),
    ('skill-link', 'Skill Link'),
    ('slow-start', 'Slow Start'),
    ('slush-rush', 'Slush Rush'),
    ('sniper', 'Sniper'),
    ('snow-cloak', 'Snow Cloak'),
    ('solar-power', 'Solar Power'),
    ('solid-rock', 'Solid Rock'),
    ('soul-heart', 'Soul-Heart'),
    ('soundproof', 'Soundproof'),
    ('speed-boost', 'Speed Boost'),
    ('stakeout', 'Stakeout'),
    ('stall', 'Stall'),
    ('stalwart', 'Stalwart'),
    ('steam-engine', 'Steam Engine'),
    ('steelworker', 'Steelworker'),
    ('stench', 'Stench'),
    ('sticky-hold', 'Sticky Hold'),
    ('storm-drain', 'Storm Drain'),
    ('sturdy', 'Sturdy'),
    ('suction-cups', 'Suction Cups'),
    ('super-luck', 'Super Luck'),
    ('surge-surfer', 'Surge Surfer'),
    ('swarm', 'Swarm'),
    ('sweet-veil', 'Sweet Veil'),
    ('swift-swim', 'Swift Swim'),
    ('symbiosis', 'Symbiosis'),
    ('synchronize', 'Synchronize'),
    ('tangled-feet', 'Tangled Feet'),
    ('technician', 'Technician'),
    ('telepathy', 'Telepathy'),
    ('teravolt', 'Teravolt'),
    ('thick-fat', 'Thick Fat'),
    ('tinted-lens', 'Tinted Lens'),
    ('torrent', 'Torrent'),
    ('tough-claws', 'Tough Claws'),
    ('turboblaze', 'Turboblaze'),
    ('unaware', 'Unaware'),
    ('unburden', 'Unburden'),
    ('victory-star', 'Victory Star'),
    ('vital-spirit', 'Vital Spirit'),
    ('volt-absorb', 'Volt Absorb'),
    ('water-absorb', 'Water Absorb'),
    ('water-compaction', 'Water Compaction'),
    ('water-veil', 'Water Veil'),
    ('weak-armor', 'Weak Armor'),
    ('white-smoke', 'White Smoke'),
    ('wonder-guard', 'Wonder Guard'),
    ('wonder-skin', 'Wonder Skin'),
    ('zen-mode', 'Zen Mode'),
]

TYPES_CHOICES = [
    ('normal', 'Normal'),
    ('fire', 'Fire'),
    ('water', 'Water'),
    ('electric', 'Electric'),
    ('grass', 'Grass'),
    ('ice', 'Ice'),
    ('fighting', 'Fighting'),
    ('poison', 'Poison'),
    ('ground', 'Ground'),
    ('flying', 'Flying'),
    ('psychic', 'Psychic'),
    ('bug', 'Bug'),
    ('rock', 'Rock'),
    ('ghost', 'Ghost'),
    ('dragon', 'Dragon'),
    ('dark', 'Dark'),
    ('steel', 'Steel'),
    ('fairy', 'Fairy'),
]


class PokemonForm(forms.ModelForm):
    # Campos para habilidades: uno para la habilidad principal y otro para la oculta
    primary_ability = forms.ChoiceField(
        choices=ABILITIES_CHOICES,
        required=True,
        label="Habilidad principal",
        widget=forms.Select
    )
    hidden_ability = forms.ChoiceField(
        choices=ABILITIES_CHOICES,
        required=False,
        label="Habilidad oculta",
        widget=forms.Select
    )
    # Campos para tipos: uno para Tipo 1 y otro para Tipo 2
    primary_type = forms.ChoiceField(
        choices=TYPES_CHOICES,
        required=True,
        label="Tipo 1",
        widget=forms.Select
    )
    secondary_type = forms.ChoiceField(
        choices=TYPES_CHOICES,
        required=False,
        label="Tipo 2",
        widget=forms.Select
    )

    class Meta:
        model = Pokemon
        fields = [
            'name',
            'image',
            'height',
            'weight',
            'base_experience',
            'order',
            'hp',
            'attack',
            'defense',
            'special_attack',
            'special_defense',
            'speed',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Configurar valores iniciales para habilidades:
            abilities = self.instance.abilities if self.instance.abilities else []
            if abilities:
                self.fields['primary_ability'].initial = abilities[0]
            if len(abilities) > 1:
                self.fields['hidden_ability'].initial = abilities[1]
            # Configurar valores iniciales para tipos:
            types = self.instance.types if self.instance.types else []
            if types:
                self.fields['primary_type'].initial = types[0]
            if len(types) > 1:
                self.fields['secondary_type'].initial = types[1]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Pokemon.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("El nombre ya está registrado.")
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Guardamos las habilidades en el campo JSON (como lista de strings)
        abilities = [self.cleaned_data.get('primary_ability')]
        hidden = self.cleaned_data.get('hidden_ability')
        if hidden:
            abilities.append(hidden)
        instance.abilities = abilities

        # Guardamos los tipos en el campo JSON (lista de strings)
        types = [self.cleaned_data.get('primary_type')]
        secondary = self.cleaned_data.get('secondary_type')
        if secondary:
            types.append(secondary)
        instance.types = types

        if commit:
            instance.save()
        return instance
