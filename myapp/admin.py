from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from myapp.models import *

class CategoryAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username == 'christsquareuser':
            return qs  # Show the records
        return qs.none()
    def has_module_permission(self, request):
        return request.user.username == 'christsquareuser' 
    list_display = ('category_name', 'category_slug','category_description') 


class TagAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username == 'christsquareuser':
            return qs  # Show the records
        return qs.none()
    def has_module_permission(self, request):
        return request.user.username == 'christsquareuser'

    list_display = ('tag_name', 'tag_slug','tag_description')


# Register your models here.
class SongListAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username == 'christsquareuser' or request.user.username == 'chorduser' or  request.user.username == 'penielselvam':
            return qs  # Show the records
        return qs.none()
    def has_module_permission(self, request):
        return request.user.username in ['christsquareuser' ,'chorduser','penielselvam']
    list_display = ('article_title','song_views','date_posted','ppt_uploaded_at','has_chords','presenter_views','presenter_todayviews','song_todayviews','last_viewed','thumb_images','ppt')
    #list_display = ['title', 'meta_title','song_views','date_posted','Tag','get_Tags']
    #list_display_links = ['tag_name']
    def display_chords(self, obj):
        # Truncate chords to first 5 characters
        return obj.chords[:5] if obj.chords else ''
    display_chords.short_description = 'chords'  # Set the column name in admin
    def has_chords(self, obj):
        return "Yes" if obj.chords else "No"

    has_chords.short_description = "chords"  # Column name in Django Admin

    search_fields=('article_title','Tag__tag_name','slug')
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'style': 'font-family: monospace'})},
    }
    fields = [
        'article_title',  
        'url', 
        'body',
        'description',
        'englishlyrics',
        'tanglishlyrics',
        'english_trans_lyrics',
        'thumb_images',
        'ppt',
        #'ppt_uploaded_at',
        'tamil_lyrics',
        #'thanglish_lyrics',
        'chords', 
        #'description',
        'Tag',
        'Categorys',
        'slug',
        'lyricsslug',
        'song_views',
        'song_todayviews',
        'presenter_views',
        'presenter_todayviews', 
    ]

    def get_tags(self, obj):
       return "\n".join([a.tag_name for a in obj.Tag_set.all()])

admin.site.register(SongList,SongListAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)       