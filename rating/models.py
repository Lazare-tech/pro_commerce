from django.db import models
from compte.models import User
from pro_commerce.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.db.models import Avg, Count
from e_comm import settings

# Create your models here.

class ReviewRating(models.Model):
    produit = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True,null=True,verbose_name="Sujet")
    review = models.TextField(max_length=500, blank=True,null=True,verbose_name="Commentaire")
    rating = models.FloatField(default=0, verbose_name="Note")
    ip = models.CharField(max_length=20, blank=True,verbose_name="Adresse IP")
    status = models.BooleanField(default=True,verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Date de mise à jour")

    # def __str__(self):
    #     return self.subject
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"

    class Meta:
        verbose_name = "Commentaire et évaluation"
        verbose_name_plural = "Commentaires et évaluations"
        ordering = ['-created_at']  # Afficher les commentaires les plus récents en premier

    def get_rating(self):
        """Retourne la note du commentaire."""
        return f"{self.rating}/5"
# #---------------------------------------------
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produit.header}: {self.rating}"