import wikipediaapi
import json
import time

wiki = wikipediaapi.Wikipedia(
    user_agent='PicaClassifier/1.0 (educational project)',
    language='es'
)

# Semillas expandidas
PICA_SEEDS = [
    # Cuchillos y navajas
    "Cuchillo", "Navaja", "Cuchillo de cocina", "Cuchillo de caza", "Navaja suiza",
    "Cuchillo de combate", "Cuchillo Bowie", "Navaja automática", "Cortaplumas",
    # Espadas y armas blancas
    "Espada", "Katana", "Sable", "Florete", "Estoque", "Alfanje", "Cimitarra",
    "Gladius", "Claymore", "Rapier", "Mandoble", "Montante", "Espada ropera",
    "Wakizashi", "Tanto", "Kodachi", "Ninjato", "Dao", "Jian",
    # Dagas y puñales
    "Daga", "Puñal", "Estilete", "Misericordia (arma)", "Kris", "Kukri",
    # Hachas
    "Hacha", "Hacha de guerra", "Tomahawk", "Francisca", "Hacha danesa",
    # Herramientas cortantes
    "Tijeras", "Bisturí", "Cúter", "Sierra", "Serrucho", "Machete",
    "Guadaña", "Hoz", "Podadera", "Cortacésped", "Motosierra", "Cizalla",
    "Escalpelo", "Lanceta", "Formón", "Cincel", "Buril", "Gubia",
    "Sacabocados", "Punzón", "Lezna", "Berbiquí", "Taladro",
    # Agujas y alfileres
    "Aguja", "Alfiler", "Aguja hipodérmica", "Aguja de coser", "Aguja de tejer",
    "Imperdible", "Chincheta", "Tachuela",
    # Anzuelos y arpones
    "Anzuelo", "Arpón", "Fisga", "Tridente",
    # Lanzas y picas
    "Lanza", "Pica", "Jabalina", "Alabarda", "Partesana", "Guja", "Venablo",
    "Pilum", "Sarissa", "Naginata", "Yari",
    # Flechas y proyectiles
    "Flecha", "Dardo", "Virote", "Saeta", "Shuriken", "Kunai",
    # Vidrio y cristal
    "Vidrio", "Cristal", "Espejo", "Vidrio templado", "Vidrio laminado",
    "Fibra de vidrio", "Vitral", "Botella de vidrio",
    # Cactus y suculentas espinosas
    "Cactus", "Nopal", "Opuntia", "Saguaro", "Cardón", "Biznaga",
    "Echinocactus", "Ferocactus", "Mammillaria", "Cereus", "Peyote",
    "Agave", "Maguey", "Yuca", "Aloe vera",
    # Plantas espinosas
    "Rosa", "Rosal", "Zarza", "Zarzamora", "Frambuesa", "Espino",
    "Espino blanco", "Espino negro", "Acacia", "Robinia", "Gleditsia",
    "Bougainvillea", "Berberis", "Pyracantha", "Cardón", "Cardo",
    "Ortiga", "Pringamoza",
    # Chiles y picantes
    "Chile", "Capsicum", "Jalapeño", "Habanero", "Serrano", "Poblano",
    "Chipotle", "Cayena", "Chile de árbol", "Chile guajillo", "Chile ancho",
    "Chile pasilla", "Chile morita", "Chile cascabel", "Pimiento morrón",
    "Carolina Reaper", "Trinidad Scorpion", "Ghost pepper", "Bhut jolokia",
    "Pimienta", "Pimienta negra", "Pimienta de cayena", "Pimienta rosa",
    "Capsaicina", "Escala Scoville",
    # Otros picantes
    "Wasabi", "Mostaza", "Rábano picante", "Jengibre", "Galanga",
    "Salsa picante", "Tabasco", "Sriracha", "Harissa", "Sambal",
    "Curry", "Gochujang", "Kimchi",
    # Insectos que pican
    "Abeja", "Avispa", "Avispón", "Abejorro", "Abeja africana",
    "Hormiga", "Hormiga roja", "Hormiga bala", "Hormiga de fuego",
    "Mosquito", "Aedes aegypti", "Anopheles", "Tábano", "Mosca negra",
    "Pulga", "Chinche", "Garrapata", "Ácaro", "Nigua",
    # Arácnidos venenosos
    "Escorpión", "Alacrán", "Araña", "Viuda negra", "Araña reclusa parda",
    "Tarántula", "Araña de rincón", "Araña lobo",
    # Animales marinos que pican
    "Medusa", "Carabela portuguesa", "Anémona de mar", "Erizo de mar",
    "Mantarraya", "Pez piedra", "Pez león", "Pez escorpión", "Raya",
    "Coral de fuego", "Estrella corona de espinas",
    # Serpientes venenosas
    "Serpiente venenosa", "Víbora", "Cobra", "Mamba negra", "Taipán",
    "Serpiente de cascabel", "Crótalo", "Nauyaca", "Coralillo", "Cobra real",
    # Otros animales peligrosos
    "Ciempiés", "Escolopendra", "Oruga venenosa", "Pez globo",
    "Ornitorrinco", "Musaraña",
    # Clavos y tornillos
    "Clavo", "Tornillo", "Perno", "Remache", "Grapa", "Clavo de acero",
    # Alambre
    "Alambre", "Alambre de púas", "Concertina", "Alambre espino",
    # Otros objetos punzantes
    "Astilla", "Pincho", "Púa", "Espina", "Gancho", "Garfio",
    "Tenedor", "Trinche", "Brocheta", "Pincho moruno",
    "Compás", "Transportador con punta",
    # Herramientas eléctricas
    "Amoladora", "Esmeril", "Dremel", "Lijadora",
    # Material médico
    "Jeringa", "Catéter", "Lanceta", "Sutura",
]

NO_PICA_SEEDS = [
    # Textiles y telas
    "Almohada", "Cojín", "Colchón", "Edredón", "Cobija", "Manta", "Sábana",
    "Algodón", "Lana", "Seda", "Terciopelo", "Felpa", "Franela", "Polar",
    "Satén", "Raso", "Lino", "Cachemir", "Angora", "Mohair", "Chenilla",
    "Peluche", "Muñeco de peluche", "Osito de peluche",
    # Ropa suave
    "Pijama", "Bata", "Calcetín", "Guante", "Bufanda", "Gorro de lana",
    # Pan y derivados
    "Pan", "Pan blanco", "Pan de molde", "Pan dulce", "Brioche", "Croissant",
    "Panqué", "Bizcocho", "Magdalena", "Muffin", "Donut", "Churro",
    "Tortilla de harina", "Tortilla de maíz", "Arepa", "Pupusa",
    # Cereales y granos
    "Arroz", "Arroz blanco", "Arroz integral", "Avena", "Cebada", "Trigo",
    "Maíz", "Quinoa", "Polenta", "Cuscús", "Bulgur",
    # Pasta
    "Pasta", "Espagueti", "Macarrón", "Lasaña", "Ravioli", "Ñoquis",
    "Fideo", "Tallarín", "Penne", "Fusilli",
    # Purés y cremas
    "Puré", "Puré de papa", "Hummus", "Guacamole", "Babaganoush",
    # Lácteos
    "Leche", "Yogur", "Queso crema", "Requesón", "Ricota", "Mascarpone",
    "Mantequilla", "Crema", "Nata", "Helado", "Natilla", "Flan",
    # Dulces suaves
    "Miel", "Mermelada", "Jalea", "Caramelo", "Chocolate", "Nutella",
    "Malvavisco", "Algodón de azúcar", "Gelatina", "Pudín", "Mousse",
    # Frutas suaves
    "Plátano", "Banana", "Mango", "Papaya", "Sandía", "Melón",
    "Durazno", "Melocotón", "Ciruela", "Higo", "Kiwi", "Aguacate",
    "Frambuesa", "Mora", "Arándano", "Fresa", "Cereza", "Uva",
    "Manzana", "Pera", "Naranja", "Mandarina", "Toronja",
    # Verduras suaves
    "Tomate", "Pepino", "Calabaza", "Calabacín", "Berenjena", "Champiñón",
    "Papa", "Camote", "Zanahoria cocida", "Chícharo", "Elote",
    # Naturaleza suave
    "Nube", "Niebla", "Neblina", "Bruma", "Rocío",
    "Agua", "Lluvia", "Río", "Lago", "Mar", "Océano",
    "Espuma", "Burbuja", "Pompas de jabón",
    "Arena", "Arena fina", "Limo", "Arcilla",
    "Hierba", "Césped", "Pasto", "Musgo", "Liquen",
    "Hoja", "Pétalo", "Flor", "Margarita", "Tulipán", "Lirio",
    "Pluma", "Plumón", "Pelusa",
    # Objetos suaves cotidianos
    "Esponja", "Esponja de baño", "Estropajo suave",
    "Globo", "Pelota de playa", "Balón",
    "Plastilina", "Masa", "Slime", "Play-Doh",
    "Jabón", "Gel", "Champú", "Acondicionador",
    "Crema corporal", "Loción", "Aceite corporal",
    "Papel", "Papel higiénico", "Servilleta", "Pañuelo",
    "Tela", "Trapo", "Toalla", "Paño",
    "Goma", "Caucho", "Silicona", "Látex",
    "Corcho", "Poliestireno", "Espuma de poliuretano",
    # Animales tiernos/inofensivos
    "Conejo", "Hámster", "Cobaya", "Chinchilla", "Jerbo",
    "Oveja", "Cordero", "Cabra", "Llama", "Alpaca",
    "Vaca", "Ternero", "Cerdo", "Lechón",
    "Mariposa", "Polilla", "Libélula", "Luciérnaga", "Catarina",
    "Caracol", "Babosa", "Lombriz", "Gusano de seda",
    "Pez dorado", "Pez betta", "Guppy", "Pez payaso",
    "Tortuga", "Tortuga marina", "Galápago",
    "Koala", "Panda", "Oso perezoso", "Manatí", "Dugongo",
    "Delfín", "Ballena", "Foca", "Nutria", "Castor",
    "Pingüino", "Pato", "Ganso", "Cisne", "Flamenco",
    "Paloma", "Gorrión", "Canario", "Periquito", "Colibrí",
    # Nubes y cielo
    "Cirro", "Cúmulo", "Estrato", "Nimbo", "Cumulonimbo",
    "Arcoíris", "Aurora boreal", "Atardecer", "Amanecer",
    # Instrumentos suaves
    "Tambor", "Bongó", "Maracas", "Pandereta",
    # Juguetes
    "Muñeca", "Títere", "Marioneta", "Oso de felpa",
    # Muebles acolchados
    "Sofá", "Sillón", "Puf", "Hamaca",
]

# Categorías de Wikipedia para expandir (extraerá artículos de estas categorías)
PICA_CATEGORIES = [
    "Cuchillos", "Espadas", "Armas blancas", "Armas de asta", "Herramientas de corte",
    "Cactaceae", "Cactus", "Capsicum", "Chiles", "Apidae", "Abejas", "Vespidae",
    "Avispas", "Scorpiones", "Escorpiones", "Serpientes venenosas", "Viperidae",
    "Elapidae", "Medusozoa", "Medusas", "Cnidaria", "Araneae", "Arañas",
    "Herramientas manuales", "Sierras", "Plantas espinosas",
]

NO_PICA_CATEGORIES = [
    "Textiles", "Telas", "Pan", "Panes", "Pastas alimenticias", "Lácteos",
    "Quesos", "Frutas", "Verduras", "Leporidae", "Conejos", "Roedores",
    "Mascotas", "Delphinidae", "Delfines", "Ballenas", "Pinnípedos",
    "Nubes", "Flores", "Plantas ornamentales", "Dulces", "Postres",
]


def get_article_text(title):
    """Obtiene el texto de un artículo de Wikipedia"""
    try:
        page = wiki.page(title)
        if page.exists():
            text = page.summary
            if len(text) > 50:
                return text
    except Exception as e:
        print(f"    Error con '{title}': {e}")
    return None


def get_links_from_article(title, max_links=30):
    """Obtiene enlaces internos de un artículo (artículos relacionados)"""
    try:
        page = wiki.page(title)
        if page.exists():
            links = list(page.links.keys())[:max_links]
            return [l for l in links if
                    not l.startswith(("Wikipedia:", "Categoría:", "Archivo:", "Plantilla:", "Ayuda:", "Portal:"))]
    except:
        pass
    return []


def get_category_members(category_name, max_items=100):
    """Obtiene artículos de una categoría de Wikipedia"""
    try:
        cat = wiki.page(f"Categoría:{category_name}")
        members = []
        if cat.exists():
            for title, page in cat.categorymembers.items():
                if len(members) >= max_items:
                    break
                if not title.startswith("Categoría:"):
                    members.append(title)
        return members
    except Exception as e:
        print(f"  Error en categoría '{category_name}': {e}")
    return []


def scrape_data(target_per_class=2500):
    data = {"text": [], "label": []}
    seen_titles = set()

    pica_count = 0
    no_pica_count = 0

    # ========== CLASE PICA (label=1) ==========
    print("=" * 50)
    print("EXTRAYENDO ARTÍCULOS QUE PICAN...")
    print("=" * 50)

    # 1. Semillas directas
    print("\n[1/3] Procesando semillas directas...")
    for seed in PICA_SEEDS:
        if pica_count >= target_per_class:
            break
        text = get_article_text(seed)
        if text and seed not in seen_titles:
            data["text"].append(text)
            data["label"].append(1)
            seen_titles.add(seed)
            pica_count += 1
            print(f"  ✓ {seed} ({pica_count})")
        time.sleep(0.05)

    # 2. Enlaces de artículos semilla
    print(f"\n[2/3] Extrayendo artículos enlazados... (actual: {pica_count})")
    for seed in PICA_SEEDS[:50]:  # Primeras 50 semillas
        if pica_count >= target_per_class:
            break
        links = get_links_from_article(seed, max_links=20)
        for link in links:
            if pica_count >= target_per_class:
                break
            if link not in seen_titles:
                text = get_article_text(link)
                if text:
                    data["text"].append(text)
                    data["label"].append(1)
                    seen_titles.add(link)
                    pica_count += 1
                    print(f"  ✓ {link} (desde {seed}) ({pica_count})")
                time.sleep(0.05)

    # 3. Categorías de Wikipedia
    print(f"\n[3/3] Extrayendo de categorías... (actual: {pica_count})")
    for cat in PICA_CATEGORIES:
        if pica_count >= target_per_class:
            break
        print(f"  Categoría: {cat}")
        members = get_category_members(cat, max_items=100)
        for member in members:
            if pica_count >= target_per_class:
                break
            if member not in seen_titles:
                text = get_article_text(member)
                if text:
                    data["text"].append(text)
                    data["label"].append(1)
                    seen_titles.add(member)
                    pica_count += 1
                    print(f"    ✓ {member} ({pica_count})")
                time.sleep(0.05)

    print(f"\n>>> Total PICA: {pica_count}")

    # ========== CLASE NO PICA (label=0) ==========
    print("\n" + "=" * 50)
    print("EXTRAYENDO ARTÍCULOS QUE NO PICAN...")
    print("=" * 50)

    # 1. Semillas directas
    print("\n[1/3] Procesando semillas directas...")
    for seed in NO_PICA_SEEDS:
        if no_pica_count >= target_per_class:
            break
        text = get_article_text(seed)
        if text and seed not in seen_titles:
            data["text"].append(text)
            data["label"].append(0)
            seen_titles.add(seed)
            no_pica_count += 1
            print(f"  ✓ {seed} ({no_pica_count})")
        time.sleep(0.05)

    # 2. Enlaces de artículos semilla
    print(f"\n[2/3] Extrayendo artículos enlazados... (actual: {no_pica_count})")
    for seed in NO_PICA_SEEDS[:50]:
        if no_pica_count >= target_per_class:
            break
        links = get_links_from_article(seed, max_links=20)
        for link in links:
            if no_pica_count >= target_per_class:
                break
            if link not in seen_titles:
                text = get_article_text(link)
                if text:
                    data["text"].append(text)
                    data["label"].append(0)
                    seen_titles.add(link)
                    no_pica_count += 1
                    print(f"  ✓ {link} (desde {seed}) ({no_pica_count})")
                time.sleep(0.05)

    # 3. Categorías de Wikipedia
    print(f"\n[3/3] Extrayendo de categorías... (actual: {no_pica_count})")
    for cat in NO_PICA_CATEGORIES:
        if no_pica_count >= target_per_class:
            break
        print(f"  Categoría: {cat}")
        members = get_category_members(cat, max_items=100)
        for member in members:
            if no_pica_count >= target_per_class:
                break
            if member not in seen_titles:
                text = get_article_text(member)
                if text:
                    data["text"].append(text)
                    data["label"].append(0)
                    seen_titles.add(member)
                    no_pica_count += 1
                    print(f"    ✓ {member} ({no_pica_count})")
                time.sleep(0.05)

    # ========== RESUMEN ==========
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    print(f"Total PICA (label=1): {pica_count}")
    print(f"Total NO PICA (label=0): {no_pica_count}")
    print(f"Total ejemplos: {len(data['label'])}")

    # Guardar
    with open("dataset_pica.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Guardado en dataset_pica.json")

    # Estadísticas adicionales
    avg_len = sum(len(t) for t in data["text"]) / len(data["text"])
    print(f"Longitud promedio de texto: {avg_len:.0f} caracteres")

    return data


if __name__ == "__main__":
    # Cambia target_per_class para obtener más o menos ejemplos
    # 2500 por clase = 5000 total
    scrape_data(target_per_class=2500)