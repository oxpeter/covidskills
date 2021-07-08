from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'covidskills'
urlpatterns = [ 
    # index showing top items and search bar:
    path('', views.IndexView.as_view(), name='index'),
    path('skills', views.SkillIndexView.as_view(), name='skills'),
    path('fields', views.FieldIndexView.as_view(), name='fields'),
    path('tags', views.TagIndexView.as_view(), name='tags'),
    path('records', views.RecordIndexView.as_view(), name='records'),
    path('projects', views.ProjectIndexView.as_view(), name='projects'),
    
    # autocomplete functions:
    path('autocomplete-skill', 
        views.SkillAutocomplete.as_view(), 
        name='autocomplete-skill',
        ),
    path('autocomplete-field', 
        views.FieldAutocomplete.as_view(), 
        name='autocomplete-field',
        ),
    path('autocomplete-tag', 
        views.TagAutocomplete.as_view(),
        name='autocomplete-tag',
        ),
    path('autocomplete-project', 
        views.ProjectAutocomplete.as_view(),
        name='autocomplete-project',
        ),
    path('autocomplete-record', 
        views.ProjectAutocomplete.as_view(),
        name='autocomplete-record',
        ),
    path('autocomplete-user', 
        views.UserAutocomplete.as_view(),
        name='autocomplete-user',
        ),
    path('autocomplete-division', 
        views.DivisionAutocomplete.as_view(),
        name='autocomplete-division',
        ),


    # detail views
    path('skills/<int:pk>', views.SkillDetailView.as_view(), name='skill-view'),
    path('fields/<int:pk>', views.FieldDetailView.as_view(), name='field-view'),
    path('tags/<int:pk>', views.TagDetailView.as_view(), name='tag-view'),
    path('records/<int:pk>', views.RecordDetailView.as_view(), name='record-view'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project-view'),
    path('divisions/<int:pk>', views.DivisionDetailView.as_view(), name='division-view'),
    
    # create views
    path('skills/add', views.SkillCreateView.as_view(), name='skill-add'),
    path('fields/add', views.FieldCreateView.as_view(), name='field-add'),
    path('tags/add', views.TagCreateView.as_view(),name='tag-add'),
    path('records/add', views.RecordCreateView.as_view(), name='record-add'),
    path('projects/add', views.ProjectCreateView.as_view(), name='project-add'),
    
    # update views
    path('skills/update/<int:pk>', views.SkillUpdateView.as_view(),
         name='skill-update'
    ),
    path('fields/update/<int:pk>', views.FieldUpdateView.as_view(), 
         name='field-update'
    ),
    path('tags/update/<int:pk>', views.TagUpdateView.as_view(), 
         name='tag-update'
    ),
    path('records/update/<int:pk>', views.RecordOwnerUpdateView.as_view(), 
         name='record-update'
    ),
    path('records/superupdate/<int:pk>', views.RecordSupervisorUpdateView.as_view(), 
         name='record-superupdate'
    ),
    path('records/assign/<int:pk>', views.AssignmentUpdateView.as_view(), 
         name='record-assign'
    ),
    path('projects/update/<int:pk>', views.ProjectUpdateView.as_view(), 
         name='project-update'
    ),
    path('divisions/update/<int:pk>', views.DivisionUpdateView.as_view(), 
         name='division-update'
    ),
    
    # search view:
    path('search/all', views.FullSearch.as_view(), name="full-search"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


