from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
from .base_views import FormView as CustomFormView
from .models import Issues
from .forms import IssueForm


class IndexView(View):
    def get(self, request):
        data = Issues.objects.all()
        return render(request, 'index.html', context={'issues': data})


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        issue = get_object_or_404(Issues, pk=pk)
        context['issue'] = issue
        return context


class IssueCreateView(CustomFormView):
    template_name = 'issue_create.html'
    form_class = IssueForm

    def form_valid(self, form):
        data = {}
        types = form.cleaned_data.pop('type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        self.issue = Issues.objects.create(**data)
        self.issue.types.set(types)
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})

class IssueEditView(FormView):
    template_name = 'issue_edit.html'
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'status', 'types':
            initial[key] = getattr(self.issue, key)
        initial['created_at'] = self.issue.created_at.strftime('H:i:s')
        return initial

    def form_valid(self, form):
        types = form.cleaned_data.pop('type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.issue, key, value)
        self.issue.save()
        self.issue.types.set(types)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issues, pk=pk)

def issue_delete_view(request, pk):
    issue = get_object_or_404(Issues, pk=pk)
    if request.method == 'GET':
        return render(request, 'issue_delete.html', context={'issue': issue})
    elif request.method == 'POST':
        issue.delete()
        return redirect('home')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

