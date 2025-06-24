# import os
# import sys
# import django
# from faker import Faker

# from pro_commerce.models import Category




# # Insérez le chemin vers le répertoire racine de votre projet Django (e_comm)
# sys.path.insert(0, '/home/yelmani/Bureau/CIRI/projet_commerce/e_comm/e_comm')


# # Réglez le DJANGO_SETTINGS_MODULE correctement
# os.environ['DJANGO_SETTINGS_MODULE'] = 'e_comm.settings'

# # django.setup()

# # Importez maintenant votre modèle Category depuis l'application pro_commerce

# # Votre script continue ici...
# # Initialisez Faker
# faker = Faker()

# # Supprimez toutes les données existantes dans Category
# Category.objects.all().delete()

# # Fonction pour créer des catégories et des sous-catégories fictives
# def create_categories():
#     for _ in range(5):
#         category = Category.objects.create(nom=faker.word())
#         for _ in range(2):
#             Category.objects.create(nom=faker.word(), sub_nom=category)

# if __name__ == '__main__':
#     create_categories()
#     print("Catégories et sous-catégories créées avec succès")
