from django.conf.urls import patterns, include, url
from test_task.views import hello, save_model_field, get_all_model_row
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$', hello),
    (r'^request/save_field/?$', save_model_field),
    (r'^request/get_all_model_row/?$', get_all_model_row),
    # Examples:
    # url(r'^$', 'test_task.views.home', name='home'),
    # url(r'^test_task/', include('test_task.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

)
