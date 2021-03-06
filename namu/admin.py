from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Deposit, Namuseta, Product, Restock, Transaction, User

# Register your models here.

admin.site.register(Namuseta)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Deposit)
admin.site.register(Restock)


class UserResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    from_encoding = "utf-8"
    to_encoding = "utf-8"
