from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, PriceSnapshot

@receiver(post_save, sender=Product)
def create_product_snapshot(sender, instance, created, **kwargs):
    print(f"\n📢 LE SIGNAL A ÉTÉ DÉCLENCHÉ ! Créé: {created}")
    if created:
        PriceSnapshot.objects.create(
            product=instance,
        )
