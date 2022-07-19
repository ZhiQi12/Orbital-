from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Module, Issue
from .forms import CreateNewMod
from .main import scrape_n_posts, RFR_avg_rating, emotion_chart, convert_emotion_chart_to_str
import time
import schedule
from pandas import *

def home(response):
    return render(response, "moderate/home.html", {})

#def index(response, code):
#    ls = Module.objects.filter(code=code).first()
#    return render(response, "moderate/list.html", {"ls":ls})

def find(response):
    return render(response, "moderate/find.html")

def moderate(request):
    mydict = {}
    text = request.POST.get('mod')
    text = text.upper()
    mydict["text"] = text
    try:
        #check if mod is in database
        comments = Module.objects.get(code=text)
        mydict["rating"] = getattr(comments, "rating")
        mydict["comment1"] = getattr(comments, "comment1")
        mydict["comment2"] = getattr(comments, "comment2")
        mydict["comment3"] = getattr(comments, "comment3")
        mydict["emotions"] = list(map(float, getattr(comments, "emotions").split(",")))
        Module.objects.filter(code=text).update(searched=
                                                getattr(comments, "searched") + 1)
    except:
        #perform MODeRATE if not in database
        try:
            tpl = scrape_n_posts(text, 3)
            mydict["rating"] = RFR_avg_rating(tpl[0])
            mydict["emotions"] = emotion_chart(tpl[0])
            
        except Exception as e:
            print(e)
            return render(request, "moderate/error.html", {})
        #comments
        try:
            mydict["comment1"] = tpl[1][0]
        except:
            mydict["comment1"] = ""
        try:
            mydict["comment2"] = tpl[1][1]
        except:
            mydict["comment2"] = ""
        try:
            mydict["comment3"] = tpl[1][2]
        except:
            mydict["comment3"] = ""

        #save into database
        mod = Module(code = text, 
                    rating = mydict["rating"],
                    comment1 = mydict["comment1"],
                    comment2 = mydict["comment2"],
                    comment3 = mydict["comment3"],
                    searched = 1,
                    emotions = convert_emotion_chart_to_str(mydict["emotions"])
                    )
        mod.save()
    global cmod
    cmod = text
    return render(request, "moderate/comments.html", mydict)

# # unsure of whr to put this
# def job(request):
#     modCodesLst = read_csv("C:/Orbital/Orbital_Moderate/mods.csv")["Module Code"].tolist()
#     for modCode in modCodesLst:
#         # save into database
#         mydict = {}
#         text = request.POST.get('mod')
#         text = text.upper()
#         mydict["text"] = text
#         tpl = scrape_n_posts(text, 3)
#         mydict["rating"] = RFR_avg_rating(tpl[0])
#         mydict["emotions"] = emotion_chart(tpl[0])
#         mod = Module(code = text, 
#             rating = mydict["rating"],
#             comment1 = mydict["comment1"],
#             comment2 = mydict["comment2"],
#             comment3 = mydict["comment3"],
#             searched = 1,
#             emotions = convert_emotion_chart_to_str(mydict["emotions"])
#             )
#         mod.save()

# def hello():
#     print("hello")

# def runjob(request):
#     #run job() function everyday at 1am
#     schedule.every().day.at("11:18").do(hello())   


def view(response):
    return render(response, "moderate/view.html")

def rating(response):
    mydict = {}
    top3 = Module.objects.order_by("-rating")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["rate1"] = getattr(top3[0], "rating")
    mydict["rate2"] = getattr(top3[1], "rating")
    mydict["rate3"] = getattr(top3[2], "rating")
    return render(response, "moderate/rating.html", mydict)

def searched(response):
    mydict = {}
    top3 = Module.objects.order_by("-searched")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["search1"] = getattr(top3[0], "searched")
    mydict["search2"] = getattr(top3[1], "searched")
    mydict["search3"] = getattr(top3[2], "searched")
    return render(response, "moderate/searched.html", mydict)

def problem(request):
    return render(request, "moderate/problem.html")

def thankyou(request):
    text = request.POST.get('problem')
    issue = Issue(code=cmod,message=text)
    issue.save()
    return render(request, "moderate/thankyou.html")
    