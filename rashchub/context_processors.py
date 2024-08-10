from store.models import CategoryModel

def menu(request):
    categories = CategoryModel.objects.all()
    return {"categories":categories}