from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML

from django import forms

from django.utils.translation import gettext_lazy as _

from persons.models import Person
from .models import Skill, StudyField, Tag, Project, RecordSheet

div_skills = Div(
                    Div('skillsets',
                        css_class='col-10'
                    ),
                    HTML("""
                            <a  href="{% url 'covidskills:skill-add' %}"
                                type="button" 
                                class="btn btn-success">
                                    Create new field
                            </a>
                        """
                    ),
                    css_class="row",
)

div_workload = Div(
                    Div('workloadcovid',
                        css_class='col-4',
                    ),
                    Div('workloadother',
                        css_class='col-4',
                    ),
                    Div('workloadidle',
                        css_class='col-4',
                    ),
                    css_class="row"
)


class RecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['fieldstrained'].label = "Fields you have been trained in"
        self.helper = FormHelper()
        self.helper.form_id = 'recordForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">User availability</div>',
                            'recordname',
                            div_workload,
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Skills and Training</div>',
                            div_skills,
                            'fieldstrained',
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Comments</div>',
                            'comments',
                            style="font-weight: bold;"
                    ),        
        )
    
    class Meta:
        model = RecordSheet
        fields = [  'recordname',
                    'workloadcovid',
                    'workloadother',
                    'workloadidle',
                    'skillsets',
                    'fieldstrained', 
                    'comments', 
                ]

        widgets =  {'recordname' : autocomplete.ModelSelect2(
                                        url='covidskills:autocomplete-publisher'
                                        ),  
                    'skillsets' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),  
                    'fieldstrained' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-field'
                                        ),                                      
                    }



class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['pi'].label = "Principal Investigator / Project Director"
        self.helper = FormHelper()
        self.helper.form_id = 'ProjectForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Project Form</div>',
                            'projectname',
                            'projectdefinition',
                            'pi',
                            'detailurl',
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Skills required for this project</div>',
                            'skillsrequired',                        
                            style="font-weight: bold;",
                    ),
        )
    
    class Meta:
        model = Project
        fields = [  'projectname',
                    'projectdefinition',
                    'pi',
                    'detailurl',
                    'skillsrequired',
                ]

        widgets =  {'skillsrequired' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),                                      
                    }
