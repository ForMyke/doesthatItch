import os
from PIL import Image
from tqdm import tqdm

NOPICA_PATH = "images/nopica"
LINE_WIDTH = 5
LINE_COLOR = (26, 26, 26)


def add_line(input_path, output_path):
    try:
        img = Image.open(input_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        w, h = img.size
        final = Image.new('RGB', (w + LINE_WIDTH, h), LINE_COLOR)
        final.paste(img, (LINE_WIDTH, 0))
        final.save(output_path)
        return True
    except Exception:
        return False


def main():
    files = [f for f in os.listdir(NOPICA_PATH) if os.path.isfile(os.path.join(NOPICA_PATH, f))]

    print(f"Procesando {len(files)} imágenes en {NOPICA_PATH}...")

    for filename in tqdm(files, unit="img"):
        path = os.path.join(NOPICA_PATH, filename)
        add_line(path, path)

    print("✓ Listo")


if __name__ == "__main__":
    main()