# Generated by Django 5.0.4 on 2024-04-18 00:52

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('project', '0001_initial'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagesliderimages',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.AddField(
            model_name='hometvmanualstep',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual_step', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='hometvmanualstep',
            name='step_picture',
            field=models.ForeignKey(blank=True, help_text='Малюнок дло блоку Про нас', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='socialmediasettings',
            name='site',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site'),
        ),
        migrations.AddField(
            model_name='socialmedialink',
            name='site_setting',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_links', to='home.socialmediasettings'),
        ),
    ]
