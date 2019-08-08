from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.aggregates import Sum
from uuid import uuid4


def movie_directory_path_with_uuid(instance, filename):
#    return '%d/%d' % (instance.movid.id, uuid4()) test this above string formatting to see if this works.
    return '{}/{}'.format(instance.movie_id, uuid4())

# class MovieImageModel
class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)




# creating a movie manager
class MovieManager(models.Manager):

    def all_with_related_person(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('actors', 'writers')
        return qs

    def all_score(self):
        qs = self.all_with_related_person()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs

    def top_10_movies(self, limit):
        qs = Movie.objects.all().annotate(score=Sum('vote__value'))
        qs = qs.exclude(score=None)
        qs = qs.order_by('-score')
        qs = qs[:limit]
        return qs



class PersonManager(models.Manager):

    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related('directed', 'writing_credits', 'role_set__movie')




class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('last_name', 'first_name')


    def __str__(self):
        if self.died:
            return '%s, %s %s-%s' % (self.last_name, self.first_name, str(self.born), str(self.died))
        return '%s, %s %s' % (self.last_name, self.first_name, str(self.born))




class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted'),
    )
    director = models.ForeignKey(Person, related_name='directed',on_delete=models.SET_NULL, null=True, blank=True)
    writers = models.ManyToManyField(Person, related_name='writing_credits', blank=True)
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    website = models.URLField(blank=True)
    actors = models.ManyToManyField(
        Person,
        through='Role',
        related_name='acting_credits',
        blank=True
    )

    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')


    def __str__(self):
        return '%s, %d' % (self.title, self.year)



class Role(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)


    class Meta:
        unique_together = ('movie', 'person', 'name')

    def __str__(self):
        return '%d %d %s' % (self.movie.id, self.person.id, self.name)



class VoteManager(models.Manager):

    def get_vote_or_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(movie=movie, user=user)
        except Vote.DoesNotExist:
            return Vote(movie=movie, user=user)



class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, 'Like'),
        (DOWN, 'Dislike'),
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'movie')


    def __str__(self):
        return '%s voted on %s' % (self.user, self.movie)

    def get_absolute_url(self):
        return reverse('core:MovieList')

