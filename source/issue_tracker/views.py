from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.views.generic import View, TemplateView
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


class IssueCreateView(View):
    def get(self, request):
        form = IssueForm()
        return render(request, "issue_create.html", context={'form': form})

    def post(self, request):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            issue = Issues.objects.create(**data)
            return redirect('issue_view', pk=issue.pk)
        else:
            return render(request, 'issue_create.html', context={'form': form})


class IssueEditView(TemplateView):
    template_name = 'issue_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        issue = get_object_or_404(Issues, pk=pk)
        initial = {}
        for key in 'summary', 'description', 'status', 'type':
            initial[key] = getattr(issue, key)
        initial['created_at'] = issue.created_at.strftime('H:i:s')
        form = IssueForm(initial=initial)
        context['issue'] = issue
        context['form'] = form
        return context

    def post(self, request, pk):
        issue = get_object_or_404(Issues, pk=pk)
        form = IssueForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(issue, key, value)
            issue.save()
            return redirect('issue_view', pk=issue.pk)
        else:
            return self.render_to_response(context={'issue': issue, 'form': form})


def issue_delete_view(request, pk):
    issue = get_object_or_404(Issues, pk=pk)
    if request.method == 'GET':
        return render(request, 'issue_delete.html', context={'issue': issue})
    elif request.method == 'POST':
        issue.delete()
        return redirect('home')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

