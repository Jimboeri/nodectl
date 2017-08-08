from django.contrib import admin

# Register your models here.
from .models import Class_type, Node, Device, NodeDevice, ndDetail

admin.site.register(Class_type)
admin.site.register(Node)
admin.site.register(Device)
admin.site.register(NodeDevice)
admin.site.register(ndDetail)
