# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bTree', '0004_user_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='owner',
            field=models.ForeignKey(to='bTree.User'),
        ),
    ]
