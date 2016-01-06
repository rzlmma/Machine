from django.contrib import admin
from machine.system.models import Department, User, Role, Permission, UserRoleRelation, RolePermissionRelation

admin.site.register(Department)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(UserRoleRelation)
admin.site.register(RolePermissionRelation)