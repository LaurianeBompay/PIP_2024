################################################################################
################################################################################
# PREPARATION DES CHEMINS VERS SHAPEFILES
from os import listdir, walk
from os.path import isfile, join

# CHEMINS SHAPEFILES BD-TOPO
Chemin_Donnees_BDTOPO : str = "C:\\Users\\dmitr\\Documents\\M2_SID\\PIP\\BDTOPO\\"

# on récupère la liste des dossiers
Domaines = [f for f in listdir(Chemin_Donnees_BDTOPO) if not isfile(join(Chemin_Donnees_BDTOPO, f))]
# on récupère tous les fichiers des tables par domaine
BDTOPO = {}
for dom in Domaines:
  SHP_files = {f.split('.')[0]:f for f in listdir(Chemin_Donnees_BDTOPO+dom) if f.endswith('.shp')}
  BDTOPO[dom]=SHP_files

def nom_f(domaine:str, table:str):
  """
  BUT: renvoie le chemin absolu du fichier .shp d'un domaine et table donnés
  IN:  -domaine: domaine de la BD TOPO
       -table: table de la BD TOPO
       DataPath est une constante globale
  """
  fichier_table =  BDTOPO[domaine][table]
  return Chemin_Donnees_BDTOPO + domaine + '/' + fichier_table
  
# CHEMINS GeoJson BD-POMPIERS
Chemin_Donnees_BD_Pompiers : str = "C:\\Users\\dmitr\\Documents\\M2_SID\\PIP\\Data_pip_2024\\"
def get_geojson_files(folder_path):
  """
  BUT: Renvoi le nom de tous les fichiers GeoJson stockés dans un dosier 'folder_path' et ses dossiers enfants
  """
  geojson_files = []
  for root, dirs, files in walk(folder_path):
    for fichier in files:
      
      if fichier.endswith(".geojson"):
        print(fichier)
        geojson_files.append(join(root, fichier))
  return geojson_files
print("Liste des fichiers GeoJson BD POMPIERS:", get_geojson_files(Chemin_Donnees_BD_Pompiers))

# FIN DE LA PREPARATION DES CHEMINS VERS SHAPEFILES
################################################################################
################################################################################
# FONCTIONS UTILS QGIS
from qgis.core import *
#from qgis.PyQt.QtCore import *
#from qgis.PyQt.QtGui import *
#from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QColor



def ajouter_couches_a_interface(couches_dict: dict):
    for nom, info in couches_dict.items():
        chemin = info['chemin']
        couleur = info['couleur']

        couche_vecteur = QgsVectorLayer(chemin, nom, 'ogr')

        if not couche_vecteur.isValid():
            print(f"La couche chargée depuis {chemin} n'est pas valide.")
        else:
            # Setup de la couleur de symbologie
            #color = QColor.fromRgbF(*couleur)
            # test 1
            color = QgsColorRamp()
            color.setColorRampType(QgsColorRamp.Interpolated)
            color.setColor1(QColor('transparent'))
            color.setColor2(QColor(couleur))
            
            #color = QColor(couleur)
            symbol = QgsSymbol.defaultSymbol(couche_vecteur.geometryType())
            #symbol.setColor(color)
            symbol.setColorRamp(color)

            # Applique la symbologie à la couche
            renderer = QgsSingleSymbolRenderer(symbol)
            couche_vecteur.setRenderer(renderer)
            
            # Ajout de la couche à l'interface graphique
            iface.addVectorLayer(chemin, nom, 'ogr')
            print(f"La couche {nom} a été ajoutée avec succès à l'interface avec la couleur {couleur}.")








def ajouter_points_sur_carte(points, nom_couche="CouchePoints"):
    try:
        # Créer une couche mémoire pour les points
        couche = QgsVectorLayer("Point?crs=EPSG:2154", nom_couche, "memory")
        fournisseur = couche.dataProvider()

        # Définir les attributs de la couche de points (facultatif)
        # pr = couche.dataProvider()
        # pr.addAttributes([])  # Ajouter des attributs si nécessaire
        # couche.updateFields()

        # Ajouter les points à la couche
        for lat, lon in points:
            point = QgsPoint(lon, lat)
            point_geometry = QgsGeometry.fromPoint(point)
            entite = QgsFeature()
            entite.setGeometry(point_geometry)
            fournisseur.addFeature(entite)

        # Mettre à jour l'étendue de la couche et l'ajouter à la carte
        couche.updateExtents()
        QgsProject.instance().addMapLayer(couche)

        # Créer un symbole (par exemple, un point jaune)
        symbol = QgsSymbol.defaultSymbol(couche.geometryType())
        symbol.setColor(QColor(255, 255, 0))  # Jaune

        # Définir le rendu pour la couche
        rendu = QgsSingleSymbolRenderer(symbol)
        couche.setRenderer(rendu)

        # Rafraîchir la carte pour afficher les changements
        iface.mapCanvas().refreshAllLayers()
    except Exception as e:
        # Gérer l'erreur, par exemple, afficher un message d'erreur dans la barre de messages QGIS
        iface.messageBar().pushMessage("Erreur", str(e), level=Qgis.Critical)


################################################################################
################################################################################
# DICO RGB PALETTE DE COULEUR
RGB = {
    "crimson": [0.8627450980392157, 0.0784313725490196, 0.23529411764705882],
    "dodgerblue": [0.11764705882352941, 0.5647058823529412, 1.0],
    "limegreen": [0.19607843137254902, 0.803921568627451, 0.19607843137254902],
    "gold": [1.0, 0.8431372549019608, 0.0],
    "violet": [0.9333333333333333, 0.5098039215686274, 0.9333333333333333],
    "darkgray": [0.6627450980392157, 0.6627450980392157, 0.6627450980392157],
    "darksalmon": [0.9137254901960784, 0.5882352941176471, 0.47843137254901963],
    "mediumturquoise": [0.2823529411764706, 0.8196078431372549, 0.8],
    "olive": [0.5019607843137255, 0.5019607843137255, 0.0],
    "saddlebrown": [0.5450980392156862, 0.27058823529411763, 0.07450980392156863],
    "darkorchid": [0.6, 0.19607843137254902, 0.8],
    "darkslategray": [0.1843137254901961, 0.30980392156862746, 0.30980392156862746],
    "ROUGE": [1.0, 0.0, 0.0],
    "TEST": [225,89,137,255]
}

