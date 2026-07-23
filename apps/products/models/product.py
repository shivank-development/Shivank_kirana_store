"""
Product model — core catalog item.
"""
from django.db import models
from django.utils.text import slugify
from apps.products.models.category import Category
from apps.products.models.brand import Brand


class Product(models.Model):
    """Main product model with all e-commerce fields."""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='products')
    description = models.TextField(blank=True)
    weight = models.CharField(max_length=50, blank=True, help_text='e.g. 1Kg, 500g, 1L')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                 help_text='MRP (original price)')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=True, blank=True,
                                          help_text='Selling price (discounted)')
    discount_percent = models.IntegerField(default=0, help_text='Auto-calculated')
    
    # Inventory
    stock = models.IntegerField(default=0)
    min_stock_alert = models.IntegerField(default=5,
                                           help_text='Alert admin when stock <= this')
    
    # Flags
    is_featured = models.BooleanField(default=False)
    is_new_launch = models.BooleanField(default=False)
    is_combo_deal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Delivery
    delivery_eta = models.CharField(max_length=100, default='Tomorrow')
    
    # Ratings
    rating_avg = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    bought_count = models.IntegerField(default=0,
                                        help_text='e.g. "325+ Bought in last month"')
    
    # Images
    image_main = models.ImageField(upload_to='products/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{n}'
                n += 1
            self.slug = slug
        
        # Auto-calculate discount percent
        if self.discount_price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            self.discount_percent = int(discount)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def selling_price(self):
        """Return discount_price if set, else price."""
        return self.discount_price if self.discount_price else self.price

    @property
    def savings(self):
        """Amount saved vs MRP."""
        if self.discount_price:
            return self.price - self.discount_price
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def low_stock(self):
        return 0 < self.stock <= self.min_stock_alert
