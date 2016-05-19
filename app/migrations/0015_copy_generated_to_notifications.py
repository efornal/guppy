# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_create_model_notification'),
    ]

    operations = [
        migrations.RunSQL("insert into notifications (id,created_at,updated_at,change_id,user_id,change_confirmed) select id,created_at,updated_at,change_id,user_id,change_confirmed from generated; SELECT setval('notifications_id_seq', COALESCE((SELECT MAX(id)+1 FROM notifications), 1), false);"),
    ]
