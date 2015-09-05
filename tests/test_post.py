from __future__ import unicode_literals, print_function

from rest_framework import status
from mezzanine.blog.models import BlogPost
from mezzanine_api.views import PostViewSet

from tests.utils import TestCase


class TestPostViewSet(TestCase):
    """
    Test the API resources for blog post.
    """

    def setUp(self):
        super(TestPostViewSet, self).setUp()
        self.viewset = PostViewSet
        self.post_published = BlogPost.objects.create(
            title="New Published Post", content="Some Published Content",
            publish_date='2000-01-01', user=self.user)

        self.post_draft = BlogPost.objects.create(
            title="New Draft Post", content="Some Draft Content",
            user=self.user)

        self.request = self.create_request_on_local_thread()

    def tearDown(self):
        super(TestPostViewSet, self).tearDown()
        self.post_published.delete()
        self.post_draft.delete()

    def test_retrieve_published_post(self):
        response = self.call_view(self.request, 'retrieve', pk=self.post_published.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post_published.title)

    def test_retrieve_draft_post_fails(self):
        response = self.call_view(self.request, 'retrieve', pk=self.post_draft.pk)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_published_posts(self):
        response = self.call_view(self.request, 'list')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['title'], self.post_published.title)
