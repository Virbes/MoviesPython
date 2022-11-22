from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, logout_then_login

from webapp.views import home_page, movies_page, movie_page, movie_add_page, \
    movie_edit_page, categories, delete_category, profile, manage_users, create_user, users_edit, edit_profile, \
    delete_users, add_to_cart, my_cart, delete_my_movie, payment, payment_cash, ticket, my_shopping, report_sales, \
    about, delete_user, registro, login_page, logout_page

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_page, name='inicio'),
    path('movies/', movies_page, name='movies_page'),
    path('movie/<int:movie_key>/', movie_page, name='movie_page'),
    path('new-movie/', movie_add_page, name='movie_add_page'),
    path('movie/<int:movie_key>/edit/', movie_edit_page),
    path('categories/', categories, name='categories'),
    path('categories/delete/<int:id_category>/', delete_category, name='delete_category'),

    path('my-profile/', profile, name='profile'),
    path('manage-users/', manage_users, name='manage_users'),
    path('new-user/', create_user, name='create_user'),
    path('users-edit/', users_edit, name='users_edit'),
    path('users-edit/<username>/', edit_profile, name="edit_profile"),
    path('delete-users/', delete_users, name='delete_users'),
    path('delete-user/<int:id_user>/', delete_user),

    path('registro/', registro, name='registro'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),

    path('movie/<int:movie_key>/acquire/', add_to_cart),
    path('my-cart/', my_cart, name='my_cart'),
    path('delete/my-movie/<int:my_movie_key>/', delete_my_movie),

    path('payment/', payment),
    path('payment/cash/', payment_cash),
    path('ticket/<int:id_sale>/', ticket),

    path('my-shopping/', my_shopping, name='my_shopping'),
    path('report-sales/', report_sales, name='report_sales'),

    path('about/', about, name='about')
]
