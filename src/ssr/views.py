from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
from .models import SsrFiels



class SsrFilesDetailView(DetailView):
	model = SsrFiels
