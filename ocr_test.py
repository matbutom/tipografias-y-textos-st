import easyocr
import cv2
import os

# Configura idioma (español, inglés) y desactiva la GPU porque en macOS no suele estar soportada por defecto
reader = easyocr.Reader(['es', 'en'], gpu=False)

# Ruta de la imagen
image_path = 'assets/tipografias/tipografias-sans-serif/1-1-5.jpeg'  # coloca aquí tu imagen dentro del repo

# Ejecuta OCR
result = reader.readtext(image_path)

# Imprime resultados
for bbox, texto, conf in result:
    print(f'Texto: {texto} (confianza: {conf:.2f})')

# Crea carpeta para recortes
os.makedirs('recortes', exist_ok=True)

# Carga la imagen con OpenCV
imagen = cv2.imread(image_path)

# Recorta cada bloque de texto y guarda el archivo
for i, (bbox, texto, _) in enumerate(result):
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    x_min, x_max = int(min(xs)), int(max(xs))
    y_min, y_max = int(min(ys)), int(max(ys))
    crop = imagen[y_min:y_max, x_min:x_max]
    cv2.imwrite(f'recortes/crop_{i}.jpg', crop)
