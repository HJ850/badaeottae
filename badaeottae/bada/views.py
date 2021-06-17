import csv

from django.shortcuts import render, redirect
from django.utils.timezone import now
from rest_framework import viewsets

from bada import bigdataPro
from bada.models import Test, Beach, Score, Jellyfish, Weather, Plankton, Imrang, Songjung, Haeundae
from bada.serializers import TestSerializer


# Create your views here.
UPLOAD_DIR='D:/LHJ/src/upload/'

class TestViewSet(viewsets.ModelViewSet):
    queryset=Test.objects.all()
    serializer_class=TestSerializer
    
def home(request):
    return render(request, 'home.html')

def table_list(request):
    return render(request, 'table_list.html')

def graph_list(request):
    return render(request, 'graph_list.html')

def beach_insert(request):
    data=[]
    bigdataPro.beach(data)
    for row in data:
        dto=Beach(beach=row[0],link_addr=row[1],link_tel=row[2],lat=row[3],lon=row[4])
        dto.save()
    return redirect('/')

def pred_insert(request):
    im_path=UPLOAD_DIR+'imrang_2021.csv'
    im_info = open(im_path, 'r', encoding='utf-8')
    im_csv = csv.reader(im_info)
    for row in im_csv :
        dto=Imrang(pred_date=row[0],at=row[1],wt=row[2],ws=row[3],swh=row[4],score=row[5])
        dto.save()
        
    song_path=UPLOAD_DIR+'songjung_2021.csv'
    song_info = open(song_path, 'r', encoding='utf-8')
    song_csv = csv.reader(song_info)
    for row in song_csv :
        dto=Songjung(pred_date=row[0],at=row[1],wt=row[2],ws=row[3],swh=row[4],score=row[5])
        dto.save()
        
    haeundae_path=UPLOAD_DIR+'haeundae_2021.csv'
    haeundae_info = open(haeundae_path, 'r', encoding='utf-8')
    haeundae_csv = csv.reader(haeundae_info)
    for row in haeundae_csv :
        dto=Haeundae(pred_date=row[0],at=row[1],wt=row[2],ws=row[3],swh=row[4],score=row[5])
        dto.save()
        
    return redirect('/')

def score_insert(request):
    data=[]
    row=bigdataPro.weather_search(data)
    im_score=bigdataPro.beach_scoring(row[0][0], row[0][1], row[0][2], row[0][3])
    song_score=bigdataPro.beach_scoring(row[0][4], row[0][5], row[0][6], row[0][7])
    hae_score=bigdataPro.beach_scoring(row[0][8], row[0][9], row[0][10], row[0][11])
    #dto=Imrang(wt=row[0][0],at=row[0][1],ws=row[0][2],swh=row[0][3],score=im_score,pred_date=now())
    #dto.save()
    im_dto=Score(beach="임랑",wt=row[0][0],at=row[0][1],ws=row[0][2],swh=row[0][3],score=im_score,date=now())
    im_dto.save()
    #dto=Songjung(wt=row[0][4],at=row[0][5],ws=row[0][6],swh=row[0][7],score=im_score,pred_date=now())
    #dto.save()
    song_dto=Score(beach="송정",wt=row[0][4],at=row[0][5],ws=row[0][6],swh=row[0][7],score=song_score,date=now())
    song_dto.save()
    #dto=Haeundae(wt=row[0][8],at=row[0][9],ws=row[0][10],swh=row[0][11],score=im_score,pred_date=now())
    #dto.save()
    hae_dto=Score(beach="해운대",wt=row[0][8],at=row[0][9],ws=row[0][10],swh=row[0][11],score=hae_score,date=now())
    hae_dto.save()
    return render(request,'weather_search.html',{'im_water_temp':row[0][0],'im_air_temp':row[0][1],'im_windspd':row[0][2],'im_wavehigh':row[0][3],
                                                 'song_water_temp':row[0][4],'song_air_temp':row[0][5],'song_windspd':row[0][6],'song_wavehigh':row[0][7],
                                                 'hae_water_temp':row[0][8],'hae_air_temp':row[0][9],'hae_windspd':row[0][10],'hae_wavehigh':row[0][11],
                                                 'weather':row[0][12],'im_score':im_score,'song_score':song_score,'hae_score':hae_score})
    
def jellyfish_insert(request):
    path=UPLOAD_DIR+'jellyfish.csv'
    jfinfo=open(path, 'r', encoding='utf-8')
    jfinfo_csv = csv.reader(jfinfo)
    for row in jfinfo_csv:
        dto=Jellyfish(name=row[0],ratio=row[1],map=row[2],date=row[3])
        dto.save()
    return redirect('/')

def weather_insert(request):
    path=UPLOAD_DIR+'weather.csv'
    weatherinfo = open(path, 'r', encoding='utf-8')
    weatherinfo_csv = csv.reader(weatherinfo)
    for row in weatherinfo_csv :
        dto=Weather(tos=row[0],vof=row[1],wt=row[2],salt=row[3],swh=row[4],
                    ws=row[5],at=row[6],ap=row[7],ratio=row[8],true=row[9])
        dto.save()
    return redirect('/')

def plankton_insert(request):
    path=UPLOAD_DIR+'plankton.csv'
    planktoninfo = open(path, 'r', encoding='utf-8')
    planktoninfo_csv = csv.reader(planktoninfo)
    for row in planktoninfo_csv :
        dto=Plankton(tos=row[0],wt=row[1],yogak=row[2].replace('\ufeff',''),moak=row[3],dangak=row[4],nbd=row[5],jigak=row[6],
                    chuck=row[7],yagwang=row[8],jf=row[9],LARVAE=row[10],others=row[11],organic=row[12],ratio=row[13],true=row[14])
        dto.save()
    return redirect('/')

def weather_heatmap(request):
    bigdataPro.weather_heatmap()
    return render(request,'graph_list.html')

def jf_clustering(request):
    bigdataPro.jf_clustering()
    return render(request,'graph_list.html')

def plankton_heatmap(request):
    bigdataPro.plankton_heatmap()
    return render(request,'graph_list.html')

def moak_nomura(request):
    bigdataPro.moak_nomura()
    return render(request,'graph_list.html')

def chucksek_nomura(request):
    bigdataPro.chucksek_nomura()
    return render(request,'graph_list.html')