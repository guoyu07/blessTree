# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bTree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tree_name', models.CharField(max_length=40)),
                ('count', models.IntegerField(default=0)),
                ('type', models.IntegerField(verbose_name='\u64cd\u4f5c\u7c7b\u578b', choices=[(0, '\u81ea\u5df1\u6d47\u6c34'), (1, '\u7b2c\u4e00\u6b21\u5206\u4eab\u670b\u53cb\u5708'), (2, '\u6dfb\u52a0\u65b0\u5e74\u613f\u671b'), (3, '\u522b\u4eba\u6d47\u6c34'), (4, '\u6210\u529f\u6dfb\u52a0\u4e00\u4f4d\u597d\u53cb'), (5, '\u795d\u798f'), (6, '\u5410\u69fd')])),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('source_id', models.CharField(default=b'na', max_length=100)),
                ('content', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['-action_time'],
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=20)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('tree_name', models.CharField(max_length=40)),
                ('if_share', models.BooleanField(default=False)),
                ('willing', models.CharField(default=b'none', max_length=300)),
                ('count', models.IntegerField(default=0)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='bTree.User')),
            ],
            options={
                'ordering': ['count'],
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='tree',
            name='owner',
            field=models.OneToOneField(to='bTree.User'),
        ),
    ]
