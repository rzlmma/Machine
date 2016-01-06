# -- coding: utf8 --*--

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import json
import uuid
from machine.system.models import User


def book_list(request):
    return render_to_response('book/book_list.html', locals(), context_instance=RequestContext(request))


def book_add(request):
    print "***********BOOKADD***************"
    return render_to_response('book/book_add.html', locals(), context_instance=RequestContext(request))


def upload_file(request):
     if request.method == 'POST':
        response = {"success": True, "error": "上传成功!"}
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        try:
            DIR = "media/book/"
            file_obj = request.FILES.get('uploadFile', None)
            fileName = str(uuid.uuid4()) + str(file_obj)
            dst_file_path = DIR + fileName
            dst_file = open(dst_file_path, 'wb')
            content = file_obj.read()
            dst_file.write(content)
            dst_file.close()

            return HttpResponse(json.dumps(response), content_type="application/json")

        except Exception, e:
            response["success"] = False
            response["error"] = unicode(e)
            return HttpResponse(json.dumps(response), content_type="application/json")


#
# def _upload(file):
#     '''''图片上传函数'''
#     if file:
#         path=os.path.join(settings.MEDIA_ROOT,'upload')
#         file_name=str(uuid.uuid1())+".jpg"
#         path_file=os.path.join(path,file_name)
#         parser = ImageFile.Parser()
#         for chunk in file.chunks():
#             parser.feed(chunk)
#         img = parser.close()
#         try:
#             if img.mode != "RGB":
#                 img = img.convert("RGB")
#             img.save(path_file, 'jpeg',quality=100)
#         except:
#             return False
#         return True
#     return False
#
#
# def uploadify_script(request):
#     response=HttpResponse()
#     response['Content-Type']="text/javascript"
#     ret="0"
#     file = request.FILES.get("Filedata",None)
#     if file:
#         if _upload(file):
#             ret="1"
#         ret="2"
#     response.write(ret)
#     return response