from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('saved-listings', views.saved_listings, name='saved_listings'),
    path("create/listing", views.create_listing, name="create_listing"),
    path("watch-listing/<int:listing_id>", views.watch_listing, name="watch_listing"),
    path("unwatch-listing/<int:listing_id>", views.unwatch_listing, name="unwatch_listing"),
    path("listing/<int:listing_id>", views.show_listing, name='show_listing'),
]
