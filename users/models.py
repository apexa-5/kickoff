from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None,name=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,name=None):
        user = self.create_user(email, password,name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    # Related fields that need unique related names to avoid conflicts
    groups = models.ManyToManyField('auth.Group', related_name='userprofile_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='userprofile_permissions', blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']  # Uncomment and add additional fields required for superuser

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
