from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    # listings
    path('', views.index, name="index"),
    path('categories/', views.get_categories, name='categories'),
    path('<slug:cat_slug>/',
        views.get_listings_by_category, name='listings'),
    path('<slug:cat_slug>/<slug:listing_slug>/',
        views.get_listing, name='listing'),
    # account
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    # user actions
    path('add_listing', views.add_listing, name='add_listing'),
    path('watchlist', views.get_watchlist, name='get_watchlist'),
    path('<slug:cat_slug>/<slug:listing_slug>/add_to_watchlist',
        views.add_to_watchlist, name="watch"),
    path('<slug:cat_slug>/<slug:listing_slug>/close_listing',
        views.close_listing, name="close_listing"),
    path('my-listings', views.get_users_listings, name='get_users_listings'),
    path('bidding', views.get_bidding, name='bidding')
]
