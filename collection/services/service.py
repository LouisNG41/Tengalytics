
from django.utils import timezone
import pandas as pd
from collection.models import Product, PriceSnapshot
from collection.services.cardmarket_service import download_cardmarket_pokemon_price, download_cardmarket_pokemon_product_cards, download_cardmarket_pokemon_product_sealed
import logging
from django.db import IntegrityError, transaction

logger = logging.getLogger(__name__)


def get_or_create_product(produit, catalogue_produit_cm):
    """
    Récupère un produit existant ou crée un nouveau produit.

    Returns:
        tuple: (produit, cree)
            - produit : instance du modèle Produit
            - cree : True si créé, False s'il existait déjà
    """
    nom = produit['Nom'].strip()

    if not nom:
        raise ValueError("Le nom du produit ne peut pas être vide.")

    try:
        produit = Product.objects.filter(nom=nom).first()

        if produit is not None:
            logger.info("Produit déjà existant : %s", nom)
            return produit, False

        with transaction.atomic():
            produit = Product.objects.create(nom=nom,
                                             tcg = produit["TCG"],
                                             cardmarket_id= catalogue_produit_cm["idCardmarket"],
                                             category = catalogue_produit_cm['Infos']['categoryName'],
                                             serie = produit['Serie'])

        logger.info("Produit créé : %s", nom)
        return produit, True

    except IntegrityError:
        # Un autre processus a pu créer le produit simultanément.
        produit = Product.objects.filter(nom=nom).first()

        if produit is not None:
            logger.info("Produit créé simultanément par un autre processus : %s", nom)
            return produit, False

        raise

def register_price(product: Product, price_data: dict) -> PriceSnapshot:
    """Ajoute le relevé du jour à l'historique du produit."""

    historique, _ = PriceSnapshot.objects.get_or_create(
        product=product
    )

    date_releve = timezone.localdate().isoformat()

    historique.prices[date_releve] = {
        "avg": price_data.get("avg"),
        "low": price_data.get("low"),
        "trend": price_data.get("trend"),
        "avg7": price_data.get("avg7"),
        "avg30": price_data.get("avg30"),
    }

    historique.save()

    return historique

def read_stock(chemin):
    """Lit le fichier Excel et retourne les données."""

    df = pd.read_excel(chemin)

    # Nettoyer les noms des colonnes
    df.columns = df.columns.str.strip()

    # Vérifier les colonnes attendues
    colonnes_attendues = [
        "Nom_item",
        "Id_purchase",
        "TCG",
        "Date_achat",
        "Prix_achat",
        "Quantite",
        "Type"
    ]

    colonnes_manquantes = [
        colonne for colonne in colonnes_attendues
        if colonne not in df.columns
    ]

    if colonnes_manquantes:
        raise ValueError(
            f"Colonnes manquantes dans le fichier : {colonnes_manquantes}"
        )

    # Convertir les dates et les nombres
    df["Date_achat"] = pd.to_datetime(
        df["Date_achat"], errors="coerce"
    )
    df["Prix_achat"] = pd.to_numeric(
        df["Prix_achat"], errors="coerce"
    )
    df["Quantite"] = pd.to_numeric(
        df["Quantite"], errors="coerce"
    )

    return df
