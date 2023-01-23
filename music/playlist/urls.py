from django.urls import path

# local modules
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('confirm/<int:tok>/', views.confirmAccount, name='confirm'),
    path('forgot-password/', views.forgotPassword, name='forgotpass'),
    path('change-password/<str:pk>', views.changePassword, name='changepass'),
    path('book-appointment/', views.bookAppointment, name='book-appointment'),
    path('download-track/', views.downloadTrack, name='selectsong'),
    path('my_track/', views.downloadMyTrack, name='downloadtrack'),
    path('my_album/', views.downloadMyAlbum, name='downloadmyalbum'),
    path('downloads/', views.download, name='downloads'),
    path('music/', views.selectMusic, name='music'),
    path('albums/', views.selectAlbums, name='albums'),
    path('tracks/<str:pk>', views.artistSingle, name='tracks'),
    path('purchased/', views.purchased, name='purchased'),
    path('download-album/', views.downloadAlbum, name='downloadalbum'),
    path('checkout/', views.payCheckout, name='checkout'),
    path('success/', views.paySuccessful, name='success'),
    path('failure/', views.payFailed, name='failure'),
    path('log-album-downloads/', views.logAlbumDownloads, name='logalbumdownloads'),
    path('paystack_callback/', views.payPaystackCallback, name='paystackcallback'),
    path('donate/', views.makeDonation, name='donate'),
]