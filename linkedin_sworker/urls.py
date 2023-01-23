from django.urls import path

from linkedin_sworker.views import *

urlpatterns = [
    path('latest-posts/', LatestPostCreateView.as_view(), name='create_latest_posts'),
    path('search-links/', SearchLinksListView.as_view(), name='create_search_links'),
    path('update-posts-required/', UpdatePostsRequiredView.as_view(), name='update_posts_required'),
]
