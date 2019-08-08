from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('movies/', MovieList.as_view(), name='MovieList'),
    path('movie/<int:pk>', MovieDetail.as_view(), name='MovieDetail'),
    path('movie/<int:movie_id>/vote', CreateVote.as_view(), name='CreateVote'),
    path('movie/<int:movie_id>/vote/<int:pk>', UpdateVote.as_view(), name='UpdateVote'),
    path('movie/<int:movie_id>/upload', MovieUpload.as_view(), name='MovieUpload'),
    path('movies/top_10/', TopView.as_view(), name='Top10MoviesList')
]