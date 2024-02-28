from django.contrib import admin
from blog_app.models import Post, Category, Comment, Photo, FeaturedPhoto
from looks_app.models import Look, LooksCategory

# from .models import Look

class PhotoInline(admin.TabularInline):
    model = Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post', 'url')  
    fields = ('post', 'url') 

class FeaturedPhotoInline(admin.TabularInline):
    model = FeaturedPhoto

class FeaturedPhotoAdmin(admin.ModelAdmin):
    list_display = ('post', 'url')  
    fields = ('post', 'url') 


class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'display_posts')

    def display_posts(self, obj):
        return ", ".join([post.title for post in obj.post_set.all()])
    
    display_posts.short_description = 'Posts'


class LooksCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'display_looks')

    def display_looks(self, obj):
        return ", ".join([look.description for look in obj.look_set.all()])

    display_looks.short_description = 'Looks'


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(FeaturedPhoto, FeaturedPhotoAdmin)
admin.site.register(Comment)
admin.site.register(LooksCategory, LooksCategoryAdmin)
admin.site.register(Look)


