# EleCor
Serveur qui permet de faire des requetes d'altitudes. Sur des bases de données GeoTiff.

## .asc > .tif
Avec Gdal.</br>
Mettre tout les .asc dans `ascs`.</br>
S'assurer de la présence de gdal_translate et de gdalbuildvrt.</br>
Lancer `asc_to_tif.py`</br>

## Serveur
Lancer `serv_alti.py`.
Pour obtenir une suite d'altitudes, il faut faire une requete vers /alti/ avec coords=lat,lon{separator}lat,lon{separator}lat,lon</br>
**Exemple:**
```
/alti/coords=0.0,12.5;80.0002,2.001
```
### Réponse </br>
Elevation en mètres.
 > Xml avec des balises \<elevation\>
```
<reponse>
<elevation>2121.0</elevation>
<elevation>21.0</elevation>
<elevation>121.0</elevation>
...
</reponse>
```
Le serveur est conçu pour fonctionner avec l'application [OruxMap](https://oruxmaps.com/cs/en/).
## Correction d'altitude dans OruxMap
Dans `Service d'altitude en ligne`:
> Coordonnées pour requêtes : autant que possible </br>
> Motif Url : `{Url du serv}/alti/coords=${coords}`</br>
> Séparateur des coordonnées : `;`</br>
> Element à chercher : `elevation`
