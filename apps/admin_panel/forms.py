from django import forms
from apps.products.models import Brand, Product, Category

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo', 'description', 'is_active', 'sort_order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brand Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'brand-slug'}),
            'logo': forms.FileInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-input', 'value': 0}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'brand', 'category', 'description',
            'weight', 'price', 'discount_price', 'stock',
            'min_stock_alert', 'is_featured', 'is_new_launch',
            'is_combo_deal', 'delivery_eta', 'image_main', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'product-slug'}),
            'brand': forms.Select(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'weight': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 500g, 1L'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'min_stock_alert': forms.NumberInput(attrs={'class': 'form-input'}),
            'delivery_eta': forms.TextInput(attrs={'class': 'form-input'}),
            'image_main': forms.FileInput(attrs={'class': 'form-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new_launch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_combo_deal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django.forms import inlineformset_factory
from apps.products.models import ProductImage, BulkPricing

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=['image', 'sort_order'],
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={'class': 'form-input'}),
        'sort_order': forms.NumberInput(attrs={'class': 'form-input', 'style': 'width: 80px;'}),
    }
)

BulkPricingFormSet = inlineformset_factory(
    Product, BulkPricing,
    fields=['min_quantity', 'price_per_unit', 'discount_label'],
    extra=1,
    can_delete=True,
    widgets={
        'min_quantity': forms.NumberInput(attrs={'class': 'form-input', 'style': 'width: 100px;'}),
        'price_per_unit': forms.NumberInput(attrs={'class': 'form-input', 'style': 'width: 100px;', 'step': '0.01'}),
        'discount_label': forms.TextInput(attrs={'class': 'form-input'}),
    }
)
