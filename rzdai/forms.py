from django import forms

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(label='Выберите видео файл')