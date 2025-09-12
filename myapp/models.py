from django.db import models


class Category(models.Model):
    category_name=models.CharField(max_length=500,default='')
    category_slug=models.CharField(max_length=500,default='')
    category_description=models.CharField(max_length=1200,default='')
    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name=models.CharField(max_length=500,default='')
    tag_slug=models.CharField(max_length=500,default='')
    tag_description=models.CharField(max_length=1200,default='')
    def __str__(self):
        return self.tag_name


class SongList(models.Model):
    #title=models.CharField(max_length=300,default='')
    url=models.CharField(max_length=300,default='')
    thumb_images=models.ImageField(upload_to='media/store/images/thumbimages',default='',blank=True)
    body=models.TextField()
    chords = models.TextField(null=True, blank=True, default=None)
    ppt=models.FileField(upload_to='media/store/pdfs',default='',blank=True)
    description=models.TextField()
    article_title=models.CharField(max_length=400,default='')
   # category=models.CharField(max_length=500,default='')
    #tags=models.ForeignKey(Tag,on_delete=models.CASCADE,null=True,blank=True)
   # categories=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)#
    #tag=models.ForeignKey(Tag,on_delete=models.CASCADE,null=True,blank=True)
    Tag=models.ManyToManyField('Tag')
    #slug=AutoSlugField(populate_from='title', slugify_function=my_slugify_function)
    #slug = models.SlugField(blank=True, unique=True)
    Categorys=models.ManyToManyField('Category')
    slug=models.CharField(max_length=1000,null=True,blank=True)
    lyricsslug=models.CharField(max_length=1000,null=True,blank=True)
    song_views=models.IntegerField(default=0)
    song_todayviews=models.IntegerField(default=0) 
    date_posted= models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    englishlyrics=models.TextField()
    tanglishlyrics=models.TextField()
    english_trans_lyrics=models.TextField(null=True, blank=True)
    last_viewed= models.DateTimeField(auto_now_add=True)
    ppt_uploaded_at = models.DateTimeField(null=True, blank=True)
    tamil_lyrics = models.TextField(null=True, blank=True)        # ✅ new field
    thanglish_lyrics = models.TextField(null=True, blank=True)    # ✅ new field
    presenter_views=models.IntegerField(default=0)
    presenter_todayviews=models.IntegerField(default=0)