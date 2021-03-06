# Generated by Django 2.1.4 on 2020-04-03 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('projectname', models.CharField(max_length=64)),
                ('projectdefinition', models.TextField()),
                ('pi', models.CharField(max_length=128)),
                ('detailurl', models.URLField(blank=True, max_length=256, null=True)),
                ('curated', models.BooleanField(blank=True, null=True)),
                ('published', models.BooleanField(blank=True, null=True)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecordSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('workloadcovid', models.IntegerField(verbose_name='COVID workload (%)')),
                ('workloadother', models.IntegerField(verbose_name='Regular workload (%)')),
                ('workloadidle', models.IntegerField(verbose_name='Availability (%)')),
                ('bestnumber', models.CharField(max_length=32)),
                ('comments', models.TextField()),
                ('curated', models.BooleanField(blank=True, null=True)),
                ('published', models.BooleanField(blank=True, null=True)),
                ('assignedprojects', models.ManyToManyField(to='covidskills.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('skillname', models.CharField(max_length=64)),
                ('skilldefinition', models.TextField()),
                ('curated', models.BooleanField(blank=True, null=True)),
                ('published', models.BooleanField(blank=True, null=True)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudyField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('fieldname', models.CharField(max_length=64)),
                ('fielddefinition', models.TextField()),
                ('curated', models.BooleanField(blank=True, null=True)),
                ('published', models.BooleanField(blank=True, null=True)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_creation', models.DateField(auto_now_add=True)),
                ('record_update', models.DateField(auto_now=True)),
                ('tagname', models.CharField(max_length=64)),
                ('tagdefinition', models.TextField()),
                ('curated', models.BooleanField(blank=True, null=True)),
                ('published', models.BooleanField(blank=True, null=True)),
                ('record_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recordsheet',
            name='fieldstrained',
            field=models.ManyToManyField(to='covidskills.StudyField'),
        ),
        migrations.AddField(
            model_name='recordsheet',
            name='record_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recordsheet',
            name='recordname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordname_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recordsheet',
            name='skillsets',
            field=models.ManyToManyField(to='covidskills.Skill'),
        ),
        migrations.AddField(
            model_name='recordsheet',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='skillsrequired',
            field=models.ManyToManyField(to='covidskills.Skill'),
        ),
    ]
