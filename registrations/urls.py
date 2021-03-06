from django.urls import path

from .views import RegistrationsHomeView, RegistrationCreateView, \
    RegistrationOverview, RegistrationQuestionEditView, RegistrationDeleteView, \
    MinimalCategoryView, MinimalDeleteView
from .forms import QUESTIONS
from .blueprints import RegistrationBlueprint
from .models import ParticipantCategory

app_name = 'registrations'

urlpatterns = [
    path('', RegistrationsHomeView.as_view(), name='home'),
    path('new/', RegistrationCreateView.as_view(), name='new_registration'),
    path('<int:reg_pk>/', RegistrationOverview.as_view(), name='overview'),
    path('delete/<int:reg_pk>/', RegistrationDeleteView.as_view(),
         name='delete'),
    path('<int:reg_pk>/<str:question>/edit/<int:question_pk>/',
         RegistrationQuestionEditView.as_view(
             question_dict=QUESTIONS,
             parent_pk_arg='reg_pk'),
         name='edit_question'),
    path('<int:reg_pk>/<str:question>/create/',
         RegistrationQuestionEditView.as_view(
             question_dict=QUESTIONS,
             parent_pk_arg='reg_pk'),
         name='create_question'),
    path('<int:reg_pk>/categories/minimal/',
         MinimalCategoryView.as_view(),
         #parent_pk_arg='reg_pk',
         name='minimal_categories'
         ),
    path('delete/category/<int:pk>/',
         MinimalDeleteView.as_view(
             model=ParticipantCategory),
         #parent_pk_arg='reg_pk',
         name='minimal_delete'
         )
]
