from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm

def index(request):
 
    print("views.index called by urls.py")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')
    

def show_category(request, category_name_slug):
  
    print("\nshow_category called by urls.py")
    context_dict = {}

    try:
        
        print("views.show_category - "
              "Category.objects.get(slug=category_name_slug)")
        category = Category.objects.get(slug=category_name_slug)
        print("category exists...")
        
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        
        context_dict['category'] = category
    except Category.DoesNotExist:
        
        print("except Category.DoesNotExist...")
        context_dict['category'] = None
        context_dict['pages'] = None

    
    print("return render(request, 'rango/category.html, context_dict)\n")
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            
            print("Form is valid, returning index(request)...")
            cat = form.save(commit=True)
            form.save(commit=True)
            print("views.add_category printing category name and url slug - "
                  "name: {}, slug: {}".format(cat, cat.slug))
           
            return index(request)
        else:
          
            print("Printing errors...")
            print(form.errors)
   
    print("views.add_category returned render b/c request.method != 'POST' "
          "or there are errors")
    return render(request, 'rango/add_category.html', {'form': form})


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
             if 'picture' in request.FILES:
                 profile.picture = request.FILES['picture']
             profile.save()
             registered = True
          else:
             print(user_form.errors, profile_form.errors)
      else:
          user_form = UserForm()
          profile_form = UserProfileForm()
      return render(request,
                            'rango/register.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})