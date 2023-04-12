import os
from tqdm import tqdm
print('start')

dir_in = 'ascs'
dir_out = 'out'

for fichier in tqdm(os.listdir(dir_in)):
    nom_fichier = fichier.split('.')[0]
    os.system(f'"gdal_translate.exe" -a_srs EPSG:2154 -co TILED=YES -co COMPRESS=LZW -co PREDICTOR=3 {dir_in}/{nom_fichier}.asc {dir_out}/{nom_fichier}.tif')

fichiers = ''
for fichier in tqdm(os.listdir(dir_out)):
    fichiers += f'{dir_out}/{fichier}\n'
    with open('vrt_list.txt', 'w') as writer:
        writer.write(fichiers)

os.system('"gdalbuildvrt.exe" -input_file_list vrt_list.txt Out.vrt')