from django.shortcuts import render
from django.conf import settings

import os

# Create your views here.

def gallery(request):
    image_list = []
    suffix = ['.jpg', '.png', '.jpeg', '.gif']
    path = os.path.join(settings.MEDIA_ROOT, 'images')
    file_list = os.listdir(path)
    for f in file_list:
        if os.path.splitext(f)[1] in suffix:
            image_list.append(settings.MEDIA_URL + 'images/' + f)

    return render(request, 'gallery/index.html', context={'image_list':image_list})
