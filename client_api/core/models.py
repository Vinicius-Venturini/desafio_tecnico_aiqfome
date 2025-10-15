from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)

    class Meta:
        app_label = 'core'
        db_table = 'product'
        default_related_name = 'products'

    def __str__(self):
        return self.title

class ClientManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")
        if not name:
            raise ValueError("name is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

class Client(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False)

    products = models.ManyToManyField(
        Product,
        through="core.ClientProduct",
        related_name="clients",
    )

    objects = ClientManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'core'
        db_table = 'client'
        default_related_name = 'clients'

    def __str__(self):
        return self.email
    
class ClientProduct(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="favorite_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'core'
        db_table = "client_product"
        constraints = [
            models.UniqueConstraint(fields=["client", "product"], name="unique_client_product")
        ]

    def __str__(self):
        return f"{self.client.email} - {self.product.title}"
