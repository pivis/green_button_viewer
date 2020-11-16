import json
from collections import defaultdict
import datetime

def load_solar_data_from_json(tz):
    jsonstr = open('./solar_production_20160813_to_20201108.json', 'rt').read()
    solar = json.loads(jsonstr)['stats']
    solardatadict = defaultdict(float)
    for x in solar:
        tsdate = datetime.datetime.fromtimestamp(x['start_time'], tz).date()
        assert x['interval_length'] == 900
        for tstime, val in enumerate(x['production']):
            if tstime >= 96:
                assert val is None
            else:
                solardatadict[(tsdate, tstime)] = (0. if val is None else val)
    return solardatadict
