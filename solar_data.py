import json
from collections import defaultdict
import datetime

def _load_one_file(content, tz, solardatadict):
    solar = json.loads(content)['stats']
    for x in solar:
        tsdate = datetime.datetime.fromtimestamp(x['start_time'], tz).date()
        assert x['interval_length'] == 900
        for tstime, val in enumerate(x['production']):
            if tstime >= 96:
                assert val is None
            else:
                solardatadict[(tsdate, tstime)] = (0. if val is None else val)

def load_solar_data_from_json(contents, tz):
    solardatadict = defaultdict(float)
    for c in contents:
        _load_one_file(c, tz, solardatadict)
    return solardatadict
