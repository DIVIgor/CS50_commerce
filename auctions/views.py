from copy import copy
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from .models import User, Category, Listing, Bid, Comment, Watchlist
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    newest_listings = Listing.objects.order_by('-date_added')[:5]
    context = {'active_listings': newest_listings}
    return render(request, 'auctions/index.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def get_categories(request):
    categories = Category.objects.order_by('name')
    return render(
        request, 'auctions/categories.html', {'categories': categories}
    )

def get_listings_by_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    listings = category.listing_set.order_by('-date_added')
    context = {'category': category, 'listings': listings}
    return render(request, 'auctions/listings_by_cat.html', context)

def get_listing(request, cat_slug, listing_slug):
    listing = get_object_or_404(Listing, slug=listing_slug)
    # comments = listing.comment_set.order_by('-date_added')
    context = {
        'listing': listing, 'cat_slug': cat_slug,
        'listing_slug': listing_slug, 'start_bid': listing.start_bid
    }
    
    get_comments(listing, context)
    # make_a_bid(request, listing, context)
    # add_comment(request, listing, context)
    if request.user.is_authenticated:
        user_bids = listing.bid_set.order_by('-date_added')
        if user_bids:
            context['current_bid'] = user_bids[0].bid
            context['current_bid_owner'] = user_bids[0].user

        context['in_watchlist'] = User.objects.get(
            username=request.user).watchlist_set.filter(listing=listing)

        comment_form = CommentForm()
        context['comment_form'] = comment_form

        is_author = request.user == listing.user
        if not is_author and not user_bids[0].user == request.user: #request.user != listing.user:
            bid_form = BidForm()
            context['bid_form'] = bid_form
            # author = False
        if request.method == 'POST':
            post_data = copy(request.POST)
            post_data['listing'] = listing
            if 'bid_submit' in request.POST and not is_author:
                form = BidForm(data=post_data)
                # form.listing = listing
                # print(form)
                # filled = Decimal(form.data['bid'])
                # if filled <= listing.start_bid or filled <= context['current_bid']:
                #     raise ValidationError('Your bid must be higher than previous')
            elif 'comment_submit' in request.POST:
                form = CommentForm(data=post_data)

            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user = request.user
                form_data.listing = listing
                form_data.save()
                return redirect(listing.get_absolute_url())
            elif type(form) == BidForm:
                context['bid_form'] = form
            elif type(form) == CommentForm:
                context['comment_form'] = form
    return render(request, 'auctions/listing.html', context)

@login_required
def add_listing(request):
    if request.method != 'POST':
        listing_form = ListingForm()
    else:
        listing_form = ListingForm(data=request.POST)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.user = request.user
            listing_id = Listing.objects.latest('date_added').id + 1 if Listing.objects.all() else 1
            listing.slug = slugify(f'{listing.name}_{listing_id}')
            listing.save()
            return redirect('auctions:listing', cat_slug=listing.category.slug, listing_slug=listing.slug)
            # return redirect('auctions:listings', request.POST.get('category'))
            
    context = {'listing_form': listing_form}
    return render(request, 'auctions/add_listing.html', context)

@login_required
def get_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    context = {'watchlist': watchlist}
    return render(request, 'auctions/watchlist.html', context)

@login_required
def add_to_watchlist(request, cat_slug, listing_slug):
    listing = get_object_or_404(Listing, slug=listing_slug)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user,
        listing=listing)
    if not created:
        watchlist.delete()
    return redirect('auctions:listing', cat_slug, listing_slug)

def get_comments(listing, listing_context):
    comments = listing.comment_set.order_by('-date_added')
    return listing_context.update({'comments': comments})

def close_listing(request, cat_slug, listing_slug):
    listing = get_object_or_404(Listing, slug=listing_slug)
    listing.is_active = False
    return redirect(listing.get_absolute_url())

# @login_required
# def make_a_bid(request, listing, listing_context):
#     if request.method != 'POST':
#         bid_form = BidForm()
#     elif request.method == 'POST' and 'bid' in request.POST:
#         bid_form = BidForm(data=request.POST)
#         if bid_form.is_valid():
#             new_bid = bid_form.save(commit=False)
#             new_bid.user = request.user
#             new_bid.listing = listing
#             new_bid.save()
#     context = {'bid_form': bid_form}
#     return listing_context.update(context)

# @login_required
# def add_comment(request, listing, listing_context):
#     if request.method != 'POST':
#         comment_form = CommentForm()
#     elif request.method == 'POST' and 'comment' in request.POST:
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.listing = listing
#             new_comment.save()
#     context = {'comment_form': comment_form}
#     return listing_context.update(context)
