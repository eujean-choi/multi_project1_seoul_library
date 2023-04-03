from django.shortcuts import render, redirect
# from pjt1_seoullibrary.visualization import visual as v
from visualization import visual


def index(request):
    contexts = dict()
    contexts['intro_map'] = visual.intro_map()
    contexts['rent_ages'] = visual.rent_ages()
    contexts['gu_lib_budget'] = visual.gu_lib_budget()
    contexts['income_lib'] = visual.income_lib

    return render(request, 'index.html', contexts)

def newloc(request):
    contexts = dict()
    contexts['income_lib'] = visual.income_lib
    contexts['satisfaction'] = visual.satisfaction()
    contexts['lib_visitor'] = visual.lib_visitor()
    contexts[''] = ''
    contexts[''] = ''
    contexts['age_percent'] = visual.age_percent()

    return render(request, 'newloc.html', contexts)

def disadv(request):
    contexts = dict()
    contexts['disadv_budget_users'] = visual.disadv_budget_users()
    contexts['disadv_av_budget_income'] = visual.disadv_av_budget_income()
    contexts['corr_heatmap'] = visual.corr_heatmap()

    return render(request, 'disadv.html', contexts)