from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    

choices = (
   ('Gown','Gown'),
   ('Saree','Saree'),
   ('Lehengas','Lehengas'),
   ('Anarkali','Anarkali'),
   ('Western Wear','Western Wear'),
   ('Indo-Western','Indo-Western')    
)

class Category(models.Model):
    category_name = models.CharField(max_length=255,choices=choices,default = 'Saree')
 
    def __str__(self):
        return self.category_name
    

class Costume(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Image(models.Model):
    costume = models.ForeignKey(Costume, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.costume


class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costumes = models.ManyToManyField(Costume, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    costume = models.ForeignKey(Costume, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.email} booked {self.costume.name}'

