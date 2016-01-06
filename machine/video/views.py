# --*-- coding: utf-8 --*--
import datetime
import logging
from django.shortcuts import render_to_response
from django.template import RequestContext

logger = logging.getLogger('django')


def video_list(request):
    return render_to_response('video/video_list.html', locals(), context_instance=RequestContext(request))