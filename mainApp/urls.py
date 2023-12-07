from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('category/<int:cat_id>', views.category, name="category"),
    path('category/<int:cat_id>/<int:subcat_id>', views.subcategory, name="subcategory"),
    path('user/', views.user, name="user"),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('cart/', views.cart, name="cart"),
    path('product/<int:prod_id>', views.product, name="product"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]
