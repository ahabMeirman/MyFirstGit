from PIL import Image # crop
from django import forms
from django.core.files import File
from .models import Photo

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        photo = super(PhotoForm, self).save()
        # это данные ширины и высоты изоброжения 
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file) # получаем изоброжение
        cropped_image = image.crop((x, y, w+x, h+y)) # и вырезаем его 
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        print('ahab')
        print(resized_image)
        resized_image.save(photo.file.path)

        return photo