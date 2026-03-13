from django.shortcuts import render, redirect
from django.contrib import messages  # ✅ To show success message
from Registrationapp.models import Review

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'Aboutus.html')

def rev(request):
    if request.method == "POST":
        rid = request.POST.get("id")
        rname = request.POST.get("name")
        remail = request.POST.get("em")
        rmob = request.POST.get("mobi")
        rmes = request.POST.get("mes")

        # Save to DB
        Review.objects.create(
            rid=rid,
            rname=rname,
            remail=remail,
            rmob=rmob,
            rmes=rmes,
        )

        messages.success(request, "Review submitted successfully!")  # ✅ Django message
        return redirect('home')  # ✅ Make sure this name exists in urls.py

    return render(request, 'review.html')
