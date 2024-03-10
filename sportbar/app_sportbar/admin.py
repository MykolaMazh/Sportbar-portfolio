from django.contrib import admin
from .models import Category, MenuPosition, Match, Client, Championship


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class MenuPositionAdmin(admin.ModelAdmin):
    save_as = True


class MatchAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(MenuPosition, MenuPositionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Championship)
admin.site.register(Client)
