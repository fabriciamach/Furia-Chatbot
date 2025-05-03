MAP_TRANSLATION = {
    "de_anubis": "Anubis",
    "de_inferno": "Inferno",
    "de_mirage": "Mirage",
    "de_nuke": "Nuke",
    "de_overpass": "Overpass",
    "de_ancient": "Ancient",
    "de_vertigo": "Vertigo",
    "de_dust2": "Dust 2",
    "de_train": "Train",
    "de_cache": "Cache",
    "de_cbble": "Cobblestone",
    "de_tuscan": "Tuscan",
    "de_season": "Season"
}

def translate_map(map_name: str) -> str:
    return MAP_TRANSLATION.get(map_name, map_name)