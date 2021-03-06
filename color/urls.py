from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_user, name="login_user"),
    path('register/', views.regsiter_user, name="register_user"),
    path('about-us/', views.about, name="about_us"),
    path('collaborate/', views.collaborate, name="collaborate"),
    path('membership/', views.membership, name="membership"),
    path('product/<int:id>/', views.product_details, name="product-details"),
    path('search/<str:cat>/<int:id>', views.search, name="search"),
    path('add-to-cart/', views.add_to_cart, name="cart"),
    path('my-designs/', views.my_designs, name='my-designs'),
    path('my-products/', views.user_products, name='my-products'),
    path('my-commission/', views.user_commission, name='my-commission'),
    path('upload-design/', views.upload_design, name="upload-design"),
    path('my-profile/', views.my_profile, name="my-profile"),
    path('add-to-wish-list/', views.wish_list, name="wish-list"),
]
