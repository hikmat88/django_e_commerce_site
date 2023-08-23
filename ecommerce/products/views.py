from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Category
from .forms import CategoryForm
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userpage.auth import admin_only

# Create your views here.
def index(request):
    return HttpResponse('This is from the products app')

# to fetch all data from the database
@login_required
@admin_only
def showproduct(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'products/product.html',context)



# to show add category form and post category
@login_required
@admin_only
def addcategory(request):
    # data processing
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'category added')
            return redirect('/products/addcategory')
        else:
            messages.add_message(request,messages.ERROR,'failed to add category')
            return render(request,'products/addcategory.html',{'forms':form})
        
        

    context={
        'forms':CategoryForm
    }
    # to load add category form
    return render(request,'products/addcategory.html',context)


@login_required
@admin_only
def postproduct(request):
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product added')
            return redirect('/products/addproduct')
        else:
            messages.add_message(request,messages.ERROR,'failed to add product')
            return render(request,'products/addproduct.html',{'forms':form})

    context={
        'forms':ProductForm
    }
    return render(request,'products/addproduct.html',context)

# show all category
@login_required
@admin_only
def showcategory(request):
    category=Category.objects.all()
    context={
        'categories':category
    }
    return render(request,'products/allcategory.html',context)

# delete category
@login_required
@admin_only
def deletecategory(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request,messages.SUCCESS,'category deleted')
    return redirect('/products/allcategory')

# update category
@login_required
@admin_only

def updatecategory(request,category_id):
    instance=Category.objects.get(id=category_id)

    if request.method=='POST':
        form=CategoryForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'category update')
            return redirect('/products/allcategory')
    else:
        messages.add_message(request,messages.ERROR,'failed to update category')
        return redirect('/products/allcategory')

    context={
        'forms':CategoryForm(instance=instance)
    }
    return render(request,'products/updatecategory.html',context)

#delete product
@login_required
@admin_only

def deleteproduct(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request,messages.SUCCESS,'product delete')
    return redirect('/products/show')

# update product
@login_required
@admin_only

def updateproduct(request,product_id):
    instance=Product.objects.get(id=product_id)

    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product update')
            return redirect('/products/show')
        else:
            messages.add_message(request,messages.ERROR,'failed to update product')
            return render(request,'products/updateproduct.html',{'forms':form})

    context={
        'forms':ProductForm(instance=instance)
    }
    return render(request,'products/updateproduct.html',context)






