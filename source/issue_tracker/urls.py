from django.urls import path
from issue_tracker.views import IndexView, IssueView, IssueEditView, \
    IssueDeleteView, ProjectsListView, ProjectDetailView, ProjectCreateView, ProjectIssueCreateView, \
    ProjectEditView, ProjectDeleteView

app_name = 'issue_tracker'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue_view'),
    path('issue/<int:pk>/edit/', IssueEditView.as_view(), name='issue_edit'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    path('projects/', ProjectsListView.as_view(), name='project_list_view'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/new', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/issue/new', ProjectIssueCreateView.as_view(), name='project_issue_create'),
    path('project/<int:pk>/edit/', ProjectEditView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]