"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from issue_tracker.views import IndexView, IssueView, IssueCreateView, IssueEditView, \
    IssueDeleteView, ProjectsListView, ProjectDetailView, ProjectCreateView, ProjectIssueCreateView, \
    ProjectEditView, ProjectDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue_view'),
    path('issue/new/', IssueCreateView.as_view(), name='issue_create'),
    path('issue/<int:pk>/edit/', IssueEditView.as_view(), name='issue_edit'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    path('projects/', ProjectsListView.as_view(), name='project_list_view'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/new', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/issue/new', ProjectIssueCreateView.as_view(), name='project_issue_create'),
    path('project/<int:pk>/edit/', ProjectEditView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete')
]
