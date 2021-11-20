from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Artist, AlbumList, SongsList, Comments, Action
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    artist_list = Artist.objects.all()
    albums = AlbumList.objects.all()
    album_list = []
    for album in albums:
        if album.artist.music_visibility == 'SM':
            album_list.append(album)

    if request.session.get("username", False):
        user = User.objects.get(username=request.session['username'])
        actions = Action.objects.filter(user=user)

        for user_album in user.artist.albumlist_set.all():
            query = Action.objects.filter(target_id=user_album.id)
            actions = actions | query

        return render(request, 'unlabel/site/index.html',
                      {"artist_list": artist_list, "album_list": album_list[:5], "actions": actions})

    else:
        return render(request, 'unlabel/site/index.html', {"artist_list": artist_list})


def artist(request, username):
    _artist = Artist.objects.get(user__username=username)
    albums = _artist.albumlist_set.all()
    actions = Action.objects.filter(user=_artist.user)

    for album in albums:
        album.songs = album.songslist_set.all()

    if actions:
        return render(request, 'unlabel/site/artist.html', {"artist": _artist, "albums": albums, "actions": actions})

    else:
        return render(request, 'unlabel/site/artist.html', {"artist": _artist, "albums": albums})


def album(request, album_id):
    this_album = AlbumList.objects.get(id=album_id)

    if this_album.artist.music_visibility == 'HM':
        return redirect('unlabel:home')

    else:
        songs = this_album.songslist_set.order_by('songName')
        artist_name = this_album.artist.artistName
        comments = this_album.comments_set.all()

        if request.session.get("username", False):
            user = User.objects.get(username=request.session['username'])
            return render(request, 'unlabel/site/detail.html',
                          {"album": this_album, "songs": songs, "artist_name": artist_name, "comments": comments,
                           "user": user})

        else:
            return render(request, 'unlabel/site/detail.html',
                          {"album": this_album, "songs": songs, "artist_name": artist_name, "comments": comments})


def add_album(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    if request.session.get("username", False) and (artist.user.username == request.session['username']):
        if request.method == "POST":
            albumArt = request.POST.get("album-art")
            albumName = request.POST.get("album-name")
            songs = request.POST.getlist("song-name")
            songs = [i for i in songs if i]
            this_artist = Artist.objects.get(id=artist_id)
            new_album = AlbumList(
                albumName=albumName,
                albumArt=albumArt,
                num_of_songs=len(songs),
                artist=this_artist,
            )
            new_album.save()

            for song in songs:
                new_song = SongsList(songName=song, album=new_album)
                new_song.save()

            action = Action(
                user=artist.user,
                verb="added the album",
                target=new_album
            )
            action.save()

            messages.add_message(request, messages.SUCCESS, 'Album added successfully!')
            return redirect('unlabel:album', album_id=new_album.id)

        else:
            _artist = Artist.objects.get(id=artist_id)
            return render(request, 'unlabel/site/add-album.html', {"artist": _artist})

    else:
        return redirect('unlabel:home')


def edit_album(request, album_id):
    album = AlbumList.objects.get(id=album_id)
    songs = album.songslist_set.all()

    if (request.session.get("username", False)) and (request.session['role'] == 'regular') and (
            album.artist.user.username == request.session['username']):
        if request.method == "POST":
            albumArt = request.POST.get("album-art")
            albumName = request.POST.get("album-name")
            songs = request.POST.getlist("song-name")
            songs = [i for i in songs if i]
            # this_artist = Artist.objects.get(id=album.artist.id)
            get_album = AlbumList.objects.get(id=album_id)
            get_album.albumName = albumName
            get_album.albumArt = albumArt
            get_album.num_of_songs = len(songs)
            get_album.save()

            get_album.songslist_set.all().delete()
            for song in songs:
                new_song = SongsList(songName=song, album=get_album)
                new_song.save()

            action = Action(
                user=get_album.artist.user,
                verb="edited the album",
                target=get_album
            )
            action.save()

            messages.add_message(request, messages.INFO, 'Album edited successfully.')
            return redirect('unlabel:album', album_id=get_album.id)
        else:
            return render(request, 'unlabel/site/edit-album.html', {"album": album, "songs": songs})

    else:
        return redirect('unlabel:home')


def edit_profile(request, username):
    artist = Artist.objects.get(user__username=username)
    # Check if user is logged in
    if request.session.get("username", False):

        if (request.session['role'] == 'admin') or (artist.user.username == request.session['username']):
            if request.method == "POST":
                artistImage = request.POST.get("artist-image")
                artistName = request.POST.get("display-name")
                email = request.POST.get("email")
                bio = request.POST.get('bio')

                artist.artistImage = artistImage
                artist.artistName = artistName
                artist.user.email = email
                artist.description = bio
                artist.user.save()
                artist.save()

                action = Action(
                    user=artist.user,
                    verb="edited their profile",
                )
                action.save()

                # messages.add_message(request, messages.INFO, 'Album edited successfully.')
                return redirect('unlabel:artist', username=username)
            else:
                return render(request, 'unlabel/site/edit-profile.html', {"user": artist.user})
        else:
            return redirect('unlabel:home')
    else:
        return redirect('unlabel:home')


def change_password(request, user_id):
    user = User.objects.get(id=user_id)
    new_password = request.POST.get('password')
    user.set_password(new_password)
    user.save()
    # Logout user
    del request.session['username']
    del request.session['role']
    return redirect('unlabel:home')


def music_visibility(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    artist.music_visibility = request.POST.get('music-visibility')
    artist.save()
    return redirect('unlabel:artist', username=artist.user.username)


def remove_admin(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    artist.role = 'regular'
    artist.save()
    return redirect('unlabel:artist', username=artist.user.username)


def make_admin(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    artist.role = 'admin'
    artist.save()
    return redirect('unlabel:artist', username=artist.user.username)


def explore(request, sort):
    albums = AlbumList.objects.order_by(sort)
    album_list = []
    for album in albums:
        if album.artist.music_visibility == 'SM':
            album_list.append(album)
    return render(request, 'unlabel/site/list.html', {"album_list": album_list})


def artists(request):
    artist_list = Artist.objects.all()
    return render(request, 'unlabel/site/artists.html', {"artist_list": artist_list})


def delete(request, album_id):
    album = AlbumList.objects.get(id=album_id)
    album.songslist_set.all().delete()
    album.delete()
    messages.add_message(request, messages.WARNING, 'Deletion successful.')
    return redirect('unlabel:explore')


def get_lyrics(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        song_id = request.POST.get('song_id')
        song = SongsList.objects.get(id=song_id)
        return JsonResponse({'success': 'success', 'song_lyrics': song.lyrics}, status=200)


def add_lyrics(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        song_id = request.POST.get('song_id')
        song = SongsList.objects.get(id=song_id)
        lyrics = request.POST.get('lyrics')
        song.lyrics = lyrics
        song.save()
        action = Action(
            user=song.album.artist.user,
            verb="added lyrics for",
            target=song
        )
        action.save()
        return JsonResponse({'success': 'success', 'song_lyrics': song.lyrics}, status=200)


def add_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        album_id = request.POST.get('album_id')
        comment = request.POST.get('comment')

        album = AlbumList.objects.get(id=album_id)
        user = User.objects.get(username=request.session['username'])

        new_comment = Comments(
            user=user,
            album=album,
            body=comment
        )
        new_comment.save()

        action = Action(
            user=user,
            verb="commented on",
            target=album
        )
        action.save()

        return JsonResponse({'success': 'success', 'comment': {
            "body": comment,
            "name": user.artist.artistName,
            "image": user.artist.artistImage,
            "username": user.username,
            "id": new_comment.id
        }}, status=200)


def delete_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        comment = Comments.objects.get(id=request.POST.get('comment_id'))
        comment.delete()
        return JsonResponse({'success': 'success'}, status=200)


def edit_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        comment = Comments.objects.get(id=request.POST.get('comment_id'))
        comment.body = request.POST.get('comment')
        comment.save()
        return JsonResponse({'success': 'success'}, status=200)


def search(request):
    return render(request, 'unlabel/site/search-results.html')


def register(request):
    if not request.session.get("username", False):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('display-name')
            user = User.objects.create_user(username, email, password)
            user.artist.artistName = name
            user.artist.save()
            request.session['username'] = user.username
            request.session['role'] = user.artist.role

            # messages.add_message(request, messages.SUCCESS, 'Registered successfully!')

            return redirect('unlabel:home')
        else:
            return render(request, 'unlabel/site/register.html')
    else:
        return redirect('unlabel:home')


def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['username'] = user.username
            request.session['role'] = user.artist.role

        return redirect('unlabel:home')

    else:
        return render(request, 'unlabel/site/login.html')


def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect('unlabel:home')
