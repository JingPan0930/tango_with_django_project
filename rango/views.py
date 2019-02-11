from django.shortcuts import render
from rango.models import Category
from django.http import HttpResponse
from rango.models import Page

def index(request):

                    category_list = Category.objects.order_by('-likes')[:5]
                    context_dict = {'categories': category_list}
                    return render(request, 'rango/index.html', context_dict)

def about(request):
    
    context = RequestContext(request)
    context_dict = {}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list

    count = request.session.get('visits',0)

    context_dict['visit_count'] = count

    return render_to_response('rango/about.html', context_dict , context)


def show_category(request, category_name_slug):
      context_dict = {}
      try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category)
            context_dict['pages'] = pages
            context_dict['category'] = category
      except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None
      return render(request, 'rango/category.html', context_dict)