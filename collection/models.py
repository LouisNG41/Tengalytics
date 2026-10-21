import uuid
from django.db import models
from django.core.validators import MinValueValidator


def generate_id_purchase():
    return "ACH-" + uuid.uuid4().hex[:10].upper()

class Product(models.Model):  

    class ProductType(models.TextChoices):
            SEALED = 'SEALED', 'Sealed'
            CARTES = 'CARTES', 'Cartes'

    cardmarket_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    tcg = models.CharField(max_length=50)
    nom = models.CharField(max_length=200)
    product_type = models.CharField(
            max_length=10,
            choices=ProductType.choices,
            default=ProductType.SEALED, 
        )
    category = models.CharField(max_length=50, blank=True)
    serie = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ["nom"]
        constraints = [
             models.UniqueConstraint(
                fields=["tcg", "nom", "cardmarket_id", "category", "serie"], 
                condition=models.Q(cardmarket_id__isnull=True),
                name="produit_unique")]

    def __str__(self):
        return self.nom


class Purchase(models.Model):
    id_purchase =  models.CharField(max_length=40, unique=True, default=generate_id_purchase)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase",
    )

    date_purchase = models.DateField(
        null=True,
        blank=True,
    )

    price_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
    )

    quantite = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    class Meta:
            ordering = ["-date_purchase"]
    
    def __str__(self):
        return f"{self.product.nom} x{self.quantite}"


class PriceSnapshot(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.PROTECT,
        related_name="price_history",
    )

    price_dict = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Historique des prix - {self.product.nom}"


    