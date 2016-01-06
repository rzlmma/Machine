# --*-- coding: utf-8 --*--
import datetime
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from machine.deco import require_login
from machine.photography.models import Photo
from machine.system.models import User

logger = logging.getLogger('django')


def photo_list(request):
    photo_list = Photo.objects.all()
    return render_to_response('photography/photo_list.html', locals(), context_instance=RequestContext(request))


@require_login
def photo_add(request):
    if request.method == "GET":
        return render_to_response('photography/photo_add.html', locals(), context_instance=RequestContext(request))

    else:
        if request.POST.get('photo_link') != '':
            photo_link = request.POST.get('photo_link')
        if request.POST.get('photo_description') != '':
            description = request.POST.get('description')
        if request.session.get('_auth_user_id'):
            session_user_id = request.session.get('_auth_user_id')
            author = User.objects.get(pk=session_user_id)

        upload_time = datetime.datetime.now()
        print photo_link, description

        Photo.objects.create(author=author, photo_link=photo_link, description=description, upload_time=upload_time)
        return HttpResponseRedirect('/')


def photo_vote(request):
    try:
        flag = request.POST.get('flag')
        photo_id = request.POST.get('photo_id')
        photo = Photo.objects.get(pk=photo_id)
        if flag == "vote_favor":
            if not request.session.get('has_favored'):
                print request.session.get('has_favored')
                favor_cnt = photo.favor_cnt + 1
                photo.favor_cnt = favor_cnt
                photo.save()
                request.session['has_favored'] = True
            else:
                print request.session.get('has_favored')
                favor_cnt = photo.favor_cnt - 1
                photo.favor_cnt = favor_cnt
                photo.save()
                request.session['has_favored'] = False
            return HttpResponseRedirect('/')

        elif flag == "vote_dislike":
            if not request.session.get('has_disliked'):
                dislike_cnt = photo.dislike_cnt + 1
                photo.dislike_cnt = dislike_cnt
                photo.save()
                request.session['has_disliked'] = True
            else:
                dislike_cnt = photo.dislike_cnt - 1
                photo.dislike_cnt = dislike_cnt
                photo.save()
                request.session['has_disliked'] = False
            return HttpResponseRedirect('/')

    except Exception as e:
        print e



