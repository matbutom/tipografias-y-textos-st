import easyocr
import cv2
import os
from pathlib import Path

# Directorios de entrada y salida
input_dir = Path('assets/tipografias/tipografias-display')
output_dir = Path('recortes-tipografias-display')
os.makedirs(output_dir, exist_ok=True)

# Inicializa el lector (español e inglés, sin GPU)
reader = easyocr.Reader(['es', 'en'], gpu=False)

# Extensiones de imagen aceptadas
extensiones = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}

# Recorre todas las imágenes en input_dir (incluyendo subcarpetas)
for image_path in input_dir.rglob('*'):
    if image_path.suffix.lower() not in extensiones:
        continue  # Ignora archivos no soportados

    print(f'Procesando {image_path}...')
    imagen = cv2.imread(str(image_path))
    if imagen is None:
        print(f'No se pudo leer {image_path}')
        continue

    result = reader.readtext(str(image_path))
    for i, (bbox, texto, conf) in enumerate(result):
        # Calcula coordenadas de recorte
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        x_min, x_max = int(min(xs)), int(max(xs))
        y_min, y_max = int(min(ys)), int(max(ys))
        crop = imagen[y_min:y_max, x_min:x_max]

        # Nombre del archivo de salida: nombre_imagen_crop_i.jpg
        out_name = output_dir / f'{image_path.stem}_crop_{i}.jpg'
        cv2.imwrite(str(out_name), crop)

        print(f'  - Guardado: {out_name}')
