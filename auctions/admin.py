from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment, Watchlist


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'is_staff', 'is_active', 'last_login',
        'date_joined'
    )
    list_display_links = list_display
    list_filter = (
        'is_active', 'is_staff',
        'last_login', 'date_joined'
    )
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category',
        'user', 'is_active', 'date_added',
        'date_updated'
    )
    list_editable = ('is_active',)
    list_display_links = list_display[:4]
    list_filter = (
        'category', 'name', 'user',
        'is_active', 'date_added', 'date_updated'
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name', 'user__username')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user', 'bid')
    list_display_links = list_display
    list_filter = ('listing', 'user', 'bid')
    search_fields = ('listing__name', 'user__username', 'bid')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user', 'date_added')
    list_display_links = list_display
    list_filter = ('id', 'listing', 'user', 'date_added')
    search_fields = ('listing__name', 'user__username')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing')
    list_display_links = list_display
    list_filter = ('user', 'listing')
    search_fields = ('user__username', 'listing__name')

# admin.site.register(Category)
# admin.site.register(Listing)
# admin.site.register(Bid)
# admin.site.register(Comment)
# admin.site.register(Watchlist)
