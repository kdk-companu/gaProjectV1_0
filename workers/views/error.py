from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView


def error_pageNotFound_404(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена.</h1>")


def error_errorServer_500(request, exception):
    return HttpResponseNotFound("ошибка сервера")


def error_noAccess_403(request, exception):
    #if not request.user.is_staff:
    #    print('проверка на права')
    return render(request, "error_403.html")



def error_error_400(request, exception):
    return HttpResponseNotFound("невозможно обработать запрос")
