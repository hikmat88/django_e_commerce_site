from django.db import models

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=10,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    Product_name=models.CharField(max_length=100)
    Product_price=models.FloatField()
    stock=models.IntegerField()
    Product_description=models.TextField()
    Product_image=models.FileField(upload_to='static/uploads',null=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Product_name
    

        
