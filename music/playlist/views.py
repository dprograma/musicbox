import datetime
import json
from multiprocessing import context
import os
import random
import string
from django.shortcuts import redirect, render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from . models import Collection, User, Song, Album, downloadLog, Transaction, GuestUser
from decouple import config
from . import sendmail
from django.core import serializers
from .serializers import AlbumSerializer, SongSerializer, CollectionSerializer
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, MyUserCreationForm, UpdateUserPasswordForm, DonationForm
from .functions import tolog
from django.shortcuts import get_object_or_404
from django import template
register = template.Library()
from django.db.models import Q
from django.db import connection

# Create your views here.

# Retrieve information from environment variables
url = config("init_trans_url")
token = config("token")
callback_url = config("callback_url")
verify_trans_url = config("verify_trans_url")
site = config("site")


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
                mytracks = [i.title for i in Collection.objects.filter(owner_id=user.id, purchased=1, type="Track")]
                myalbums = [i.title for i in Collection.objects.filter(owner_id=user.id, purchased=1, type="Album")]
                request.session['track_collection'] = list(set(mytracks))
                request.META['track_collection'] = list(set(mytracks))
                request.session['album_collection'] = list(set(myalbums))
                request.META['album_collection'] = list(set(myalbums))
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            tolog("loginuser method: "+e)
            messages.error(request, 'User does not exist.')
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
                subject = 'Account Creation for Chucks Peters Music'
                emailmsgs = sendmail.EmailMessages(tok, site, user.username)
                emailMsg, alt = emailmsgs.registerMsg()
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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    seek = Song.objects.filter(Q(album__album_name__icontains=q)|
    Q(title__icontains=q))
    album = Album.objects.all().first()
    # songs = Song.objects.all()
    context = {"songs": seek, "album": album}
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
    try:
        user = User.objects.get(email=pk)
        form = UpdateUserPasswordForm(instance=user)
        if request.method == 'POST':
            form = UpdateUserPasswordForm(request.POST, instance=user)
            if form.is_valid:
                form.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('login')
    except Exception as e:
        tolog(str(e))
        e_str = ""
        err = list(form.errors.values())
        for i in range(len(err)):
            if err[i - 1][0] == err[i][0]:
                err[i][0] = err[i - 1][0]
            e_str = e_str + err[i][0]
        if e_str == '':
            e_str = 'You cannot submit a form with empty fields.'
        messages.error(request, e_str+"\n")
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
    try:
        if request.method == 'POST':
            track_id = request.POST['song']
            track = Song.objects.get(id=track_id)
            amount = str(int(track.amount))
            title = track.title
            type = "Track"
            artist = track.artist
            formatted_amount = str(int(amount))+"00"
            username = request.user.username
            if request.session:
                request.session['payload'] = {"id":track_id, "amount": amount, "username": username,
                                        "formatted_amount": formatted_amount, "title": title, "artist": artist, "type": type, "mode": "purchase"}
            else:
                request.META['payload'] = {"id":track_id, "amount": amount, "username": username,
                                        "formatted_amount": formatted_amount, "title": title, "artist": artist, "type": type, "mode": "purchase"}
            return redirect('checkout')
    except Exception as e:
        tolog("MY TRACK ERROR: line 232 in downloadMyTrack. "+str(e))


def downloadMyAlbum(request):
    try:
        if request.method == 'POST':
            album_id = request.POST['album']
            album = Album.objects.get(id=album_id)
            amount = str(int(album.amount))
            title = album.album_name
            type = "Album"
            artist = album.artist
            formatted_amount = str(int(amount))+"00"
            username = request.user.username
            if request.session:
                request.session['payload'] = {"id":album_id, "amount": amount, "username": username,
                                        "formatted_amount": formatted_amount, "title": title, "artist": artist, "type": type, "mode": "purchase"}
            else:
                request.META['payload'] = {"id":album_id, "amount": amount, "username": username,
                                        "formatted_amount": formatted_amount, "title": title, "artist": artist, "type": type, "mode": "purchase"}
            return redirect('checkout')
    except Exception as e:
        tolog("MY ALBUM ERROR: "+str(e))


@login_required(login_url='login')
def download(request):
    email = request.user.email
    user = User.objects.get(email=email)
    downloads = user.downloads.all()
    context = {"downloads": downloads}
    return render(request, 'playlist/download.html', context)


def selectMusic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    seek = Song.objects.filter(Q(album__album_name__icontains=q)|
    Q(title__icontains=q))
    album = Album.objects.all().first()
    context = {"songs": seek, "album": album}
    return render(request, 'playlist/selectmusic.html', context)


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
    try:
        if request.session['user']:
            albumuser = request.session['user']
            tolog("SESSION ALBUM USER"+str(albumuser))
        elif request.META['user']:
            albumuser = request.META['user']
            tolog("META ALBUM USER"+str(albumuser))
        
        user = User.objects.get(id=albumuser['userid'])
        album = request.POST.get('album')
        tracks = request.POST.get('tracks')
        json_tracks = json.loads(tracks)
        tracks_fields = json.loads(json_tracks)
        for track in tracks_fields:
            fields = track['fields']
            tolog("ALBUM FIELDS: "+str(fields))
            download = downloadLog(
                album_name=album,
                owner=user,
                artist=fields['artist'],
                title=fields['title'],
                album_id=fields['album'],
                album_img_path=fields['image'],
                track_path=fields['mp3'],
                created_at=fields['created_at'],
                meta=fields,
            )
            download.save()
        return redirect('albums')
    except Exception as e:
        tolog(str(e))


def artistSingle(request, pk):
    alb = Album.objects.get(id=pk)
    album_tracks = alb.tracks.all()
    context = {"tracks": album_tracks}
    return render(request, 'playlist/artist_single.html', context)


@login_required(login_url='login')
def purchased(request):
    context = {}
    return render(request, 'playlist/purchased.html', context)


def payCheckout(request):
    try:
        if request.method == 'POST':
            artist = request.POST['artist']
            title = request.POST['title']
            username = request.POST['username']
            amount = request.POST['amount']
            formatted_amount = request.POST['formatted_amount']
            if request.POST['email']:
                email = request.POST['email']
                password = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
                # guestuser = GuestUser.objects.create(name=username, email=email)
                check_existing = User.objects.filter(username=username) or User.objects.filter(email=email).exists()
                if check_existing:
                    user = User.objects.get(email=email)
                else:
                    newuser = User(username=username, email=email, is_loggedin=True, is_registered=True)
                    newuser.save()
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    emailmsgs = sendmail.EmailMessages(None, site, username)
                    emailMsg, alt = emailmsgs.itemPurchasedMsg(password)
                    subject = "Thank You For Your Patronage [Chucks Peters Music]"
                    sendmail.SendMail(email, subject, emailMsg, alt)
            else:
                email = request.user.email     
            # print("SESSION PAYLOAD: ", request.session['payload'])  

            if request.session:
                request.session['user'] = {"email": user.email, "username": user.username, "userid": user.id}
            else:
               request.META['user'] = {"email": user.email, "username": user.username, "userid": user.id}
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
    except Exception as e:
        tolog(str(e))

    context = {}
    return render(request, 'playlist/checkout.html', context)


def payPaystackCallback(request):
    ref_id = request.GET.get('reference')
    tolog("ref_id: "+str(ref_id))
    verify_url = verify_trans_url+ref_id
    tolog("verify_url: "+verify_url)
    headers = {
        'Authorization': 'Bearer '+token
    }
    tolog("AUTHORIZATION HEADER: "+str(headers))
    response = requests.get(verify_url, headers=headers)
    tolog("RESPONSE: "+str(response))
    resp = json.loads(response.text)
    tolog("CALLBACK URL RESP: "+str(resp))
    status = resp['data']['status']
    tolog("RESPONSE STATUS: "+str(status))
    request.session['payment_verification'] = resp
    print("I got here1!")
    if request.session:
        track = request.session['payload']
        user = request.session['user']
    else:
        track = request.META['payload']
        user = request.META['user']
    print("I got here2!")
    # tolog("PAYLOAD: "+str(track))
    print("PAYLOAD: ", track)
    mode = track['mode']
    tolog("MODE: "+str(mode))
    try: 
        if status == "success":
            if mode == "purchase":
                # print("REQUEST USER: ", request.user)
                # user_id = request.user.id
                user_id = user['userid']
                user = User.objects.get(id=user_id)
                title = track['title'].strip()
                type = track['type']
                collection = Collection(owner=user, type=type, purchased=True, title=title)
                collection.save()
                track_instance = get_object_or_404(Song, id=track['id'])
                collection.songlist.add(track_instance)
                transactionlog(status=resp['status'], message=resp['message'], data=resp['data'])
                mytracks = [i.title for i in Collection.objects.filter(owner_id=user.id, purchased=1, type="Track")]
                myalbums = [i.title for i in Collection.objects.filter(owner_id=user.id, purchased=1, type="Album")]
                request.session['track_collection'] = mytracks
                request.META['track_collection'] = mytracks
                request.session['album_collection'] = myalbums
                request.META['album_collection'] = myalbums
                return redirect('success')
            elif mode == "donate":
                transactionlog(status=resp['status'], message=resp['message'], data=resp['data'])
                return redirect('success')
        else:
            return redirect('failure')
    except Exception as e:
        tolog("PAYSTACK CALLBACK ERROR: "+str(e))


def paySuccessful(request):
    context = {}
    return render(request, 'playlist/success.html', context)

def payFailed(request):
    context = {}
    return render(request, 'playlist/failure.html', context)


def transactionlog(**kwargs):
    newspost, _ = Transaction.objects.get_or_create(**kwargs)
    for attr, value in kwargs.items():
        setattr(newspost, attr, value)
    newspost.save()
    

@register.filter(name='is_in_list')
def is_in_list(value, given_list):
    return True if value in given_list else False

    
def makeDonation(request):
    donation = DonationForm()
    if request.user:
        user = request.user
    if request.method == 'POST':
        email = request.POST['email']
        amount = request.POST['amount']
        formatted_amount = str(int(amount))+"00"
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
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
            request.session['payload'] = {"mode": "donate"}
            return redirect(auth_url)            
    context = {"donation": donation, "user": user}
    return render(request, 'playlist/donate.html', context)