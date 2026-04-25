from django.db import models

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Soup', 'Soup'),
        ('Main', 'Main Course'),
        ('Salad', 'Salad'),
        ('Dessert', 'Dessert'),
        ('Snack', 'Snack'),
    ]

    name = models.CharField(max_length=200)
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Main')
    
    time = models.CharField(max_length=100)
    quick = models.BooleanField(default=False)
    ingredients = models.TextField(help_text="Enter separated by comma: egg, milk, tomato")
    steps = models.TextField()

    def __str__(self):
        return self.name


class UserQuery(models.Model):
    chat_id = models.CharField(max_length=100)
    query_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Query"
        verbose_name_plural = "Search Analytics"

    def __str__(self):
        return f"{self.query_text} (from {self.chat_id})"