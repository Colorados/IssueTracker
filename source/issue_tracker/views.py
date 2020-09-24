from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView, ListView
from .base_views import FormView as CustomFormView
from .models import Issues
from .forms import IssueForm, SimpleSearchForm
from django.db.models import Q


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'issues'
    paginate_by = 10
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Issues.objects.all()

        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(summary__icontains=search) | Q(description__icontains=search))
        return data.order_by('-created_at')

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
        self.issue = form.save()
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
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

