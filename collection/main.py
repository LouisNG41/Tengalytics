
import os
import django
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from collection.services.cardmarket_service import charger_catalogue_cardmarket
from collection.services.service import read_stock, get_or_create_product
from collection.models import Product, PriceSnapshot

#catalogue = charger_catalogue_cardmarket()
df_collection = read_stock("data_stock_pokemon.xlsx")

print("it's all good for this file")

for _, produit in df_collection.iterrows():

    check_data(produit)
    # si Id_transac est différent de null donc que la transaction existe déja : 
    if produit["Id_transac"] != None : 
    
        

    else: 

        product = get_or_create_product(produit=produit, catalogue_produit_cm=catalogue[produit['Nom']])
        
                Product.objects.get_or_create(
                    product=produit
                )

        
        