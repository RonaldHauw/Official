from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.Demo_homepage, name='Demo_homepage'),
    url(r'^Uitleg',views.demo_uitleg,name='Demo_uitleg'),
    url(r'^contact',views.contact,name='Contact_page'),
    url(r'^root',views.Root,name='Root'),
    url(r'^User', views.user_homepage, name='User_homepage'),
    url(r'^CentralControl',views.centralcontrol,name="ToCentralControl"),
    url(r'^DemoDatabaseInterfaceCentralcontrolunit',views.DemoDatabaseInterfaceCentralcontrolunit,name="DemoDatabaseInterfaceCentralcontrolunit"),
    url(r'^Demo_Encryptie',views.Demo_Encryptie,name="Demo_Encryptie"),
    url(r'^Demo_Communicatie_Elektronica_Optimalisatie',views.Demo_Communicatie_Elektronica_Optimalisatie,name="Demo_Communicatie_Elektronica_Optimalisatie"),
    url(r'^Vergelijking', views.vergelijking,name="Vergelijking"),
]

