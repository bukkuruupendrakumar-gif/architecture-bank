from django.urls import path
from . import views

urlpatterns = [
    # 🏠 HOME
    path('', views.home, name="home"),

    # 🔐 AUTH
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # 📊 DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # 📂 CATEGORY → DESIGNS
    path('designs/<int:id>/', views.designs, name='designs'),

    # ❤️ LIKE
    path('like/<int:id>/', views.like_design, name='like'),

    # ⭐ WISHLIST (AJAX TOGGLE)
    path('wishlist/<int:id>/', views.wishlist_toggle, name='wishlist'),

    # ⭐ WISHLIST PAGE
    path('wishlist-page/', views.wishlist_page, name='wishlist_page'),

    # 📅 BOOK (AJAX QUICK BOOK)
    path('book/<int:id>/', views.book_design, name='book'),

    # 📅 BOOKING FORM (NEW FLOW)
    path('booking/<int:id>/', views.booking_page, name='booking'),
    path('save-booking/<int:id>/', views.save_booking, name='save_booking'),

    # 💳 PAYMENT
    path('payment/<int:id>/', views.payment, name='payment'),

    # ✅ SUCCESS PAGE
    path('success/', views.payment_success, name='success'),
]