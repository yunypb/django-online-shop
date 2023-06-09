from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from OnlineShop.forms import FormCard, CreateUserForm, CreateComs
from OnlineShop.models import Product, Category_brands, Category_model, Category_for, Image, Card, Cart, Order, Comment

def pagination_p(request, context, items):
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1
    paginator = Paginator(items, 3)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context['items'] = items

def all_for_main_page():
    brands = Category_brands.objects.all()
    section = Category_model.objects.all()
    type = Category_for.objects.all()

    context = {'brands': brands, 'section': section, 'type': type}
    return context


def sex_men_or_women(num):
    items = Product.objects.filter(sex=num)

    return items


@login_required(login_url='login')
def main_page(request):
    items = Product.objects.all()
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def main_page_men(request):
    items = sex_men_or_women(1)
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def main_page_women(request):
    items = sex_men_or_women(2)
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def main_page_brand(request, brand_pk):
    items = Product.objects.filter(category_brands=brand_pk)
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def main_page_section(request, section_pk):
    items = Product.objects.filter(category_model=section_pk)
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def main_page_type(request, type_pk):
    items = Product.objects.filter(category_for=type_pk)
    context = all_for_main_page()
    pagination_p(request, context, items)
    return render(request, 'OnlineShop/shop.html', context)


@login_required(login_url='login')
def about(request):
    context = all_for_main_page()
    return render(request, 'OnlineShop/about.html', context)


@login_required(login_url='login')
def index(request):
    context = all_for_main_page()

    return render(request, 'OnlineShop/index.html', context)


@login_required(login_url='login')
def contact(request):
    context = all_for_main_page()
    return render(request, 'OnlineShop/contact.html', context)


@login_required(login_url='login')
def shop_single(request, product_id):
    type = Category_for.objects.all()
    product = Product.objects.get(id=product_id)
    images = Image.objects.filter(product=product_id)
    items = Product.objects.filter(category_model=product.category_model)[:3]

    if len(Comment.objects.filter(product=product_id)) == 0:
        num_coms = '"Not yet"'
        len_coms = '"Not yet"'
    else:
        num_coms = sum(i.review for i in Comment.objects.filter(product=product_id)) / len(
            Comment.objects.filter(product=product_id))
        product.rating = num_coms
        product.save()
        len_coms = len(Comment.objects.filter(product=product_id))
    context = {'items': items, 'product': product, 'images': images, 'type': type, 'num_coms': num_coms,
               'len_coms': len_coms}
    return render(request, 'OnlineShop/shop-single.html', context)


@login_required(login_url='login')
def cart(request):
    if not Cart.objects.filter(user=request.user):
        Cart.objects.create(user=request.user)
    type = Category_for.objects.all()
    items = Cart.objects.get(user=request.user)
    len_p = sum(i.quantity for i in items.product.all())
    context = {'type': type, 'items': items, 'sum_p': sum(i.quantity_f for i in items.product.all()), 'len_p': len_p}
    if Card.objects.filter(user=request.user):
        card = Card.objects.get(user=request.user)
        context['card'] = card
    return render(request, 'OnlineShop/cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    if not Cart.objects.filter(user=request.user):
        Cart.objects.create(user=request.user)
    prod = Product.objects.get(pk=product_id)
    products = Cart.objects.get(user=request.user)
    products.product.add(prod)
    prod.quantity += 1
    prod.save()
    prod.quantity_f = prod.quantity * prod.price
    prod.save()
    return redirect('shop_single', product_id)


@login_required(login_url='login')
def add_to_cart_and_go_cart(request, product_id):
    if not Cart.objects.filter(user=request.user):
        Cart.objects.create(user=request.user)
    prod = Product.objects.get(pk=product_id)
    products = Cart.objects.get(user=request.user)
    products.product.add(prod)
    prod.quantity += 1
    prod.save()
    prod.quantity_f = prod.quantity * prod.price
    prod.save()
    return redirect('cart')


@login_required(login_url='login')
def card_add(request):
    if request.method == 'POST':
        form = FormCard(request.POST)
        if form.is_valid():
            items = form.save(commit=False)
            items.user = request.user
            items.save()
            return redirect('cart')
    else:
        form = FormCard()
        context = {'form': form}
        return render(request, 'OnlineShop/cardpage.html', context)


@login_required(login_url='login')
def card_delete(request):
    card = Card.objects.all().delete()
    return redirect('cart')


@login_required(login_url='login')
def delete_p_f_cart(request, pr_pk):
    cart = Cart.objects.get(user=request.user)
    prod = cart.product.get(pk=pr_pk)
    prod.quantity = 0
    prod.save()
    Cart.objects.get(user=request.user).product.remove(pr_pk)
    return redirect('cart')


@login_required(login_url='login')
def delete_p_f_cart_all(request):
    cart = Cart.objects.get(user=request.user)
    for i in cart.product.all():
        i.quantity = 0
        i.save()
    Cart.objects.get(user=request.user).product.clear()
    return redirect('cart')


@login_required(login_url='login')
def qount_plus(request, prod_pk):
    prod = Cart.objects.get(user=request.user).product.get(pk=prod_pk)
    prod.quantity += 1
    prod.quantity_f = prod.quantity * prod.price
    prod.save()

    return redirect('cart')


@login_required(login_url='login')
def qount_min(request, prod_pk):
    prod = Cart.objects.get(user=request.user).product.get(pk=prod_pk)
    prod.quantity -= 1
    prod.quantity_f = prod.quantity * prod.price
    prod.save()
    if prod.quantity == 0:
        Cart.objects.get(user=request.user).product.remove(prod_pk)
    return redirect('cart')


@login_required(login_url='login')
def order_create(request):
    order = Order.objects.create(user=request.user)
    cart = Cart.objects.get(user=request.user)
    order.cost = sum(i.quantity_f for i in cart.product.all())
    for i in cart.product.all():
        order.product.add(i)
        i.quantity = 0
        i.save()
    order.save()
    cart.product.clear()
    return redirect('order')


@login_required(login_url='login')
def order(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'OnlineShop/order.html', context)


def login_page(request):
    if request.user is not None:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'OnlineShop/login.html')

        context = {}
        return render(request, 'OnlineShop/login.html', context)
    else:
        return redirect('index')


def register(request):
    if request.user is not None:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form': form}
        return render(request, 'OnlineShop/registration.html', context)
    else:
        return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def comments(request, product_id):
    coms = Comment.objects.filter(product=product_id)
    pk = product_id
    my_com = Comment.objects.filter(user=request.user).filter(product=product_id)

    context = {'coms': coms, 'pk': pk, 'my_com': my_com}
    return render(request, 'OnlineShop/comments.html', context)


@login_required(login_url='login')
def comments_add(request, product_id):
    form = CreateComs()
    pk = product_id
    if request.method == 'POST':
        reviews = request.POST.get('rating')
        form = CreateComs(request.POST)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.review = reviews
            com.product = Product.objects.get(pk=product_id)
            com.review_p = 5 - int(com.review)
            com.save()
            Product.objects.get(pk=product_id).rating = sum(
                i.review for i in Comment.objects.filter(product=product_id))
            return redirect('comments', product_id)
    else:

        context = {'form': form, 'pk': pk}
        return render(request, 'OnlineShop/comment_add.html', context)


@login_required(login_url='login')
def comment_del(request, product_id):
    Comment.objects.filter(user=request.user).get(product=product_id).delete()
    return redirect('comments', product_id)


@login_required(login_url='login')
def comment_edit(request, product_id):
    comss = Comment.objects.filter(user=request.user).get(product=product_id)
    pk = product_id
    if request.method == 'POST':
        form = CreateComs(request.POST, instance=comss)
        num = comss.review
        reviews = request.POST.get('rating')
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            if reviews is not None:
                com.review = reviews
                com.review_p = 5 - int(com.review)
            else:
                com.review = num
                com.review_p = 5 - num
            com.product = Product.objects.get(pk=product_id)
            com.save()
            return redirect('comments', product_id)
    else:
        form = CreateComs(instance=comss)
        context = {'form': form, 'pk': pk}
        return render(request, 'OnlineShop/comment_add.html', context)

