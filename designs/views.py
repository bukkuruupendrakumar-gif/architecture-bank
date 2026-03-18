from django.shortcuts import render
from .models import Category, Design

def home(request):
    query = request.GET.get('q')
    
    categories = Category.objects.all()
    designs = None

    if query:
        designs = Design.objects.filter(name__icontains=query)

    return render(request, "home.html", {
        "categories": categories,
        "designs": designs
    })

def designs(request, id):
    designs = Design.objects.filter(category_id=id)
    return render(request, "designs.html", {"designs": designs})
def like_design(request, id):
    # your logic here
    return redirect('home')