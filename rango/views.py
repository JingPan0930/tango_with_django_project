from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from rango.forms import PageForm
from rango.models import Category, Page, PostAd
from rango.forms import CategoryForm
from rango.forms import UserForm, UserProfileForm, PostForm, CommentForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from django import views
from django.contrib.auth.models import User

# Create your views here.
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    # last_visit_time = datetime.now()
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits


def index(request):
    request.session.set_test_cookie()
    # construct a dict to pass to the template engine as its context
    # note the key boldmessage is the same as {{boldmessage}} in the template
    category_list = Category.objects.order_by('-likes')[:5]
    # context_dict = {'categories': category_list}

    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}
    response = render(request, 'rango/index.html', context_dict)
    # return a rendered response to send to the client
    # we make use of the shortcut func to make our lives easier
    # note that  the first parameter is the template we wish to use

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def show_item(request, item_title_slug):
    context_dict = {}
    try:
        ads = PostAd.objects.get(slug=item_title_slug)
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        # pages = Page.objects.filter(category=ads)
        # Adds our results list to the template context under name pages.
        # context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['ads'] = ads
    except PostAd.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        context_dict['ads'] = None
        # context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def about(request):
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    ## A HTTP POST
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # have we been provided with a valid form?
        if form.is_valid():
            # save the new category to the database
            form.save(commit=True)
            # now that the category is saved
            # we could give a confirmation
            # but since the most recent category added is on the index page
            # we can direct the user back to the index page
            return index(request)
        else:
            # the supplied form contained errors
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            print("===========")
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
    else:
        ## ON the PDF of tangowithdjango19,the e.g is like that:
        #          else:
        #              print(user_form.errors, profile_form.errors)
        #  	else:
        # user_form = UserForm()
        #      	profile_form = UserProfileForm()

        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered
                   })


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))


# ==============================================
@login_required
def post_ad(request):
    posted = False
    if request.method == 'POST':
        post_ad_form = PostForm(data=request.POST)
        print(posted, post_ad_form)

        if post_ad_form.is_valid():

            ad_form = post_ad_form.save(commit=False)

            print("run here")
            if 'image' in request.FILES:
                ad_form.image = request.FILES['image']
                ad_form.likes = 0
                ad_form.save()
                posted = True
            else:
                print(post_ad_form.errors)

    else:

        post_ad_form = PostForm()

    return render(request,
                  'rango/postad.html',
                  {'post_ad_form': post_ad_form,

                   'posted': posted
                   })


# def AdCreateView(CreateView):
#     model=PostAd
#     template_name = "postad.html"
#     fields=('title',"image","description","price","location","email","phone")
#     path('rango/postad.html',views.Ad)
# ==============================
def showitem(request):
    from rango import models
    slide= models.PostAd.objects.order_by('-likes')[:1]
    ad_list = models.PostAd.objects.all()

    return render(request, "rango/showitem.html",
                  {"ad_list": ad_list,"slide":slide})


# =================================
def item(request):
    from rango import models


    title = request.GET['title']

    ad_list = models.PostAd.objects.filter(title=title)


    # mes = request.GET['message']


    if request.method == 'GET':
        com_form = CommentForm(data=request.POST)
        print(com_form.is_valid())
        if com_form.is_valid():
            comment = com_form.save(commit=False)

            comment.save()
            # registered=True


    else:
        ## ON the PDF of tangowithdjango19,the e.g is like that:
        #          else:
        #              print(user_form.errors, profile_form.errors)
        #  	else:
        # user_form = UserForm()
        #      	profile_form = UserProfileForm()

        com_form = CommentForm()
    mes_list = models.Comment.objects.all()
    return render(request, "rango/item.html", {"mes_list": mes_list, "commentform": com_form,"ad_list": ad_list})



# ========================
@login_required
def like_category(request):
    cat_id = None
    if request.method == "GET":
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


@login_required
def like_ad(request):
    ad_id = None
    if request.method == "GET":
        ad_id = request.GET['ad_id']
    likes = 0
    if ad_id:
        ad = PostAd.objects.get(id=int(ad_id))
        if ad:
            likes = ad.likes + 1
            ad.likes = likes
            ad.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    from rango import models
    cat_list = []
    if starts_with:
        cat_list = models.PostAd.objects.filter(title__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list})


def comment(request):
    from rango import models

    # mes = request.GET['message']

    registered = False
    if request.method == 'POST':
        com_form = CommentForm(data=request.POST)
        print(com_form)
        if com_form.is_valid():
            comment = com_form.save(commit=False)
            print("save")
            comment.save()
            # registered=True


    else:
        ## ON the PDF of tangowithdjango19,the e.g is like that:
        #          else:
        #              print(user_form.errors, profile_form.errors)
        #  	else:
        # user_form = UserForm()
        #      	profile_form = UserProfileForm()
        print("000")
        com_form = CommentForm()
    mes_list = models.Comment.objects.all()
    return render(request, "rango/comment.html", { "mes_list":mes_list,"commentform": com_form})


def preview(request):
    return  render(request,"rango/preview.html")
def refreshcomment(request):
    if request.method == 'POST':
        com_form = CommentForm(data=request.POST)
        print(com_form.is_valid())
        if com_form.is_valid():
            comment = com_form.save(commit=False)
            print("save")
            comment.save()
            # registered=True


    return HttpResponse(comment)


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'rango/profile_registration.html', context_dict)
	
def mydetail(request):
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    response = render(request, 'rango/mydetail.html')
    return response

@login_required
def myfavourite(request):
    from rango import models
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    email = request.user.email
    ad_list = models.PostAd.objects.filter(email = email)
    slide= models.PostAd.objects.order_by('likes')[:1]
    response = render(request,'rango/myfavourite.html',
                      {"ad_list": ad_list,"slide":slide})
    return response


@login_required
def mypost(request):
    from rango import models
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    email = request.user.email
    print (email)
    print("-----------")
    print(request.user)
    ad_list = models.PostAd.objects.filter(email = email)
    slide= models.PostAd.objects.order_by('title')[:1]
    response = render(request,'rango/mypost.html',
                      {"ad_list": ad_list,"slide":slide})
    return response


@login_required
def myinformation(request):
    from rango import models
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    
    
    response = render(request,'rango/myinformation.html')
    return response


class RangoRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


class SearchView(views.View):
    def get(self,request):
        keyword = request.GET.get('suggestion','')
        result=PostAd.objects.filter(title__icontains=keyword).order_by('title').all()

        return render(request,'rango/showitem.html',{"result":result,'item_count':len(result),'keyword':keyword})