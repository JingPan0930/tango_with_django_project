from django.contrib import admin
from rango.models import Category, Page, PageAdmin,PostAd,Comment
from rango.models import UserProfile
# admin.site.register(Category)
admin.site.register(Page, PageAdmin)
# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
class PostadAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(PostAd,PostadAdmin)
admin.site.register(Comment)