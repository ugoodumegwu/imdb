from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Movie
from .views import *


class MovieListPaginationTestCase(TestCase):

    ACTIVE_PAGINATION_HTML = """
    <li class='active page-item'>
        <a href="%s?page=%d" class="page-link">%d</a>
    </li>
    """


    def setUp(self):
        for n in range(15):
            Movie.objects.create(title='%d movie'%(n),
                                 year = 1990 + n,
                                 runtime = 100,
                                 )

    def testFirstPage(self):
        movie_list_path = reverse('core:MovieList')
        request = RequestFactory().get(path=movie_list_path)
        response = MovieList.as_view()(request)
        self.assertEqual(200, response.status_code, 'Incorrect status code')
        self.assertTrue(response.context_data['is_paginated'])
        self.assertInHTML(self.ACTIVE_PAGINATION_HTML % (movie_list_path, 1, 1), response.rendered_content)