from django.contrib import admin
from rango.models import Category, Page
from django.utils.text import slugify

#Clase personalizada para el modelo Page
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Registrar el modelo Category
admin.site.register(Category, CategoryAdmin)
# Registrar el modelo Page y Admin
admin.site.register(Page, PageAdmin)
