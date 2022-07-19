from django.conf import settings
import json
import sys
from moderate.models import Module
from moderate.main import *

def update_database():
    modulelist = list(Module.objects.all().values_list('code', flat=True))
    for module in modulelist:
        tpl = scrape_n_posts(module, 3)
        Module.objects.filter(code=module).update(
            rating = RFR_avg_rating(tpl[0]),
            comment1 = tpl[1][0],
            comment2 = tpl[1][1],
            comment3 = tpl[1][2],
            searched = 5,
            emotions = convert_emotion_chart_to_str(emotion_chart(tpl[0]))
        )