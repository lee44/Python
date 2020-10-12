from django.urls import path
from . import views #from . means the current directory views.py is in

# urls.py defines how to handle different url patterns such as path/5 or path/5/results

# In real Django projects, there might be five, ten, twenty apps or more. How does Django differentiate the URL names between them? The answer is namespace.
# app_name sets the application namespace so each url path can be references by polls:index, polls:detail
app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]