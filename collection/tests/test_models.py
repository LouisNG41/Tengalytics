from datetime import date
from decimal import Decimal
import pytest

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import PriceSnapshot, Purchase, Product
from django.utils import timezone

pytestmark = pytest.mark.django_db

class ProductTests(TestCase):
    def test_create_product_without_cardmarket_id(self):
        Product.objects.create(tcg="Pokemon", nom="Elite Trainer box 30th", category="ETB")
        Product.objects.create(tcg="Pokemon", nom="Bundle 151", category="Bundle")
        self.assertEqual(Product.objects.count(), 2)

    def test_cant_create_product_with_same_cardmarket_id(self):
        Product.objects.create(tcg="Pokemon", nom="Eevee ex", cardmarket_id=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(tcg="Pokemon", nom="Autre", cardmarket_id=1)

    def test_same_name_and_same_serie(self):
        Product.objects.create(tcg="Pokemon", nom="Pikachu ex", product_type="CARTES", serie="PRE")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(tcg="Pokemon", nom="Pikachu ex", product_type="CARTES", serie="PRE")

class PurchaseTests(TestCase):
    def setUp(self):
        self.product_ETB_30th =  Product.objects.create(tcg="Pokemon", nom="Elite Trainer box 30th", category="ETB", cardmarket_id="41")

    def test_verification_id_generation_from_purchase(self):
        achat = Purchase.objects.create(product=self.product_ETB_30th, date_purchase="2026-10-10", price_purchase=Decimal("10"))
        self.assertTrue(achat.id_purchase.startswith("ACH-"))

    def test_same_purchase_ok(self):
        achat1 = Purchase.objects.create(product=self.product_ETB_30th, date_purchase="2026-10-10", price_purchase=Decimal(100))
        achat2 = Purchase.objects.create(product=self.product_ETB_30th, date_purchase="2026-10-10", price_purchase=Decimal(100))
        self.assertEqual(Purchase.objects.count(), 2)

    def test_id_purchase_unique(self):
        Purchase.objects.create(id_purchase="ACH-1", product=self.product_ETB_30th, price_purchase=Decimal(10))
        with self.assertRaises(IntegrityError), transaction.atomic():
            Purchase.objects.create(id_purchase="ACH-1", product=self.product_ETB_30th, price_purchase=Decimal(12))

    def test_cant_create_purchase_with_negatif_price(self):

        purchase = Purchase.objects.create(product=self.product_ETB_30th, date_purchase="2026-10-10", price_purchase=Decimal(-10))
        with pytest.raises(ValidationError) as exc_info : 
            purchase.full_clean()

    def test_cant_create_purchase_with_negatif_quantite(self) : 

        purchase = Purchase.objects.create(product=self.product_ETB_30th, date_purchase="2026-10-10", price_purchase=Decimal(10), quantite = 0)
        with pytest.raises(ValidationError) as exc_info : 
            purchase.full_clean()
        
    def test_delete_product_include_delete_purchase(self):
        Purchase.objects.create(id_purchase="ACH-1", product=self.product_ETB_30th, price_purchase=Decimal(10))
        self.product_ETB_30th.delete()
        self.assertEqual(Purchase.objects.count(), 0)

class PriceSnapshotTests(TestCase):

    def test_create_product_include_create_priceSnapshot(self):
        product = Product.objects.create(tcg="Pokemon", nom="Elite Trainer box 30th", category="ETB")
        self.assertEqual(PriceSnapshot.objects.count(), 1)

    def test_create_product_and_update_priceSnapshot(self):
        product = Product.objects.create(tcg="Pokemon", nom="Elite Trainer box 30th", category="ETB")
        pricesnapshot = product.price_history
        assert pricesnapshot.price_dict == {}
        pricesnapshot.add_daily_price(avg=45.50, low=42.00, trend=60.00)
        today_str = timezone.now().date().isoformat()
        assert today_str in pricesnapshot.price_dict
        metrics = pricesnapshot.price_dict[today_str]
        assert metrics["avg"] == 45.50
        assert metrics["low"] == 42.00
        assert metrics["trend"] == 60.00
