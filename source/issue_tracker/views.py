from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .base_views import FormView as CustomFormView
from .models import Issues, Project
from .forms import IssueForm, SimpleSearchForm, ProjectForm, ProjectIssueForm
from django.db.models import Q


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


class IssueCreateView(CustomFormView):
    template_name = 'issues/issue_create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})

class IssueEditView(UpdateView):
    template_name = 'issues/issue_edit.html'
    form_class = IssueForm
    model = Issues

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.object.pk})


class IssueDeleteView(DeleteView):
    template_name = 'issues/issue_delete.html'
    model = Issues
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ProjectsListView(ListView):
    template_name = 'projects/project_list_view.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    template_name = 'projects/project_detail.html'
    model = Project


class ProjectCreateView(CreateView):
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
