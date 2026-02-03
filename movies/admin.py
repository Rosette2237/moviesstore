from django.contrib import admin
from .models import Movie, Review, ReviewReport

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
# admin.site.register(Review)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'date', 'is_hidden')
    list_filter = ('is_hidden', 'date')
    search_fields = ('comment', 'user__username', 'movie__name')

@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('reason', 'user__username', 'review__comment')