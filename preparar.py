import os
import glob
from PIL import Image
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import sys

# ============================================
# CONFIGURACIÓN
# ============================================

SOURCE_PICA_PATH = "./images/pica"
SOURCE_NOPICA_PATH = "./images/nopica"

OUTPUT_DIR = "dataset"
TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "validation")

TRAIN_PICA_DIR = os.path.join(TRAIN_DIR, "pica")
TRAIN_NOPICA_DIR = os.path.join(TRAIN_DIR, "nopica")
VAL_PICA_DIR = os.path.join(VAL_DIR, "pica")
VAL_NOPICA_DIR = os.path.join(VAL_DIR, "nopica")

VAL_SPLIT = 0.2
RANDOM_STATE = 42
TARGET_SIZE = (224, 224)


# ============================================
# FUNCIÓN DE PROCESAMIENTO
# ============================================

def process_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim

        img_cropped = img.crop((left, top, right, bottom))
        img_resized = img_cropped.resize(TARGET_SIZE, Image.LANCZOS)

        if img_resized.mode != 'RGB':
            img_resized = img_resized.convert('RGB')

        img_resized.save(output_path, format='PNG')
        return True
    except Exception:
        return False


def process_and_copy(source_files, dest_folder, prefix):
    print(f"\n📋 Procesando {len(source_files)} imágenes para: {dest_folder}")
    success_count = 0

    for i, src_path in enumerate(tqdm(source_files, unit="img", ncols=100)):
        dest_filename = f"{prefix}_{i:05d}.png"
        dest_path = os.path.join(dest_folder, dest_filename)

        if process_image(src_path, dest_path):
            success_count += 1

    print(f"✓ {success_count}/{len(source_files)} imágenes procesadas.")


# ============================================
# SCRIPT PRINCIPAL
# ============================================
def main():
    print("Iniciando preparación de datos...")

    print("\n📁 Creando estructura de carpetas...")
    for folder in [TRAIN_PICA_DIR, TRAIN_NOPICA_DIR, VAL_PICA_DIR, VAL_NOPICA_DIR]:
        os.makedirs(folder, exist_ok=True)
    print(f"✓ Estructura creada en '{OUTPUT_DIR}'")

    print("\n🔍 Buscando imágenes...")

    pica_files = glob.glob(os.path.join(SOURCE_PICA_PATH, "*.*"))
    nopica_files = glob.glob(os.path.join(SOURCE_NOPICA_PATH, "*.*"))

    if not pica_files:
        print(f"ERROR: No se encontraron imágenes en: {SOURCE_PICA_PATH}")
        sys.exit()
    if not nopica_files:
        print(f"ERROR: No se encontraron imágenes en: {SOURCE_NOPICA_PATH}")
        sys.exit()

    print(f"✓ Pica: {len(pica_files)}")
    print(f"✓ No pica: {len(nopica_files)}")

    print("\n📊 Dividiendo dataset...")
    pica_train, pica_val = train_test_split(pica_files, test_size=VAL_SPLIT, random_state=RANDOM_STATE)
    nopica_train, nopica_val = train_test_split(nopica_files, test_size=VAL_SPLIT, random_state=RANDOM_STATE)

    print(f"  Train - Pica: {len(pica_train)}, No pica: {len(nopica_train)}")
    print(f"  Val   - Pica: {len(pica_val)}, No pica: {len(nopica_val)}")

    print("\n🚀 Procesando imágenes...")

    process_and_copy(pica_train, TRAIN_PICA_DIR, "pica")
    process_and_copy(pica_val, VAL_PICA_DIR, "pica")
    process_and_copy(nopica_train, TRAIN_NOPICA_DIR, "nopica")
    process_and_copy(nopica_val, VAL_NOPICA_DIR, "nopica")

    print("\n" + "=" * 50)
    print("✨ COMPLETADO ✨")
    print("=" * 50)
    print(f"\n📂 {TRAIN_DIR}/")
    print(f"   ├── pica/ ({len(os.listdir(TRAIN_PICA_DIR))} imgs)")
    print(f"   └── nopica/ ({len(os.listdir(TRAIN_NOPICA_DIR))} imgs)")
    print(f"\n📂 {VAL_DIR}/")
    print(f"   ├── pica/ ({len(os.listdir(VAL_PICA_DIR))} imgs)")
    print(f"   └── nopica/ ({len(os.listdir(VAL_NOPICA_DIR))} imgs)")


if __name__ == "__main__":
    main()