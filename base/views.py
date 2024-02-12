import json
import os
import shutil

from django.shortcuts import render, redirect
from .forms import UserForm, UploadForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Company, Upload
from django.views.generic.base import TemplateView
from .models import FileChunkUpload
from django.core.serializers import serialize
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.conf import settings
from django.core import management
from django.core.management.commands import loaddata

def login_user(request):
    try:
        page = 'login-user'

        if request.user.is_authenticated:
            return redirect('chunked-upload-start')

        if request.method == 'POST':
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            try:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Username or password does not existed")
            except:
                messages.error(request, "User is not existed")
        context = {'page': page}
        return render(request, 'login_register.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse("Failed to register user {}".format(e))


def logout_user(request):
    logout(request)
    return redirect('login-user')


def register_user(request):
    try:
        page = 'register-user'
        form = UserForm()
        try:
            if request.method == 'POST':
                form = UserForm(request.POST)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.email = user.email.lower()
                    user.save()
                    login(request, user)
                    return redirect('chunked-upload-start')

            context = {'form': form}

        except Exception as e:
            messages.error(request, e)

        return render(request, 'login_register.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse("Failed to register user {}".format(e))


def get_all_users_and_status(request):
    """Gets all user names and their status."""

    users = User.objects.all()
    user_names_and_status = []
    for user in users:
        user_names_and_status.append({
          "username": user.username,
          "status": user.is_active,
        })
    context = {'user_names_and_status': user_names_and_status}

    return render(request, 'users_status.html', context=context)

class ChunkedUploadDemo(TemplateView):
    template_name = 'upload_file.html'

class MyChunkedUploadView(ChunkedUploadView):
    model = FileChunkUpload
    field_name = 'the_file'

    def on_completion(self, uploaded_file, request):
        # Allow non authenticated users to make uploads
        pass


class FileChunkUploadCompleteView(ChunkedUploadCompleteView):
    model = FileChunkUpload

    def on_completion(self, uploaded_file, request):
        try:
            if request.method == 'POST':
                get_data = FileChunkUpload.objects.filter(upload_id=request.POST.get('upload_id'))
                serialized_data = json.loads(serialize('json', get_data))
                print(serialized_data)
                self.upload_data_to_database(data=serialized_data)
        except Exception as e:
            return HttpResponse("Error while serializing data {}".format(e))

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}

    def upload_data_to_database(self, data):
        try:
            get_filename = ((data[0]).get('fields')).get('filename')
            get_filepath = ((data[0]).get('fields')).get('file')
            filename = os.path.join(settings.MEDIA_ROOT, get_filename)
            filepath = os.path.join(settings.MEDIA_ROOT, get_filepath)
            shutil.copy(filepath, filename)

            result = management.call_command('add_csv', filename)

            return result
        except Exception as e:
            print(e)
            return HttpResponse("Error while uploading csv data to database {}".format(e))


