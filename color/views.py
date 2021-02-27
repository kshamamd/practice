from django.shortcuts import render, redirect
from .models import Banner, HomeBanner, ThemeCategory, Theme, Product, Image, Cart, User, CreatorDesign
from .forms import RegisterUser, CreatorDesignForm, UpdateProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponse
from django.views import View


# Project Views


def wish_list(request):
    response = HttpResponse('adding product to wish list')
    print(response)
    if request.method == 'POST':
        wish_id = request.POST.get('data_id')
        print(request.POST.get('data_id'))
        if 'wish_id' in request.COOKIES:
            wish_id = request.COOKIES['wish_id']
            counter = wish_id.split('|')
            ids = set(counter)
            print('wish ids {}'.format(ids))
            print('wish id {}'.format(wish_id))
            wish_object_id_list = []
            for prod_id in ids:
                product = Product.objects.filter(id=prod_id)
                wish_object_id_list.append(product)
            wish_count = len(set(counter))
        else:
            wish_count = 1
        '''adding product id to wish list'''
        print('wish {}'.format(request.COOKIES['wish_id']))
        if 'wish_id' in request.COOKIES:
            wish_id = request.COOKIES['wish_id']
            if wish_id == "":
                wish_id = str(wish_id)
            else:
                wish_id = wish_id + "|" + str(wish_id)
            response.set_cookie('wish_id', wish_id)
        else:
            response.set_cookie('wish_id', wish_id)
            print('wish response {}'.format(wish_id))
    # return JsonResponse({'status': 'ok'})
    return render(request, template_name="pages/wish-list.html", context={})


'''Adding products to Cart'''
'''def add_to_cart(request):
    print('cart {}'.format(request.COOKIES))
    response = HttpResponse('adding product to cart!')
    # for cart counter, fetching products ids added by customer from cookies
    if request.method == 'POST': 
        product_id = request.POST.get('data_id')
        cart = request.session.get('cart')

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids'] 
            counter = product_ids.split('|')
            ids = set(counter)
            product_object_list = []
            for prod_id in ids:
                product = Product.objects.filter(id=prod_id)
                product_object_list.append(product)
            product_count_in_cart = len(set(counter))
        else:
            product_count_in_cart = 1
        print(product_id)
        #response = render(request, template_name="pages/cart.html")
        #return redirect('cart')
        #, context={'product_object_list': product_object_list,'product_count_in_cart': product_count_in_cart}
        #adding product id to cookies list is empty
        if 'product_ids' in request.COOKIES: 
            product_ids = request.COOKIES['product_ids']
            if product_ids == "":
                product_ids = str(product_id)
            else:
                product_ids = product_ids+"|"+str(product_id)
            response.set_cookie('product_ids', product_ids)
        else:
            response.set_cookie('product_ids', product_id)

        product = Product.objects.get(id=product_id)
        messages.info(request, str(product.product_name) + ' added to cart successfully!')
   # return JsonResponse({'status': 'ok'})
    return render(request, template_name="pages/cart.html")'''


def my_profile(request):
    get_home_banners = HomeBanner.objects.first()
    get_user = User.objects.get(id=request.user.id)
    change_pass = PasswordChangeForm(request.user)
    form = UpdateProfile(request.POST or None, instance=get_user)
    if request.method == "POST" and 'update_profile' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('color:my-profile')

    if request.method == 'POST' and 'update_pass' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('color:my-profile')
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, template_name="pages/user-profile.html",
                  context={'get_home_banners': get_home_banners, 'form': form, 'change_pass': change_pass})


def user_commission(request):
    print(request.COOKIES)
    return render(request, template_name="pages/user-commission.html", context={})


def user_products(request):
    get_user_products = Product.objects.filter(creator_id=request.user.id)
    get_user_product_count = Product.objects.filter(creator_id=request.user.id).count()
    return render(request, template_name="pages/user-product.html",
                  context={'get_user_products': get_user_products, 'get_user_product_count': get_user_product_count})


def upload_design(request):
    creator_design_form = CreatorDesignForm(request.POST or None)
    if request.method == "POST":
        creator_design_form = CreatorDesignForm(request.POST or None, request.FILES)
        print(creator_design_form)
        if creator_design_form.is_valid():
            creator_design_form = creator_design_form.save(commit=False)
            creator_design_form.user = request.user
            creator_design_form.design_status = 'under_review'
            creator_design_form.save()
            return redirect('color:my-designs')
    return render(request, template_name="pages/design-upload.html", context={"form": creator_design_form})


def my_designs(request):
    get_current_login_user_designs = CreatorDesign.objects.filter(user=request.user)
    get_current_login_user_design_count = CreatorDesign.objects.filter(user=request.user).count()

    return render(request, template_name="pages/user-designs.html",
                  context={'get_current_login_user_designs': get_current_login_user_designs,
                           'get_current_login_user_design_count': get_current_login_user_design_count})


def regsiter_user(request):
    form = RegisterUser(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password2']
            form = form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('color:dashboard')
    return render(request, template_name="registration/register.html", context={'form': form})


def login_user(request):
    logout(request)
    username = password = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('color:dashboard')
    else:
        return redirect('color:dashboard')
    return render(request, template_name='dashboard.html', context={})


def dashboard(request):
    print(request.session)
    # response = HttpResponse('adding product to wish list')
    # value1 = request.COOKIES['pr']
    # print('cookie {}'.format(value1))
    get_replaceable_banner = Banner.objects.first()
    get_home_banners = HomeBanner.objects.first()
    get_all_theme_categories = ThemeCategory.objects.all()
    get_all_themes = Theme.objects.all()
    get_six_theme_categories = ThemeCategory.objects.all().order_by('-date')[:6]
    get_six_themes = Theme.objects.all().order_by('-date')[:6]
    get_cult_favs = Product.objects.all().order_by('-date')[:4]
    # form = AuthenticationForm()
    # request.login_form = form
    response = render(request, template_name='dashboard.html',
                      context={'get_all_theme_categories': get_all_theme_categories,
                               'get_replaceable_banners': get_replaceable_banner, 'get_home_banners': get_home_banners,
                               'get_all_themes': get_all_themes, 'get_cult_favs': get_cult_favs,
                               'get_six_themes': get_six_themes, 'get_six_theme_categories': get_six_theme_categories})
    # response.set_cookie('pr', '123456789')
    return response


def product_details(request, id):
    get_single_product = Product.objects.get(id=id)
    get_images = Image.objects.filter(product_for=get_single_product.id)
    single_cat = []
    single_theme = []
    for get_cat in get_single_product.product_category.all():
        single_cat.append(get_cat)

    for get_theme in get_single_product.product_theme.all():
        single_theme.append(get_theme)
    get_similar_products_by_category = Product.objects.filter(product_category=single_cat[0]).order_by('-id')[:4]
    get_similar_products_by_theme = Product.objects.filter(product_theme=single_theme[0]).order_by('-id')[:4]
    return render(request, template_name="pages/product-details.html",
                  context={'get_single_product': get_single_product, 'get_images': get_images,
                           'get_similar_products': get_similar_products_by_category,
                           'get_similar_products_by_theme': get_similar_products_by_theme})


def search(request, cat, id):
    get_all_theme_categories = ThemeCategory.objects.all()
    get_all_themes = Theme.objects.all()
    get_home_banners = HomeBanner.objects.first()
    get_products_by_category_or_theme = ''
    try:
        get_products_by_category_or_theme = Product.objects.filter(product_category=id, product_theme=id).order_by(
            '-date')
    except:
        pass
    paginator = Paginator(get_products_by_category_or_theme, 12)  # 1 posts in each page
    page = request.GET.get('page')
    try:
        get_products_by_category_or_theme = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        get_products_by_category_or_theme = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        get_products_by_category_or_theme = paginator.page(paginator.num_pages)
    return render(request, template_name="pages/search.html",
                  context={'get_all_theme_categories': get_all_theme_categories, 'category_or_theme': cat,
                           'get_all_themes': get_all_themes, 'get_home_banners': get_home_banners,
                           'get_products_by_category_or_theme': get_products_by_category_or_theme, 'page': page})


def about(request):
    return render(request, template_name='pages/about.html', context={})


def collaborate(request):
    register_member = RegisterUser(request.POST or None)
    return render(request, template_name='pages/collaborate.html', context={'register_member': register_member})


def membership(request):
    return render(request, template_name='pages/membership.html', context={})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})


# class Index(View):

def add_to_cart(request):
    if request.method == 'POST':
        product = request.POST.get('data_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity <= 1:
                    cart.pop(product)
                else:
                    cart[product] = quantity - 1
            else:
                cart[product] = quantity + 1

        else:
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1

    request.session['cart'] = cart
    print('cart', request.session['cart'])
    print(product)
    # print('cart {}'.format(request.COOKIES))
    return render(request, template_name='pages/about.html')


'''def get(self, request):
    # print()
    return HttpResponse(f'/color{request.get_full_path()[1:]}')'''


