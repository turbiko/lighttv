# Generated by Django 5.0.4 on 2024-04-09 10:13

import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeOnlineTv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('online_provider_url', models.URLField(default='#')),
                ('logo_provider', models.ForeignKey(blank=True, help_text='Логотип провайдера', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_tv', to='wagtailcore.page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('about_name', models.CharField(blank=True, max_length=50, null=True)),
                ('about_title', models.CharField(blank=True, max_length=50, null=True)),
                ('about_description', wagtail.fields.RichTextField(blank=True, null=True)),
                ('manual_name', models.CharField(blank=True, max_length=150, null=True)),
                ('manual_title', models.CharField(blank=True, max_length=250, null=True)),
                ('manual_text', models.CharField(blank=True, max_length=550, null=True)),
                ('online_name', models.CharField(blank=True, max_length=150, null=True)),
                ('online_title', models.CharField(blank=True, max_length=250, null=True)),
                ('online_text', wagtail.fields.RichTextField(blank=True, null=True)),
                ('about_picture', models.ForeignKey(blank=True, help_text='малюнок дло блоку Про нас', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageSliderImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_images', to='wagtailcore.page')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeTvManualStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('about_name', models.CharField(blank=True, max_length=150, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual_step', to='wagtailcore.page')),
                ('step_picture', models.ForeignKey(blank=True, help_text='малюнок дло блоку Про нас', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialMediaSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField(default='#', help_text='Facebook URL')),
                ('instagram', models.URLField(default='#', help_text='Instagram URL')),
                ('tiktok', models.URLField(default='#', help_text='Tiktok URL')),
                ('youtube', models.URLField(default='#', help_text='YouTube URL')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
