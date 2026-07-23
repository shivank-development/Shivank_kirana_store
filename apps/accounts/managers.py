"""
Custom User Manager — Shivank Kirana Store
Handles user creation with email as the unique identifier.
"""
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    Email is used as the primary identifier instead of username.
    """

    def create_user(self, email, phone, full_name, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError(_('Email address is required.'))
        if not phone:
            raise ValueError(_('Phone number is required.'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'customer')

        user = self.model(
            email=email,
            phone=phone,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, full_name, password=None, **extra_fields):
        """Create and return a superuser (admin)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, phone, full_name, password, **extra_fields)

    def create_delivery_boy(self, email, phone, full_name, password=None, **extra_fields):
        """Create and return a delivery boy user."""
        extra_fields.setdefault('role', 'delivery_boy')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(email, phone, full_name, password, **extra_fields)

    def get_by_phone(self, phone: str):
        """Lookup user by phone number."""
        return self.get(phone=phone)

    def active_customers(self):
        """Return all active customers."""
        return self.filter(role='customer', is_active=True)

    def active_delivery_boys(self):
        """Return all active delivery boys."""
        return self.filter(role='delivery_boy', is_active=True)
