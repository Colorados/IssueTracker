from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issues, Project
from .forms import IssueForm, SimpleSearchForm, ProjectForm, ProjectIssueForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
    template_name = 'issues/index.html'
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
    template_name = 'issues/issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        issue = get_object_or_404(Issues, pk=pk)
        context['issue'] = issue
        return context


class IssueEditView(LoginRequiredMixin, UpdateView):
    template_name = 'issues/issue_edit.html'
    form_class = IssueForm
    model = Issues

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.object.pk})


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'issues/issue_delete.html'
    model = Issues
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'projects/project_list_view.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'projects/project_detail.html'
    model = Project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    model = Project
    form_class = ProjectForm


class ProjectIssueCreateView(CreateView):
    model = Issues
    template_name = 'projects/project_issue_create.html'
    form_class = ProjectIssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        form.save_m2m()
        return redirect('project_detail', pk=project.pk)


class ProjectEditView(UpdateView):
    template_name = 'projects/project_edit.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    template_name = 'projects/project_delete.html'
    model = Project
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)