# Importation
# fichier script python de définitions de fonctions utiles
import QgisUtils 

print(RGB['crimson'])

# LES COUCHES A AFFICHER
# la fonction nom_f renvoie le nom du fichier .shp d'une table de la BD-TOPO (définie ds QgisUtils.py)
# Les couches à afficher sont rangées dans un dictionnaire
# La clé est le nom que l'on donne à la couche à afficher
# Les 2 valeurs associées sont le chemin vers le fichier couche et la couleur d'affichage
# L'ordre des couches est importante (elles se superposent au fur et à mesure)
Couches = {
            'SURFACE_HYDROGRAPHIQUE': {'couleur': 'green', 'chemin':nom_f('HYDROGRAPHIE', 'SURFACE_HYDROGRAPHIQUE')},
            'PEI':                    {'couleur': 'green', 'chemin':'C:\\Users\\dmitr\\Documents\\M2_SID\\PIP\\Data_pip_2024\\pei\\pei_20231025.geojson'},
            'COURS_D_EAU':            {'couleur': 'green', 'chemin':nom_f('HYDROGRAPHIE', 'COURS_D_EAU')}

}

# Appelle de la fonction définie dans le fichier QgisUtils.py
ajouter_couches_a_interface(Couches)