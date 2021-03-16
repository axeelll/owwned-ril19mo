from django.contrib import admin
from .models import Building
from .models import Floor
from .models import Room

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
