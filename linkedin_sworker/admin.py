from django.contrib import admin

from linkedin_sworker.models import *


@admin.register(UpdateSubscription)
class UpdateSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('email',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LatestPost)
class LatestPostAdmin(admin.ModelAdmin):
    list_display = ('posted_at', 'body', 'search_link', 'added_at', 'updated_at')
    ordering = ('-posted_at',)
    search_fields = ('body', 'search_link__keyword')
    list_filter = ('search_link__keyword',)
    readonly_fields = ('added_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('search_link')


@admin.register(SearchLink)
class SearchLinkAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'created_at', 'updated_at', 'search_link')
    ordering = ('keyword',)
    search_fields = ('keyword',)
    readonly_fields = ('created_at', 'updated_at')
