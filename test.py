def map_values(mapping, x):
    return mapping.get(x)

# Exemple de dictionnaire de mappage
marque_mapping = {
    "Toyota": 1,
    "Honda": 2,
    "Ford": 3
}

# Utilisation de la fonction
print(map_values(marque_mapping, 'Ford'))  # Sortie: 1
print(map_values(marque_mapping, "BMW"))     # Sortie: None
