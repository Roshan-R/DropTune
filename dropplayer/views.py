from django.shortcuts import render
from django.http import HttpResponse
import os, glob
from .qrcodegen import qrgen
from .forms import MusicUpload, saveNewSong, songComplete
# Create your views here.
def get_song_list():
    """
    Returns a list of the names of all the songs present in the static/dropplayer/songs folder
    """
    #for changing directory to the directory of this python script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #list which will contain the names of all the files
    namelist = []
    for files in (sorted(glob.glob('./static/dropplayer/songs/*.mp3'), key=os.path.getmtime)):
        filename = "/static/dropplayer/songs/"+str(files[26:]) #26 cz I had to trim away all the path text that was preceding it.
        namelist.append(filename)
    return namelist

def index(request):
    """
    Renders DropTune homepage
    """
    imgdata, ip = qrgen()
    return render(request, 'dropplayer/index.html', {'qrcode': imgdata, 'ip': ip})

def player(request):
    """
    Renders the music player page
    """
    #list of the names of all the songs
    song_list = get_song_list()
    if request.method == "POST":
        form = songComplete(request.POST)
        if form.is_valid():
            print(request.POST['complete'])
            if request.POST['complete'] == 'ended':
                os.chdir(os.path.dirname(os.path.abspath(__file__)))
                delsong = 'static/dropplayer/songs/'+song_list[0]
                os.remove(song_list[0][1:])
                song_list = song_list[1:]
            return render(request, 'dropplayer/player.html', {'songlist': song_list, 'endconfirm': form})
    else:
        form = songComplete()
    return render(request, 'dropplayer/player.html', {'songlist': song_list, 'endconfirm': form})

def dj(request):
    """
    Renders and manages the uploaded song of the DJ page
    """
    if request.method == "POST":
        form = MusicUpload(request.POST, request.FILES)
        if form.is_valid():
            saveNewSong(request.FILES['newsong'])
            return render(request, 'dropplayer/dj.html', {'musicform':form})
    else:
        form = MusicUpload()
    return render(request, 'dropplayer/dj.html', {'musicform':form})