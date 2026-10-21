import requests
from django.utils import timezone

def download_cardmarket_pokemon_product_cards():
    response = requests.get("https://downloads.s3.cardmarket.com/productCatalog/productList/products_singles_6.json", timeout=60)
    response.raise_for_status()

    return response

def download_cardmarket_pokemon_product_sealed():
    response = requests.get("https://downloads.s3.cardmarket.com/productCatalog/productList/products_nonsingles_6.json", timeout=60)
    response.raise_for_status()

    return response


def download_cardmarket_pokemon_price():
    response = requests.get("https://downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json", timeout=60)
    response.raise_for_status()

    return response

def clear_products_data_from_cardmarket():

    pokemon_products = download_cardmarket_pokemon_product_sealed
    pokemon_prices = download_cardmarket_pokemon_price

    data_clear = f"data_{timezone.localdate().strftime('%Y_%m_%d')}"

    for product in pokemon_products["products"]:    
        data_clear[product["name"]] = {}


import json
from pathlib import Path


def charger_catalogue_cardmarket():

    product = download_cardmarket_pokemon_product_sealed()
    produits = product.json()["products"]

    price = download_cardmarket_pokemon_price()
    prix = price.json()["priceGuides"]

    # Indexer les prix par ID Cardmarket
    prix_par_id = {
        item["idProduct"]: item
        for item in prix
    }

    catalogue = {}

    for produit in produits:
        nom = produit["name"]
        id_product = produit["idProduct"]

        # Sécurité : ne jamais écraser un nom identique
        if nom not in catalogue: 
            catalogue[nom] = {
                "idCardmarket": id_product,
                "infos": produit,
                "prix": prix_par_id.get(id_product),
            }


    fichier_sortie = "catalogue_cardmarket_test.json"

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(catalogue, f, indent=4, ensure_ascii=False)

    print(f"Catalogue sauvegardé : {fichier_sortie}")
    print(f"Nombre de produits : {len(catalogue)}")

    return catalogue
