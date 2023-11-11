from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import os
from .forms import VideoUploadForm
from PIL import Image, ImageDraw, ImageFont
import cv2
import torch
from torchvision import transforms
import torch.nn as nn
from torchvision.models import resnext101_32x8d
from collections import Counter
from django.http import JsonResponse
from .prep import process_video
import asyncio

def index(request):
    result = None
    most_common_label = None

    label_mapping = {
        0: 'крутит колесо (cartwheel)',
        1: 'ловит мяч (catch)',
        2: 'хлопает (clap)',
        3: 'лезет (climb)',
        4: 'ныряет вниз (dive)',
        5: 'с мечом (draw_sword)',
        6: 'показывает дриблинг мячом (dribble)',
        7: 'фехтует (fencing)',
        8: 'крутит сальто (flic_flac)',
        9: 'играет в гольф (golf)',
        10: 'стоит на руках (handstand)',
        11: 'получает удар (hit)',
        12: 'прыгает (jump)',
        13: 'что-то поднимает (pick)',
        14: 'pour',
        15: 'pullup',
        16: 'push',
        17: 'pushup',
        18: 'shoot_ball',
        19: 'sit',
        20: 'situp',
        21: 'swing_baseball',
        22: 'sword_exercise',
        23: 'throw'
    }

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']

            # Создаем временное место и сохраняем видеофайл в него
            with open('temp_video.mp4', 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Вызываем функцию process_video и передаем результат в переменную result
            most_common_label = process_video('temp_video.mp4')  # Update most_common_label
            print(most_common_label)

            # Заменяем числовую метку на соответствующую строку из словаря
            most_common_label = label_mapping.get(most_common_label, 'Unknown')
    else:
        form = VideoUploadForm()

    return render(request, 'index.html', {'form': form, 'result': result, 'most_common_label': most_common_label})

