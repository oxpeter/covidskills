from django.contrib import admin

from .models import Skill, StudyField, Tag, RecordSheet, Project, Division

# customize the look of the admin site:
admin.site.site_header = 'Covid Skillsets and Projects Management Page'
admin.site.site_title = "DCMP"
admin.site.index_title = "Back end administration"

# create custom actions:
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Publish selected items"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = "Un-publish selected items"

def make_curated(modeladmin, request, queryset):
    queryset.update(curated=True)
make_curated.short_description = "Mark selected items as curated"


# customize the individual model views:
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("skillname",
                    "skilldefinition",
                    "curated",
                    "published",
                    )
    list_filter = ('curated', 'published',)
    search_fields = ('skillname', 'skilldefinition',)
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ("fieldname", 
                    "fielddefinition",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('fieldname', 'fielddefinition', )
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("tagname", 
                    "tagdefinition",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('tagname','tagdefinitions')
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(RecordSheet)
class RecordSheetAdmin(admin.ModelAdmin):
    list_display = ("recordname", 
                    "bestnumber",
                    "curated",
                    "published",
    )
    list_filter =  ('curated', 
                    'published',
                    'supervisor', 
                    'recorddivision'
                    )
    search_fields = ('recordname', 'comments')
    actions = [make_published, make_unpublished, make_curated]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("projectname", 
                    "pi",
                    "detailurl",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('projectname', 'projectdefinition', 'pi')
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(Division)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("divisionname", 
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('divisionname',)
    actions = [make_published, make_unpublished, make_curated]