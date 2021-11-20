from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


# Create your models here.

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default='regular', max_length=50)
    artistImage = models.CharField(default='artists/default.png', max_length=1000)
    artistName = models.CharField(default='defaultartistname', max_length=1000)
    description = models.TextField(blank=True)
    artistGenre = models.CharField(default='Trending', max_length=100)
    music_visibility = models.CharField(default='SM', max_length=2)

    def get_absolute_url(self):
        return reverse('unlabel:artist', args=[self.user.username])


@receiver(post_save, sender=User)
def create_user_artist(sender, instance, created, **kwargs):
    if created:
        Artist.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_artist(sender, instance, **kwargs):
    instance.artist.save()


class AlbumList(models.Model):
    albumName = models.CharField(max_length=100)
    albumArt = models.CharField(max_length=1000)
    published = models.DateField(auto_now_add=True)
    num_of_songs = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.albumName

    def get_absolute_url(self):
        return reverse('unlabel:album', args=[self.id])


class SongsList(models.Model):
    songName = models.CharField(max_length=1000)
    lyrics = models.TextField(blank=True)
    album = models.ForeignKey(AlbumList, on_delete=models.CASCADE)

    def __str__(self):
        return self.songName

    def get_absolute_url(self):
        return reverse('unlabel:album', args=[self.album.id])


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(AlbumList, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']



regular_user = {"username": "artist", "password": "user"}
admin_user = {"username": "admin", "password": "valid"}

# class ArtistList:
#     def __init__(self, id, artistImage, artistName, description, artistGenre):
#         self.id = id
#         self.artistImage = artistImage
#         self.artistName = artistName
#         self.description = description
#         self.artistGenre = artistGenre


# artist1 = ArtistList(101, "artists/anuv-jain.jpeg", 'Anuv Jain', "placeholder", 'Trending')
# artist2 = ArtistList(102, "artists/bharat-chauhan.jpeg", 'Bharat Chauhan', "placeholder", 'Trending')
# artist3 = ArtistList(103, "artists/bombay-bandook.jpeg", 'Bombay Bandook', "placeholder", 'Trending')
# artist4 = ArtistList(104, "artists/lifafa.jpeg", 'Lifafa',
#                      "Contemporary electronic music production has served to score the memories of a generation here in India, but with one element strangely absent - voice and vernacular. As Lifafa, Suryakant Sawhney has spent five years exploring uncharted terrain in this part of the world: electronic music that not only speaks in sonics, but also of words and meaning. The audience for this music is unknown. Via an ongoing exploration of Hindi and Urdu, a constant refinement of his own production techniques, and his instinctive take on melody and cadence, this music - spiritual and sensual, familiar and alien - has caught the attention of audiences not just in urban, Anglicised India, but in less obvious corners of this country, and beyond.",
#                      'Trending')
# artist5 = ArtistList(105, "artists/peter-cat-recording-company.jpeg", 'Peter Cat Recording Company',
#                      "Peter Cat Recording Co. is a Delhi-based band that was founded in 2009. The band consists of five members: Suryakant Sawhney, Karan Singh, Dhruv Bhola, Rohit Gupta and Kartik Sundareshan Pillai. In 2018, they signed to Paris based label Panache and released their first record Portrait of A Time: 2010 - 2016. In June 2019, they released Bismillah. With two new members on board since 2017, the decade-old band is now “a self-aware organism”, said frontman Suryakant Sawhney – a “more well-oiled machine” than ever before. It still retains three of its older members: Sawhney, the principal songwriter; Kartik Pillai on keyboard, guitars, trumpet and electronics; and Karan Singh on drums.",
#                      'Trending')
# artist6 = ArtistList(106, "artists/prabhdeep.jpeg", 'Prabhdeep',
#                      "Prabh Deep is widely acknowledged as one of the best underground MCs in the country. Born and brought up in Tilak Nagar, Prabh’s music paints a vivid picture of growing up in a locality that’s reeling from high unemployment rates and the recent influx of drugs in the community. His early critical success of his singles such as G Maane and Kal led to music streaming giant Saavn tapping him as one of the faces of their Desi Hip-Hop campaign and Apple Music featuring him as the spotlight artist of the month. His debut album, titled Class-Sikh, was produced in collaboration with hip-hop phenom Sez On The Beat and is widely regarded as one of the seminal albums that will come to define not just the Indian hip-hop scene, but the music industry in the country at large.",
#                      'Trending')
# artist7 = ArtistList(107, "artists/anoushka-masey.jpeg", 'Anoushka Masey', "placeholder", 'Trending')
# artist8 = ArtistList(108, "artists/the-local-train.jpeg", 'The Local Train', "placeholder", 'Trending')
#
# artist_list = [artist4, artist5, artist6]


# class AlbumList:
#     def __init__(self, id, albumName, albumArt, artistId, ):
#         self.id = id
#         self.albumName = albumName
#         self.albumArt = albumArt
#         self.artistId = artistId


# album1 = AlbumList(201, "Happy Holidays", "albums/happy-holidays.jpeg", 105)
# album2 = AlbumList(202, "Potrait of Time", "albums/portrait-of-time.jpeg", 105)
# album3 = AlbumList(203, "We’re Getting Married", "albums/we're-getting-married.jpeg", 105)
# album4 = AlbumList(204, "Chitta", "albums/chitta.jpeg", 106)
# album5 = AlbumList(205, "Tabia", "albums/tabia.jpeg", 106)
# album6 = AlbumList(206, "Pandemic", "albums/pandemic.jpeg", 106)
# album7 = AlbumList(207, "Jaago", "albums/jaago.jpeg", 104)
# album8 = AlbumList(208, "Superpower 2020", "albums/superpower-2020.jpeg", 104)
#
# album_list = [album1, album2, album3, album4, album5, album6, album7, album8]


# class SongsList:
#     def __init__(self, id, songName, albumId, ):
#         self.id = id
#         self.songName = songName
#         self.albumId = albumId


# song1 = SongsList(301, "Clouds", 201)
# song2 = SongsList(302, "Work Clothes", 201)
# song3 = SongsList(303, "Chronic", 201)
# song4 = SongsList(304, "Potrait of a Time", 202)
# song5 = SongsList(305, "Copulations", 202)
# song6 = SongsList(306, "Flies", 202)
# song7 = SongsList(307, "We're Getting Married", 203)
# song8 = SongsList(308, "Chitta", 204)
# song9 = SongsList(309, "Qafir", 205)
# song10 = SongsList(310, "Tabia", 205)
# song11 = SongsList(311, "Taqat", 205)
# song12 = SongsList(312, "Pandemic", 206)
# song13 = SongsList(313, "Jaago", 207)
# song14 = SongsList(314, "Nikamma", 207)
# song15 = SongsList(315, "Candy", 207)
# song16 = SongsList(316, "Laash", 208)
# song17 = SongsList(317, "Irradon", 208)
# song18 = SongsList(318, "Mann Ki Baat", 208)
#
# song_list = [song1, song2, song3, song4, song5, song6, song7, song8, song9, song10, song11, song12, song13, song14,
#              song15, song16, song17, song18]
