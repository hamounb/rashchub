from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(ContactUsModel)
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date", "modified_date", "code")
    search_fields = ("first_name", "last_name", "mobile", "email", "message", "code")
    

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)


@admin.register(ColorModel)
class ColorAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(CapacityModel)
class CapacityAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(MaterialModel)
class MaterialAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(HashtagModel)
class HashtagAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

class ProductPriceInlineAdmin(admin.TabularInline):
    model = ProductPriceModel
    fields = ("capacity", "price", "on_sale")
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

class ProducImageInlineAdmin(admin.TabularInline):
    model = ProductImageModel
    fields = ("product", "image")
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("name", "code")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductPriceInlineAdmin, ProducImageInlineAdmin]
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("product", "image")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        # Delete the associated file before deleting the object
        if obj.image:  # Assuming your file field is named 'your_file_field'
            obj.image.delete(save=False)  # Delete the file from storage
        
        # Call the parent class delete_model method to perform the actual deletion
        super().delete_model(request, obj)


@admin.register(ProductPriceModel)
class ProductPriceAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("product",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(ProductCommentModel)
class ProductCommentAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("user", "product", "comment")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(InvoiceModel)
class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("pk", "user",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)


@admin.register(InvoiceItemModel)
class InvoiceItemAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("invoice", "product")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)