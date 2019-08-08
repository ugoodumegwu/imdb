from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Movie, Person, Vote, MovieImage
from django.views import View
from .forms import VoteForm, ImageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.exceptions import PermissionDenied

class MovieList(ListView):
    model = Movie
    paginate_by = 3

class MovieDetail(DetailView):

    model = Movie
    queryset = Movie.objects.all_score()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_blank_vote(movie=self.object, user=self.request.user)
            if vote.id:
                vote_form_url = reverse('core:UpdateVote', kwargs={'movie_id': self.object.id, 'pk': vote.id})
            else:
                vote_form_url = reverse('core:CreateVote', kwargs={'movie_id': self.object.id})
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url']  = vote_form_url
            image_form = ImageForm(initial={
                'user': self.request.user,
                'movie': Movie.objects.get(pk=self.object.id),
            })
            ctx['image_form'] = image_form
        return ctx




class PersonDetailView(DetailView):

    queryset = Person.objects.all_with_prefetch_movies()
    template_name = 'core/my_person_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Indiviual Detail'
        return data


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm
    template_name = 'core/test.html'

    # this method below i believe is to fill the form with initial data
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        movie_id = self.kwargs['movie_id']
        initial['movie'] = Movie.objects.get(pk=movie_id)
        return initial


    def form_invalid(self, form):
        print('form invalid')
        print(form.cleaned_data)
        return redirect(to=(reverse('core:MovieDetail', kwargs={'pk':self.kwargs['movie_id']})))

    def get_success_url(self):
        return reverse('core:MovieList')




class UpdateVote(LoginRequiredMixin, UpdateView):

    form_class = VoteForm
    template_name = ''
    queryset = Vote.objects.all()


    def get_object(self, queryset=None):
        vote = super().get_object(self.queryset)
        user = self.request.user
        movie = vote.movie
        if user != vote.user:
            raise PermissionDenied('cannot change antoher users vote')
        return vote

    def get_success_url(self):
        return reverse('core:MovieList')



class MovieUpload(LoginRequiredMixin, CreateView):

    form_class = ImageForm
    model = MovieImage
    movie_id = ''
    template_name = 'core/imageupload.html'

    def get_initial(self):
        initial = super(MovieUpload, self).get_initial()
        initial['user'] = self.request.user
        initial['movie'] = self.kwargs['movie_id']
        self.movie_id = self.kwargs['movie_id']
        return initial

    def form_invalid(self, form):
        print('inside form invalid')
        print(form.cleaned_data)
        return redirect(to='core:MovieList')

    def get_success_url(self):
        return reverse('core:MovieDetail', kwargs={'pk': self.movie_id})

class TopView(ListView):
    model = Movie
    queryset = Movie.objects.top_10_movies(10)
    template_name = 'core/top_10_movies.html'