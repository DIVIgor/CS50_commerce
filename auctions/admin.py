from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment, Watchlist


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display = []
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = []
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category',
        'user', 'is_active', 'date_added',
        'date_updated'
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    # list_display = []
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user',
        'date_added'
    )
    list_filter = (
        'id', 'user', 'date_added'
    )

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    # list_display = []
    pass

# admin.site.register(Category)
# admin.site.register(Listing)
# admin.site.register(Bid)
# admin.site.register(Comment)
# admin.site.register(Watchlist)
