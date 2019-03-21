from django.conf.urls import url
from rango import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name="add_category"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    # url(r'^/(?P<category_name_slug>[\w\-]+)/$',
    #     views.show_category, name='show_item'),
    # url(r'^register_profile/$', views.register_profile, name='register_profile'),
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^adpost/$', views.post_ad, name='adpost'),
    url(r'^showitem/$', views.showitem, name='showitem'),
    url(r'^item/$', views.item, name='item'),
    url(r'^like/$', views.like_category, name='like_category'),
    url(r'^like_ad/$', views.like_ad, name='like_ad'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
    url(r'^comment/', views.comment,name='comment'),
	url(r'^preview/', views.preview,name='preview'),
	url(r'^refreshcomment/', views.refreshcomment,name='refreshcomment'),
	url(r'^search/$', view =views.SearchView.as_view(),name='search'),
	url(r'^mydetail/$', views.mydetail, name='mydetail'),
    url(r'^myfavourite/$', views.myfavourite, name='myfavourite'),
    url(r'^mypost/$', views.mypost, name='mypost'),
    url(r'^myinformation/$', views.myinformation, name='myinformation'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    # tets
    # url(r'^ad_images/(?P<path>.*)', 'django.views.static.serve', {'document_root':'E:\\workspace\\tango_with_django_project'}),
]