import datetime

from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

from persons.models import Person, Department, Organization, Role 


class Tag(models.Model):
    """
    A collection of tags for mapping to other models
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # keyword
    tagname = models.CharField(max_length=64)
    
    # definition / elaboration of keyword
    tagdefinition = models.TextField()

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.tagname,)

    def get_absolute_url(self):
        return reverse('covidskills:tag-view', kwargs={'pk': self.pk})

class Skill(models.Model):
    """
    A skill that can be drawn upon with minimal instruction required
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # keyword
    skillname = models.CharField("Skill name", max_length=64)
    
    # definition / elaboration of keyword
    skilldefinition = models.TextField("Skill definition")

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.skillname,)

    def get_absolute_url(self):
        return reverse('covidskills:skill-view', kwargs={'pk': self.pk})

class StudyField(models.Model):
    """
    A an area of expertise that someone has trained in.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # keyword
    fieldname = models.CharField("Name of field", max_length=64)
    
    # definition / elaboration of keyword
    fielddefinition = models.TextField("Description of field")

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.fieldname,)

    def get_absolute_url(self):
        return reverse('covidskills:field-view', kwargs={'pk': self.pk})

class Project(models.Model):
    """
    A project someone has been assigned to
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # keyword
    projectname = models.CharField("Project name", max_length=64)
    
    # definition / elaboration of keyword
    projectdefinition = models.TextField("Description of project")

    # PI / supervisor of project work. 
    pi = models.CharField("Project lead/supervisor", max_length=128)

    # priority of the project
    HIGHEST = "CO" 
    HIGH = "HI" 
    MEDIUM = "ME"
    LOW = "LO" 
    PRIORITY_CHOICES = (
            (HIGHEST, "Highest (COVID)"),
            (HIGH, "High"),
            (MEDIUM, "Medium"),
            (LOW, "Low"),
    )
    priority = models.CharField(
                            max_length=2,
                            choices = PRIORITY_CHOICES,
                            default = LOW,
    ) 

    # project type
    OPS = "OP" 
    COVID = "CO" 
    PROJECT = "PR"
    TYPE_CHOICES = (
            (OPS, "Operational"),
            (COVID, "COVID related"),
            (PROJECT, "Project"),
    )
    projecttype = models.CharField(
                            max_length=2,
                            choices = TYPE_CHOICES,
                            default = OPS,
    ) 
    
    # amount of time needed for the project
    timeneeded = models.PositiveIntegerField("Number of weeks needed", 
                                             null=True, blank=True)
    
    # link to further details 
    detailurl = models.URLField("Project URL", max_length=256, null=True, blank=True)
   
    # list of skills required for this project
    skillsrequired = models.ManyToManyField(Skill, verbose_name="Skills required",)
       
    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.projectname, self.pi)

    def get_absolute_url(self):
        return reverse('covidskills:project-view', kwargs={'pk': self.pk})

                
class RecordSheet(models.Model):
    """
    An entry for a person, to indicate their skills and availability
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE, 
                                      related_name="author_user")
 
    # workload spent on COVID-related activities (direct and indirect) 
    workloadcovid = models.IntegerField("COVID workload (%)")
    
    # workload spent on normal duties
    workloadother = models.IntegerField("Regular workload (%)")
    
    # time spent on 'filler' tasks or other replaceable activities
    workloadidle = models.IntegerField("Availability (%)")
    
    # number of days (rounded) that a person is working remotely
    remotetime = models.PositiveIntegerField("Days working remote (round up)", null=True, blank=True)
    
    # number of days each week a person could defer to work on COVID tasks
    deferdays = models.PositiveIntegerField("Days each week that can be deferred", 
                                    null=True, blank=True)
    
    # maximum number of weeks a person can defer their work
    deferlimit = models.PositiveIntegerField("Max weeks able to be deferred", 
                                     null=True, blank=True)
    
    # impact of deferring the person by this amount of time
    deferimpact = models.TextField("Impact of deferring work", 
                                    blank=True, null=True)
    
    # cwid of the person the record pertains to
    cwid = models.CharField("CWID", max_length=16, unique=True)
    
    # name of the person the record pertains to
    recordname = models.CharField("Employee name", max_length=256, unique=True)
    
    # list of skillsets the person has ability in
    skillsets = models.ManyToManyField( Skill, 
                                        verbose_name="Employee skills", 
                                        db_table="db_regskills_employee",
                                        blank=True, 
                                        related_name='regskills',
                                        )

    # list of skillsets the person is very strong in
    strongskills = models.ManyToManyField(  Skill, 
                                            verbose_name="Employee strong skills",
                                            db_table="db_strskills_employee", 
                                            blank=True, 
                                            related_name='strskills',
                                            )

    # list of fields the person has training in
    fieldstrained = models.ManyToManyField( StudyField, 
                                            verbose_name="Tertiary training",
                                            blank=True,
                                            )
    
    # best contact number
    bestnumber = models.CharField("Best contact number", max_length=32, 
                                    blank=True, null=True)
    
    # supervisor
    supervisor = models.ForeignKey(User, 
                                    on_delete=models.PROTECT, 
                                    related_name="record_supervisor",
                                    null=True, 
                                    blank=True)
    
    # projects that the user has been assigned to
    assignedprojects = models.ManyToManyField(Project, blank=True)
    
    # field to capture any other information
    comments = models.TextField(null=True, blank=True)

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}: {} skills {} assigned projects".format(self.recordname, 
                                                            len(self.skillsets.all()), 
                                                            len(self.assignedprojects.all()))

    def get_absolute_url(self):
        return reverse('covidskills:record-view', kwargs={'pk': self.pk})
        
        