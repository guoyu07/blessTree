# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bTree', '0002_auto_20160130_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_plant',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tree',
            name='content',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='tree',
            name='type',
            field=models.IntegerField(verbose_name='\u64cd\u4f5c\u7c7b\u578b', choices=[(0, '\u81ea\u5df1\u6d47\u6c34'), (1, '\u7b2c\u4e00\u6b21\u5206\u4eab\u670b\u53cb\u5708'), (2, '\u6dfb\u52a0\u65b0\u5e74\u613f\u671b'), (3, '\u522b\u4eba\u6d47\u6c34'), (4, '\u6210\u529f\u6dfb\u52a0\u4e00\u4f4d\u597d\u53cb'), (5, '\u795d\u798f'), (6, '\u5410\u69fd'), (7, '\u521b\u5efa\u6811\u6728')]),
        ),
    ]
