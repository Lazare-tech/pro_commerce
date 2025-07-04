# Generated by Django 4.2.13 on 2024-09-25 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pro_commerce", "0015_category_photos_product_photos_subcategory_photos"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="product_images/", verbose_name="Image du produit"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="photos",
            field=models.URLField(
                blank=True, null=True, verbose_name="Photo du produit"
            ),
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("couleur", models.CharField(max_length=30, verbose_name="Couleur")),
                (
                    "taille",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Taille"
                    ),
                ),
                (
                    "photo_principale",
                    models.ImageField(
                        upload_to="product_variants/", verbose_name="Photo principale"
                    ),
                ),
                (
                    "photos_supplémentaires",
                    models.ManyToManyField(
                        blank=True,
                        related_name="variants",
                        to="pro_commerce.productimage",
                        verbose_name="Photos supplémentaires",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="pro_commerce.product",
                        verbose_name="Produit principal",
                    ),
                ),
            ],
        ),
    ]
