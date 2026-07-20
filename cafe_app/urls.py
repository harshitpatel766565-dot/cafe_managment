from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:id>/', views.category_filter, name='category_filter'),
    path('register/', views.register, name='register'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path("contact/", views.contact, name="contact"),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('increase-quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-item/<int:id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]