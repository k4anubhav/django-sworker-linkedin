from datetime import timedelta

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response

from linkedin_sworker.serializers import *

UPDATE_INTERVAL = timedelta(seconds=int(os.environ['UPDATE_INTERVAL_SEC']))


class SearchLinksListView(ListAPIView):
    serializer_class = SearchLinkSerializer

    def get_queryset(self):
        return SearchLink.objects.all()


class LatestPostCreateView(CreateAPIView):
    serializer_class = LatestPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_ = serializer.validated_data['id']
        post = LatestPost.objects.filter(id=id_).first()
        if post:
            post.save()
            return Response({'detail': 'already posted'}, status=status.HTTP_200_OK)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class UpdatePostsRequiredView(GenericAPIView):
    @staticmethod
    def get(request):
        last_updated_post = LatestPost.objects.order_by('-updated_at').first()
        if last_updated_post is None or last_updated_post.updated_at < timezone.now() - UPDATE_INTERVAL:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
