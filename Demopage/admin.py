from django.contrib import admin

# Register your models here.


from .models import Neighbourhood

admin.site.register(Neighbourhood)

from .models import House

admin.site.register(House)

from .models import Room

admin.site.register(Room)