# Generated by Django 5.1.4 on 2024-12-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_review_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="description",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="review_title",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
    ]
