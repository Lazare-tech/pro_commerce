
### 3. **Modification du script de seed**

# Avec ces changements, vous pouvez ajuster votre script de seed pour qu'il utilise des URLs d'images valides :

# ```python
import os
import django
import random
from faker import Faker

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_comm.settings')
django.setup()

from compte.models import User
from phonenumber_field.phonenumber import PhoneNumber
from pro_commerce.models import Category, Subcategory, Adresse, Product, UserFavorite

# Utilisez faker pour générer des données aléatoires
fake = Faker()

# Liste d'URLs d'images pour les produits
product_image_urls = [
     'https://unsplash.com/fr/photos/paires-de-lot-de-sandales-assorties-sur-textile-blanc-I7GHd8PlZqc',
     'https://unsplash.com/fr/photos/une-paire-de-chaussures-assise-sur-un-canape-aDsuSeXQPeo',
            'https://unsplash.com/fr/photos/personne-portant-une-montre-chronographe-blanche-DC49m383KP4',
        'https://unsplash.com/fr/photos/allume-iphone-6-dore-6lcT2kRPvnI',
         'https://unsplash.com/fr/photos/une-personne-tient-un-telephone-cellulaire-avec-une-brosse-a-dents-a-la-main-3sU8hrWjsmc',
    'https://unsplash.com/fr/photos/une-personne-fait-cuire-des-nouilles-dans-une-casserole-sur-une-table-7Jr2cegwwUI',
'https://unsplash.com/fr/photos/batteur-sur-socle-multicolore-avec-boitier-en-verre-eIqO4P50MeY',
'https://unsplash.com/fr/photos/textiles-de-couleurs-assorties-SDR3oDS4mOc',
'https://unsplash.com/fr/photos/calme-jeune-homme-boucle-en-veste-en-cuir-de-style-de-rue-marchant-et-fumant-FFYfj5w1P-g',

   ]

def generate_burkina_phone_number():
    """ Générer un numéro de téléphone aléatoire au format +226 suivi de 8 chiffres """
    return f"+226{random.randint(10000000, 99999999)}"

# Données des catégories et sous-catégories
categories_data = [
    {'nom': 'Chaussures', 'souscategories': ['Baskets', 'Sandales', 'Talons']},
    {'nom': 'Habits', 'souscategories': ['T-Shirts', 'Pantalons', 'Vestes']},
    {'nom': 'Téléphones', 'souscategories': ['Smartphones', 'Téléphones classiques']},
    {'nom': 'Montres', 'souscategories': []},
    {'nom': 'Matériel de cuisine', 'souscategories': ['Casseroles', 'Mixeurs']},
]

def populate_categories():
    print("Création des catégories et sous-catégories...")
    for cat_data in categories_data:
        # Création de la catégorie
        categorie = Category.objects.create(
            nom=cat_data['nom'],
            slug=fake.slug(),
            photo=random.choice(product_image_urls)  # Choisir une URL d'image aléatoire pour la catégorie
        )
        print(f"Catégorie créée: {categorie.nom}")
        
        # Création des sous-catégories
        for souscat_nom in cat_data['souscategories']:
            souscategorie = Subcategory.objects.create(
                nom=souscat_nom,
                categorie=categorie,
                slug=fake.slug(),
                photo=random.choice(product_image_urls)  # Choisir une URL d'image aléatoire pour la sous-catégorie
            )
            print(f"Sous-catégorie créée: {souscategorie.nom} pour la catégorie {categorie.nom}")

def populate_users():
    print("Création des utilisateurs avec numéros de téléphone...")
    for _ in range(5):
        phone_number = generate_burkina_phone_number()
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        print(f"Utilisateur créé: {user.username} avec numéro {phone_number}")
        # Création de l'adresse de l'utilisateur
        Adresse.objects.create(
            ville=fake.city(),
            quartier=fake.street_name(),
            repere=fake.sentence(nb_words=3)[:20],
            contact=PhoneNumber.from_string(phone_number=phone_number, region='BF'),
            utilisateur=user
        )
        print(f"Adresse créée pour {user.username} avec numéro {phone_number}")

def populate_products():
    print("Création des produits avec images associées aux catégories et sous-catégories...")
    categories = Category.objects.all()
    users = User.objects.all()
    for categorie in categories:
                # for _ in range(random.randint(3, 6)):  # Créez entre 3 et 6 produits par catégorie

        for _ in range(random.randint(1, 3)):  # Créez entre 3 et 6 produits par catégorie
            user = random.choice(users)  # Choisir un utilisateur aléatoire
            adresse = random.choice(user.adresses.all()) if user.adresses.exists() else None
            product = Product.objects.create(
                photo=random.choice(product_image_urls),  # Choisir une URL d'image aléatoire
                nom=fake.word().capitalize(),
                ville=fake.city(),
                description=fake.sentence(nb_words=12)[:99],  # Description avec max 120 caractères
                prix=random.randint(1000, 50000),
                stock=random.randint(1, 100),
                categorie=categorie,
                sous_categorie=random.choice(categorie.souscategories.all()) if categorie.souscategories.exists() else None,
                utilisateur=user,
                adresse=adresse
            )
            print(f"Produit créé: {product.nom} dans la catégorie {product.categorie.nom}")

# def populate_favorites():
#     print("Création des produits favoris...")
#     users = User.objects.all()
#     products = Product.objects.all()
#     for user in users:
#         favorite_products = random.sample(list(products), random.randint(1, 5))  # Chaque utilisateur peut avoir 1 à 5 produits favoris
#         for product in favorite_products:
#             UserFavorite.objects.get_or_create(user=user, product=product)
#             print(f"{user.username} a ajouté {product.nom} à ses favoris.")

def run():
    populate_categories()
    populate_users()
    populate_products()
    # populate_favorites()

if __name__ == '__main__':
    run()
