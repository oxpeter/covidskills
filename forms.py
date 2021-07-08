from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML, Field

from django import forms

from django.utils.translation import gettext_lazy as _

from persons.models import Person
from .models import Skill, StudyField, Tag, Project, RecordSheet, Division

div_skills = Div(
                    Div('skillsets',
                        css_class='col-10'
                    ),
                    HTML("""
                            <a  href="{% url 'covidskills:skill-add' %}"
                                type="button" 
                                class="btn btn-success btn-sml">
                                    Create new skill
                            </a>
                        """
                    ),
                    css_class="row",
)
div_name = Div(
                    Div('cwid',
                        css_class='col-2',
                    ),
                    Div('recordname',
                        css_class='col-8',
                    ),
                    Div('bestnumber',
                        css_class='col-2',
                    ),
                    css_class="row"
)


div_super = Div(
                Div('supervisor',
                    css_class='col-4',
                ),
                Div('recorddivision',
                    css_class='col-8',
                ),
                css_class="row"
)

def three_equal(ONE,TWO,THREE):
    div_thirds = Div(
                        Div(ONE,
                            css_class='col-4',
                        ),
                        Div(TWO,
                            css_class='col-4',
                        ),
                        Div(THREE,
                            css_class='col-4',
                        ),
                        css_class="row"
    )
    return div_thirds

class RecordSupervisorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordSupervisorForm, self).__init__(*args, **kwargs)
        self.fields['cwid'].label = "CWID"
        #self.fields['cwid'].initial = self.request.user
        self.fields['recordname'].label = "Full name"
        #self.fields['skillsets'].label = ";".join(dir(self.fields['cwid']))
        self.fields['skillsets'].label = "Employee skills"
        self.fields['fieldstrained'].label = "Fields you have a tertiary qualification in (Bachelors, Masters, PhD, etc)"
        self.helper = FormHelper()
        self.helper.form_id = 'recordForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">User availability</div>',
                            div_name,
                            div_super,
                            three_equal("remotetime", "deferdays","deferlimit"),
                            "deferimpact",
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Skills and Training</div>',
                            div_skills,
                            'strongskills',
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
        fields = [  'cwid',
                    'recordname',
                    'supervisor',
                    'recorddivision', 
                    'bestnumber',
                    "remotetime", 
                    "deferdays",
                    "deferlimit",
                    'deferimpact',
                    'skillsets',
                    'strongskills',
                    'fieldstrained', 
                    'comments', 
                ]

        widgets =  {'skillsets' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),
                    'strongskills' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),
                    'fieldstrained' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-field'
                                        ),  
                    'supervisor' : autocomplete.ModelSelect2(
                                        url='covidskills:autocomplete-user'
                                        ),    
                    'recorddivision' : autocomplete.ModelSelect2(
                                        url='covidskills:autocomplete-division'
                                        ),                                                                            
                    }


class RecordOwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordOwnerForm, self).__init__(*args, **kwargs)
        self.fields['cwid'].label = "CWID"
        self.fields['recordname'].label = "Full name"
        self.fields['skillsets'].label = "Employee skills"
        self.fields['fieldstrained'].label = "Fields you have a tertiary qualification in (Bachelors, Masters, PhD, etc)"
        self.helper = FormHelper()
        self.helper.form_id = 'recordForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Field('cwid', readonly=True),
                    Fieldset('<div class="alert alert-info">User details for ' + "{} ({})".format(self.instance.recordname, self.instance.cwid) + '</div>',
                            'recordname',
                            'bestnumber',
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Skills and Training</div>',
                            div_skills,
                            'strongskills',
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
        fields = [  'cwid',
                    'recordname',
                    'bestnumber',
                    'skillsets',
                    'strongskills',
                    'fieldstrained', 
                    'comments', 
                ]

        widgets =  {'skillsets' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),
                    'strongskills' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),
                    'fieldstrained' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-field'
                                        ),                                                                              
                    }
                    
class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['assignedprojects'].label = "List of projects user is assigned to."
        self.helper = FormHelper()
        self.helper.form_id = 'assignmentForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Assign or remove projects for ' + str(self.instance.recordname) + '</div>',
                            'assignedprojects',
                            'comments',
                            style="font-weight: bold;",
                    ),
        )
    
    class Meta:
        model = RecordSheet
        fields = [  'assignedprojects', 
                    'comments', 
                ]

        widgets =  {'assignedprojects' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-project'
                                        ),                                     
                    }


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['pi'].label = "Project lead / supervisor"
        self.helper = FormHelper()
        self.helper.form_id = 'ProjectForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Project Form</div>',
                            'projectname',
                            'projectdefinition',
                            'pi',
                            three_equal('priority', 'projecttype', 'timeneeded'),
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
                    'priority', 
                    'projecttype', 
                    'timeneeded',
                    'detailurl',
                    'skillsrequired',
                ]

        widgets =  {'skillsrequired' : autocomplete.ModelSelect2Multiple(
                                        url='covidskills:autocomplete-skill'
                                        ),                                      
                    }
