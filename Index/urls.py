from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [ url(r'$', views.Index, name='Index'),
                url(r'^test', views.ToCentralcontrol, name='ToCentralControl')

]

