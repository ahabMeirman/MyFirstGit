from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import *

User = get_user_model()

