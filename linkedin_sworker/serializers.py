from rest_framework import serializers

from linkedin_sworker.models import *


class LatestPostSerializer(serializers.ModelSerializer):
    keyword = serializers.PrimaryKeyRelatedField(queryset=SearchLink.objects.all(), source='search_link')

    class Meta:
        model = LatestPost
        fields = ('id', 'body', 'keyword')
        extra_kwargs = {
            'id': {'read_only': False, 'validators': []},
        }


class SearchLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLink
        fields = ('keyword', 'search_link')

    def save(self, **kwargs):
        raise Exception('This method is not allowed')
