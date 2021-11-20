from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('artist/<str:username>/', views.artist, name='artist'),
    path('album/<int:album_id>/', views.album, name='album'),
    path('add-album/<int:artist_id>/', views.add_album, name='add_album'),
    path('edit-album/<int:album_id>/', views.edit_album, name='edit_album'),
    path('edit-profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('change-password/<int:user_id>/', views.change_password, name='change_password'),
    path('music-visibility/<int:artist_id>/', views.music_visibility, name='music_visibility'),
    path('make-admin/<int:artist_id>/', views.make_admin, name='make_admin'),
    path('remove-admin/<int:artist_id>/', views.remove_admin, name='remove_admin'),
    path('artists/', views.artists, name='artists'),
    path('explore/<sort>/', views.explore, name='explore'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<int:album_id>/', views.delete, name='delete'),
    path('album/get_lyrics/', views.get_lyrics, name='get_lyrics'),
    path('album/add_lyrics/', views.add_lyrics, name='add_lyrics'),
    path('album/add_comment/', views.add_comment, name='add_comment'),
    path('album/delete_comment/', views.delete_comment, name='delete_comment'),
    path('album/edit_comment/', views.edit_comment, name='edit_comment')
]