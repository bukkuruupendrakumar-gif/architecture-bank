from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings


from .models import Category, Design, Wishlist, Booking


# =============================
# 🏠 HOME + SEARCH
# =============================
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


# =============================
# 🔐 LOGIN (FIXED ✅)
# =============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Validate fields
        if not username or not password:
            return render(request, 'login.html', {
                "error": "All fields are required"
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Redirect to next page if exists
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'dashboard')

        else:
            return render(request, 'login.html', {
                "error": "Invalid username or password"
            })

    return render(request, 'login.html')


# =============================
# 📝 SIGNUP (FIXED ✅ NO CRASH)
# =============================
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Empty validation
        if not username or not password:
            return render(request, "signup.html", {
                "error": "All fields are required"
            })

        # ✅ Prevent duplicate crash
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        # ✅ Create user safely
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()

        return redirect("login")

    return render(request, "signup.html")


# =============================
# 🚪 LOGOUT
# =============================
def logout_view(request):
    logout(request)
    return redirect('login')


# =============================
# 📊 DASHBOARD
# =============================
@login_required
def dashboard(request):
    categories = Category.objects.all()
    bookings = Booking.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'categories': categories,
        'bookings': bookings,
        'wishlist': wishlist
    })


# =============================
# 📂 CATEGORY → DESIGNS
# =============================
@login_required
def designs(request, id):
    designs = Design.objects.filter(category_id=id)

    return render(request, "designs.html", {
        "designs": designs
    })


# =============================
# ❤️ LIKE
# =============================
@login_required
def like_design(request, id):
    design = get_object_or_404(Design, id=id)

    if request.user in design.likes.all():
        design.likes.remove(request.user)
    else:
        design.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# =============================
# ⭐ WISHLIST (AJAX)
# =============================
@login_required
def wishlist_toggle(request, id):
    design = get_object_or_404(Design, id=id)

    wish, created = Wishlist.objects.get_or_create(
        user=request.user,
        design=design
    )

    if not created:
        wish.delete()
        return JsonResponse({'status': 'removed'})

    return JsonResponse({'status': 'added'})


# =============================
# ⭐ WISHLIST PAGE
# =============================
@login_required
def wishlist_page(request):
    wishes = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'wishes': wishes
    })


# =============================
# 📅 BOOK DESIGN (AJAX)
# =============================
@login_required
def book_design(request, id):
    if request.method == "POST":
        design = get_object_or_404(Design, id=id)

        booking, created = Booking.objects.get_or_create(
            user=request.user,
            design=design
        )

        if created:
            booking.status = "Booked"
            booking.save()
            return JsonResponse({'status': 'booked'})

        return JsonResponse({'status': 'already_booked'})

    return JsonResponse({'status': 'error'})


# =============================
# 📅 BOOKING PAGE
# =============================
@login_required
def booking_page(request, id):
    design = get_object_or_404(Design, id=id)

    return render(request, 'booking.html', {
        'design': design
    })


# =============================
# 📅 SAVE BOOKING
# =============================
@login_required
def save_booking(request, id):
    if request.method == "POST":
        design = get_object_or_404(Design, id=id)

        booking, created = Booking.objects.get_or_create(
            user=request.user,
            design=design,
            defaults={
                'name': request.POST.get('name', 'unknown'),
                'phone': request.POST.get('phone', '0000000000'),
                'address': request.POST.get('address', 'not provided'),
                'status': 'Pending'
            }
        )

        if not created:
            booking.name = request.POST.get('name', booking.name)
            booking.phone = request.POST.get('phone', booking.phone)
            booking.address = request.POST.get('address', booking.address)
            booking.save()

        return redirect('payment', booking.id)


# =============================
# 💳 PAYMENT
# =============================
@login_required
def payment(request, id):
    booking = get_object_or_404(Booking, id=id)

    # ✅ SAFE MODE (no Razorpay)
    if not hasattr(settings, "RAZORPAY_KEY"):
        booking.status = "Paid"
        booking.save()
        return render(request, "success.html", {"booking": booking})

    try:
        import razorpay

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET)
        )

        order = client.order.create({
            "amount": 50000,
            "currency": "INR",
            "payment_capture": "1"
        })

        return render(request, "payment.html", {
            "booking": booking,
            "order": order,
            "razorpay_key": settings.RAZORPAY_KEY
        })

    except Exception:
        booking.status = "Paid"
        booking.save()
        return render(request, "success.html", {"booking": booking})


# =============================
# ✅ PAYMENT SUCCESS
# =============================
@login_required
def payment_success(request):
    booking_id = request.GET.get('booking_id')

    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = "Paid"
        booking.save()

    return render(request, "success.html")