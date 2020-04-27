from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from translate.forms import PhotoForm
from translate.models import Photo


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'multiple_upload/progress_bar_upload.html', {'photos': photos_list})

    def post(self, request):
        #time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            print('data')
            print(data)
            print(data.loaded)
            print('data')
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

