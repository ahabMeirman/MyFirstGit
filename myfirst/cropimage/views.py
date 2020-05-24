from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.
# def image(request):
# 	return render(request, 'photo_list.html')

def photo_list(request):
	photos = Photo.objects.all()

	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return redirect ('photo_list_url')

	else:
		form = PhotoForm()

	return render(request, 'photo_list.html', context = { 'form' : form, 'photos' : photos })