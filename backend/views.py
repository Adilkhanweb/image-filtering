from django.shortcuts import render, redirect
from backend.forms import UploadForm
from django.views.generic import *

from backend.models import Upload


def ConverterShowView(request):
    return render(request, 'tabler/index.html', {"form": UploadForm()})


class ConverterView(CreateView):
    model = Upload
    fields = ('image', 'action')
    template_name = 'tabler/form.html'

    def form_valid(self, form):
        c = form.save()
        return redirect('detail', c.id)


class ConverterDetailView(DetailView):
    model = Upload
    template_name = 'tabler/result.html'

    def get_object(self, queryset=None):
        return Upload.objects.get(id=self.kwargs.get("id"))
