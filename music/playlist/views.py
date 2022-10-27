import datetime
import json
from multiprocessing import context
import os
import random
from django.shortcuts import redirect, render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from . models import Collection, User, Song, Album, downloadLog
from decouple import config
from . import sendmail
from django.core import serializers
from .serializers import AlbumSerializer, SongSerializer
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, MyUserCreationForm, UpdateUserPasswordForm

# Create your views here.

# Retrieve information from environment variables
url = config("init_trans_url")
token = config("token")
callback_url = config("callback_url")
verify_trans_url = config("verify_trans_url")


def loginUser(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        try:
            if check_password(password, user.password):
                user.is_loggedin = True
                user.save()
                login(request, user)
                collection = Collection.objects.filter(
                    owner_id=user.id).first()
                if collection:
                    album = Album.objects.filter(albumlist_id=collection.id)
                else:
                    album = {}
                return redirect(reverse('home'), kwargs={"collection": album})
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, 'User does not exist.'+str(e))
    context = {'page': page}
    return render(request, 'playlist/login_register.html', context)


def registerUser(request):
    page = "Sign Up"
    if request.user.is_authenticated:
        return redirect('home')
    try:
        form = MyUserCreationForm()
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.is_registered = True
                tok = str(random.randint(111111, 99999999999)) + str(datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")).replace(':', '').replace(',', '').replace('-', '').replace(' ', '')
                user.token = tok
                user.save()
                # Send email notification
                to = user.email
                subject = 'Account Creation for Barbarshop'
                emailMsg = f'''<div style="background: #eee;padding: 10px;">
                                <div style="max-width: 500px;margin: 0px auto;font-family: sans-serif;text-align: center;background: #fff;border-radius: 5px;overflow: hidden;">
                                    <div style="width: 100%;background: #fc9700;">
                                        <h1 style="color: #fff;text-decoration: none;margin: 0px;padding: 10px 0px;">Barbarshop</h1>
                                    </div>
                                    <div style="color: #000;padding: 10px;margin-top: 10px;">
                                        Hello {user.username}, <br/>Thank you for registering with us at Barbarshop. Please login to your dashboard with your email and password
                                        <div style="padding: 10px;margin: 10px 0px;color: #000;background: #eee;border-radius: 5px; height: 80px;">
                                        Account Confirmation:
                                            <p><a style="margin:10px; padding: 10px; width: 100px; height: 45px; background-color: #fc9700; font-size: 35px; color: #fff;font-weight: 700; border-radius: 5px; text-decoration: none;" href='http://127.0.0.1:8000/confirm/{tok}'>
                                                Confirm
                                            </a></p>
                                        </div>
                                    </div>
                                    <div style="color: #000; padding-bottom: 10px;">
                                        However, if this registration process was not initiated by you, kindly ignore this mail.
                                        <br />
                                        If you have encounter any problem while creating your account, feel free to <a href="http://localhost:8000/contact" style="text-decoration: none; color: #bf5794;">contact us</a>
                                    </div>
                                </div>
                            </div>'''
                alt = '''Hello user, Thank you for registering with us at Barbarshop. Please login to your dashboard with your email and dashboard. <br />  However, if this registration process was not initiated by you, kindly ignore this mail.'''
                sendmail.SendMail(to, subject, emailMsg, alt)
                messages.success(
                    request, f"You account was created successfully. You will receive an message shortly at {user.email} to confirm your email.")
                # end email notification
                return redirect('home')
            else:
                e_str = ""
                err = list(form.errors.values())
                for i in range(len(err)):
                    if err[i - 1][0] == err[i][0]:
                        err[i][0] = err[i - 1][0]
                    e_str = e_str + err[i][0]
                if e_str == '':
                    e_str = 'You cannot submit a form with empty fields.'
                messages.error(request, e_str+"\n")
        context = {'form': form, 'page': page}
        return render(request, 'playlist/login_register.html', context)
    except Exception as e:
        messages.error(
            request, "Something went wrong during registration." + str(e))


def confirmAccount(request, tok):
    user = User.objects.get(token=tok)
    if user.is_active == True:
        messages.error(request, "Your account is already confirmed.")
        return redirect('login')
    elif user.is_active == False and user.is_registered == True:
        user.is_active = True
        user.save()
        messages.success(
            request, "Your account has been confirmed successfully.")
        return redirect('login')
    else:
        messages.error(request, "Invalid user account")
        return redirect('register')


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    songs = Song.objects.all()
    context = {"songs": songs}
    return render(request, 'playlist/home.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'playlist/update_user.html', {'form: form'})


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'playlist/profile.html', context)


@login_required(login_url='login')
def bookAppointment(request):
    context = {}
    return render(request, 'playlist/appointment.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            if user.is_registered == True:
                return redirect('changepass', pk=email)
            else:
                messages.error(request, 'Incorrect email address')
        except Exception as e:
            messages.error(request, 'Incorrect email address')
    context = {"page": "Forgot password"}
    return render(request, 'playlist/forgotpassword.html', context)


def changePassword(request, pk):
    user = User.objects.get(email=pk)
    form = UpdateUserPasswordForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserPasswordForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('login')
    context = {"email": pk, "form": form, "page": "Create your new password"}
    return render(request, 'playlist/changepassword.html', context)


@csrf_exempt
def downloadTrack(request):
    if request.method == 'POST':
        song = Song.objects.all()
        single = serializers.serialize('json', song)
        context = {"song": json.dumps(single)}
        return JsonResponse(context)


def downloadMyTrack(request):
    if request.method == 'POST':
        track_id = request.POST['song']
        track = Song.objects.get(id=track_id)
        amount = str(int(track.amount))
        title = track.title
        artist = track.artist
        formatted_amount = str(int(amount))+"00"
        email = request.user.email
        username = request.user.username
        request.session['payload'] = {"amount": amount, "email": email, "username": username,
                                      "formatted_amount": formatted_amount, "title": title, "artist": artist}
        return redirect('checkout')


@login_required(login_url='login')
def download(request):
    email = request.user.email
    user = User.objects.get(email=email)
    downloads = user.downloads.all()
    context = {"downloads": downloads}
    return render(request, 'playlist/download.html', context)


def selectMusic(request):
    songs = Song.objects.all()
    context = {"songs": songs}
    return render(request, 'playlist/selectmusic.html', context)


# @login_required(login_url='login')
def selectAlbums(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, 'playlist/selectalbums.html', context)


@csrf_exempt
def downloadAlbum(request):
    id = request.POST.get('id')
    album = Album.objects.get(id=id)
    album_tracks = album.tracks.all()
    serialized = serializers.serialize('json', album_tracks)
    context = {"tracks": json.dumps(
        serialized), "album": json.dumps(album.album_name)}
    return JsonResponse(context)


@csrf_exempt
def logAlbumDownloads(request):
    id = request.user.id
    user = User.objects.get(id=id)
    album = request.POST.get('album')
    tracks = request.POST.get('tracks')
    json_tracks = json.loads(tracks)
    tracks_fields = json.loads(json_tracks)
    for track in tracks_fields:
        fields = track['fields']
        download = downloadLog.objects.create(
            album_name=album,
            owner=user,
            artist=fields['artist'],
            title=fields['title'],
            album_id=fields['album'],
            album_img_path=fields['image'],
            track_path=fields['mp3'],
            created_at=fields['created_at'],
            songlist=fields['songlist'],
            meta=fields,
        )
        download.save()
    return redirect('albums')


def artistSingle(request, pk):
    alb = Album.objects.get(id=pk)
    album_tracks = alb.tracks.all()
    context = {"tracks": album_tracks}
    return render(request, 'playlist/artist_single.html', context)


@login_required(login_url='login')
def purchased(request):
    context = {}
    return render(request, 'playlist/purchased.html', context)


@login_required(login_url='login')
def payCheckout(request):
    if request.method == 'POST':
        artist = request.POST['artist']
        title = request.POST['title']
        username = request.user.username
        amount = request.POST['amount']
        formatted_amount = request.POST['formatted_amount']
        email = request.user.email
        payload = json.dumps(
            {"email": email, "amount": formatted_amount, "callback_url": callback_url})
        headers = {
            'Access-Control-Request-Method': '',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
        response = requests.post(url, headers=headers, data=payload)
        resp = json.loads(response.text)
        auth_url = resp['data']['authorization_url']
        return redirect(auth_url)

    context = {}
    return render(request, 'playlist/checkout.html', context)


def payPaystackCallback(request):
    ref_id = request.GET.get('reference')
    verify_url = verify_trans_url+ref_id
    headers = {
        'Authorization': 'Bearer '+token
    }
    response = requests.get(verify_url, headers=headers)
    resp = json.loads(response.text)
    status = resp['data']['status']
    request.session['payment_verification'] = resp
    if status == "success":
        return redirect('success')
    else:
        return redirect('failure')


def paySuccessful(request):
    context = {}
    return render(request, 'playlist/success.html', context)

def payFailed(request):
    context = {}
    return render(request, 'playlist/failure.html', context)
    
