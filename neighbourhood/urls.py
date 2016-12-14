from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from auxilary import *
import auxilary

urlpatterns = [
    url(r'^House/(?P<house_id>[0-9]+)$',views.house, name='House'),
    url(r'^House/(?P<house_id>[0-9]+)/chart_data_energy$',views.getchartdata,name='Chartdata'),
    url(r'^room/(?P<id>[0-9]+)$',views.room, name='Room'),
    url(r'^$',views.indexneighbourhood, name='IndexNeighbourhood'),
    url(r'^CentralControl',views.indexcentralcontrol,name="ToCentralControl"),
    url(r'^Root',views.Root,name='Root'),
    url(r'^Demo',views.Demo_homepage,name='Demo'),
    url(r'^$',views.indexcentralcontrol, name='IndexCentralControl'),
    url(r'^testinterface',views.testinterface, name='testinterface'),
    url(r'^status/(?P<device_id>[0-9]+)/(?P<value>[0-9]+)/(?P<roomorhouse>[0-9]+)/(?P<type>[0-9]+)$', auxilary.change_status, name='status'),
    url(r'^doityourself',views.handmatig, name='handmatig'),
    url(r'^start/(?P<house_id>[0-9]+)/(?P<roomorhouse>[0-9]+)/', auxilary.daytime, name='start'),
    url(r'^optimalisated',views.vergelijking, name = 'vergelijking'),
    url(r'^initialise', auxilary.initialise, name='initialise'),



]

#/(?P<house_ip>\w+)/(?P<room_id>[0-9]+)/(?P<device_ref_id>\w+)/(?P<value>[0-9]+)$'



