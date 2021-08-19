from dal import autocomplete

from django.shortcuts import render, get_object_or_404

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User

from django.urls import reverse_lazy, reverse

from django.http import Http404
from .models import Skill, Tag, StudyField, Project, RecordSheet, Division

from .forms import ProjectForm, RecordSupervisorForm, RecordOwnerForm, AssignmentForm

import six 

##################################
######  SELF-UPDATE MIXIN   ######
##################################

class UserIsRecordOwner(object):
     """Verify that the current user is the owner of the Record."""
     def dispatch(self, request, *args, **kwargs):
         record = get_object_or_404(RecordSheet, pk=kwargs['pk'])
         if record.cwid != request.user.username:
             raise Http404
         return super(UserIsRecordOwner, self).dispatch(request, *args, **kwargs)

class UserIsRecordSupervisor(object):
     """Verify that the current user is the owner of the Record."""
     def dispatch(self, request, *args, **kwargs):
        record = get_object_or_404(RecordSheet, pk=kwargs['pk'])
         
        if request.user.has_perm('covidskills.change_recordsheet'):
            pass
        elif record.supervisor != request.user:
            raise Http404
        return super(UserIsRecordSupervisor, self).dispatch(request, *args, **kwargs)

class UserIsSupervisor(object):
    """Verify that the current user is the owner of the Record."""
    def dispatch(self, request, *args, **kwargs):
        records = RecordSheet.objects.filter(published=True
                                    ).filter(supervisor=request.user
                                    ).count()
        
        if request.user.has_perm('covidskills.change_recordsheet'):
            pass
        elif records < 1:
             raise Http404
        return super(UserIsSupervisor, self).dispatch(request, *args, **kwargs)

####################################
######  AUTOCOMPLETE  VIEWS   ######
####################################

class SkillAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Skill.objects.filter(published=True)

        if self.q:
            qs = qs.filter( 
                            Q(skillname__icontains=self.q) | 
                            Q(skilldefinition__icontains=self.q)
                            )
        return qs

class FieldAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = StudyField.objects.filter(published=True)

        if self.q:
            qs =  qs.filter(
                            Q(fieldname__icontains=self.q)
                            )
        return qs

class TagAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.filter(published=True)

        if self.q:
            qs =  qs.filter(
                            Q(tagname__icontains=self.q) | 
                            Q(tagdefinition__icontains=self.q)
                            )
        return qs

class ProjectAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.filter(published=True)

        if self.q:
            qs =  qs.filter(
                            Q(projectname__icontains=self.q) |
                            Q(projectdefinition__icontains=self.q)
            ) 
        return qs

class DivisionAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Division.objects.filter(published=True)

        if self.q:
            qs =  qs.filter(divisionname__icontains=self.q) 
        return qs
        
class UserAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return "{} {} ({})".format(item.first_name, item.last_name, item.username) 
                                     
        
    def get_queryset(self):
        qs = User.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(username__icontains=self.q) |
                            Q(first_name__icontains=self.q) |
                            Q(last_name__icontains=self.q)
            ) 
        return qs
        
###################
### Index views ###
###################

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        ds = Project.objects.filter(published=True)
        return ds
        
    def get_context_data(self, **kwargs):
        # get the record for the user
        own_record = RecordSheet.objects.filter(cwid=self.request.user)
        
        # get records of any staff user supervises
        staff_records = RecordSheet.objects.filter(supervisor=self.request.user
                                          ).order_by('recordname'
                                          )
        
        # get counts of other classes
        skill_count = Skill.objects.filter(published=True).count()
        record_count = RecordSheet.objects.filter(published=True).count()
        tag_count = Tag.objects.filter(published=True).count()
        field_count = StudyField.objects.filter(published=True).count()
        project_count = Project.objects.filter(published=True).count()
        
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({ 
                        'own_record'     : own_record,
                        'staff_records'  : staff_records,
                        'skill_count'    : skill_count, 
                        'record_count'   : record_count,
                        'tag_count'      : tag_count,
                        'field_count'    : field_count,
                        'project_count'  : project_count,
        })
        return context

class SkillIndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index_skills.html'
    context_object_name = 'skill_list'

    def get_queryset(self):
        ds = Skill.objects.filter(published=True
                         ).order_by('skillname'
                         )
        return ds
        
    def get_context_data(self, **kwargs):
        context = super(SkillIndexView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class RecordIndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index_records.html'
    context_object_name = 'record_list'

    def get_queryset(self):
        records = RecordSheet.objects.filter(published=True)
        return records
        
    def get_context_data(self, **kwargs):
        records = RecordSheet.objects.filter(published=True)
        
        # get records of any staff user supervises
        staff_records = RecordSheet.objects.filter(supervisor=self.request.user
                                          ).order_by('recordname'
                                          )

        # get list of all unique person supervisors
        supervisors = records.order_by('supervisor'
                            ).values_list('supervisor', flat=True
                            ).distinct(
                            )
        
        # determine if user is a supervisor
        if staff_records.count() < 1:
            is_supervisor = False
        else:
            is_supervisor = True
        
        context = super(RecordIndexView, self).get_context_data(**kwargs)
        context.update({
                        'supervisors'  : list(supervisors), 
                        'is_supervisor': is_supervisor,
                        'staff_records': staff_records, 
        })
        return context
        
class FieldIndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index_fields.html'
    context_object_name = 'field_list'

    def get_queryset(self):
        flds = StudyField.objects.filter(published=True)
        # kws.sort()
        return flds
        
    def get_context_data(self, **kwargs):
        context = super(FieldIndexView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class TagIndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index_tags.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        t = Tag.objects.filter(published=True)
        # ins.sort()
        return t
        
    def get_context_data(self, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class ProjectIndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'covidskills/index_projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        prjs = Project.objects.filter(published=True
                             ).order_by('projectname')

        return prjs
        
    def get_context_data(self, **kwargs):
        context = super(ProjectIndexView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
####################
### Detail views ###
####################

class SkillDetailView(LoginRequiredMixin, generic.DetailView):
    model = Skill
    template_name = 'covidskills/detail_skill.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(SkillDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [], 
        })
        return context
        
class FieldDetailView(LoginRequiredMixin, generic.DetailView):
    model = StudyField
    template_name = 'covidskills/detail_field.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(FieldDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [],  
        })
        return context

class TagDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Tag
    template_name = 'covidskills/detail_tag.html'

    def get_context_data(self, **kwargs):

        context = super(TagDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [],  
        })
        return context
        
class RecordDetailView(LoginRequiredMixin, generic.DetailView):
    model = RecordSheet
    template_name = 'covidskills/detail_record.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [],  
        })
        return context
        
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'covidskills/detail_project.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [],  
        })
        return context

class DivisionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Division
    template_name = 'covidskills/detail_division.html'
    
    def get_context_data(self, **kwargs):
        
        context = super(DivisionDetailView, self).get_context_data(**kwargs)
        context.update({'empty_list'    : [],  
        })
        return context

####################
### Create views ###
####################

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    fields = [  'skillname',
                'skilldefinition',
    ]
    template_name = "covidskills/basic_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user

        self.object.save()
        return super(SkillCreateView, self).form_valid(form)

class FieldCreateView(PermissionRequiredMixin, CreateView):
    model = StudyField
    fields = [  'fieldname',
                'fielddefinition',
    ]
    template_name = "covidskills/basic_form.html"
    permission_required = 'covidskills.add_studyfield'
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(FieldCreateView, self).form_valid(form)

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = [  'tagname',
                'tagdefinition',
    ]
    template_name = "covidskills/basic_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(TagCreateView, self).form_valid(form)

class RecordCreateView(UserIsSupervisor, LoginRequiredMixin, CreateView):
    model = RecordSheet
    form_class = RecordSupervisorForm
    template_name = "covidskills/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    """
    def get_initial(self):
        #return super(RecordCreateView, self).get_initial(form)
        return { 'cwid': self.request.user,
                 'recordname' : self.request.user.get_full_name(),
        }
    """    
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        # set publish to true
        self.object.published = True
        self.object.save()
        return super(RecordCreateView, self).form_valid(form)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "covidskills/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        # set publish to true
        self.object.published = True
        self.object.save()
        return super(ProjectCreateView, self).form_valid(form)


        
####################
### Update views ###
####################

class SkillUpdateView(PermissionRequiredMixin, UpdateView):
    model = Skill
    fields = [  'skillname',
                'skilldefinition',
    ]
    template_name = "covidskills/basic_form.html"
    permission_required = 'covidskills.change_skill'

class FieldUpdateView(PermissionRequiredMixin, UpdateView):
    model = StudyField
    template_name = "covidskills/basic_form.html"
    fields = [  'fieldname',
                'fielddefinition',
    ]
    permission_required = 'covidskills.change_studyfield'

class TagUpdateView(PermissionRequiredMixin, UpdateView):
    model = Tag
    template_name = "covidskills/basic_form.html"
    fields = [  'tagname',
                'tagdefinition',
    ]
    permission_required = 'covidskills.change_tag'
  
class RecordSupervisorUpdateView(UserIsRecordSupervisor, LoginRequiredMixin, UpdateView):
    model = RecordSheet
    form_class = RecordSupervisorForm
    template_name = "covidskills/basic_crispy_form.html"

class RecordOwnerUpdateView(UserIsRecordOwner, LoginRequiredMixin, UpdateView):
    model = RecordSheet
    form_class = RecordOwnerForm
    template_name = "covidskills/basic_crispy_form.html"


class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    "This is a record update view with limited fields"
    model = RecordSheet
    form_class = AssignmentForm
    template_name = "covidskills/basic_crispy_form.html"
    
class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "covidskills/basic_crispy_form.html"
    permission_required = 'covidskills.change_project'

class DivisionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Division
    fields = [  'divisionname',
                'divisiondefinition',
    ]
    template_name = "covidskills/basic_form.html"
    permission_required = 'covidskills.change_division'
 
 
##############################
######  SEARCH  VIEWS   ######
##############################

class FullSearch(LoginRequiredMixin, generic.TemplateView):
    template_name = 'covidskills/search_results.html'
    def post(self, request, *args, **kwargs):
        st = request.POST['srch_term']
        qs_sk = Skill.objects.all()
        qs_sk =  qs_sk.filter(  Q(skillname__icontains=st) | 
                                Q(skilldefinition__icontains=st)  
                     ).filter(published=True
        )
        qs_fi = StudyField.objects.all()
        qs_fi =  qs_fi.filter(  Q(fieldname__icontains=st) |
                                Q(fielddefinition__icontains=st) 
                      ).filter(published=True
        )
        qs_tg = Tag.objects.all()
        qs_tg = qs_tg.filter( Q(tagname__icontains=st) |
                              Q(tagdefinition__icontains=st)  
        )
        qs_pj = Project.objects.all()
        qs_pj = qs_pj.filter( Q(projectname__icontains=st) |
                              Q(projectdefinition__icontains=st) | 
                              Q(pi__icontains=st)
        ).filter(published=True)
        qs_re = RecordSheet.objects.all()
        qs_re = qs_re.filter( Q(recordname__icontains=st) |
                              Q(comments__icontains=st)  
        ).filter(published=True)
        context = { "search_str" : st,
                    "qs_skills": qs_sk,
                    "qs_fields": qs_fi,
                    "qs_tags": qs_tg,
                    "qs_projects": qs_pj,
                    "qs_records": qs_re,
        }
        return render(request, self.template_name, context)
        
############################
### Error handling views ###
############################
    
def handler403(request, exception, template_name="403.html"):
    """
    Error 403 = Forbidden 
    
    """
    response = render(request, "403.html")
    response.status_code = 403
    return response
    
def handler404(request, exception, template_name="404.html"):
    """
    Error 404 = Not found 
    
    """
    response = render(request, "404.html")
    response.status_code = 404
    return response
        