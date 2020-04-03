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
    skillname = models.CharField(max_length=64)
    
    # definition / elaboration of keyword
    skilldefinition = models.TextField()

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
    fieldname = models.CharField(max_length=64)
    
    # definition / elaboration of keyword
    fielddefinition = models.TextField()

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
    projectname = models.CharField(max_length=64)
    
    # definition / elaboration of keyword
    projectdefinition = models.TextField()

    # PI / supervisor of project work. 
    pi = models.CharField(max_length=128)
    
    # link to further details 
    detailurl = models.URLField(max_length=256, null=True, blank=True)
   
    # list of skills required for this project
    skillsrequired = models.ManyToManyField(Skill)
   
    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.projectname,, self.pi)

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
    
    # name of the person the record pertains to
    recordname = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="recordname_user")
    
    # list of skillsets the person has expertise in
    skillsets = models.ManyToManyField(Skill)

    # list of fields the person has training in
    fieldstrained = models.ManyToManyField(StudyField)
    
    # best contact number
    bestnumber = models.CharField(max_length=32)
    
    # supervisor
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="supervisor_user",
                                    null=True,
                                    blank=True,
                                    )
    
    # projects that the user has been assigned to
    assignedprojects = models.ManyToManyField(Project)
    
    # field to capture any other information
    comments = models.TextField()

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}: {} skills {} assigned projects".format(self.recordname, 
                                                            len(self.skillsets), 
                                                            len(self.assignedprojects))

    def get_absolute_url(self):
        return reverse('covidskills:record-view', kwargs={'pk': self.pk})
        
        