from rest_framework.generics import CreateAPIView, ListAPIView

from linkedin_sworker.serializers import *


class SearchLinksListView(ListAPIView):
    serializer_class = SearchLinkSerializer

    def get_queryset(self):
        return SearchLink.objects.all()


class LatestPostCreateView(CreateAPIView):
    serializer_class = LatestPostSerializer
