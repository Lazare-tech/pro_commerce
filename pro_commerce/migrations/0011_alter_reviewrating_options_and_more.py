# Generated by Django 4.2.13 on 2024-09-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pro_commerce", "0010_rating"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reviewrating",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Commentaire et évaluation",
                "verbose_name_plural": "Commentaires et évaluations",
            },
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Date de création"
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="ip",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="Adresse IP"
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="rating",
            field=models.FloatField(default=0, verbose_name="Note"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="review",
            field=models.TextField(
                blank=True, max_length=500, null=True, verbose_name="Commentaire"
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Statut"),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="subject",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Sujet"
            ),
        ),
        migrations.AlterField(
            model_name="reviewrating",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Date de mise à jour"
            ),
        ),
    ]
