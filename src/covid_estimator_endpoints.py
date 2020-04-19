import json
import logging
from flask import request, Flask

from time import strftime
import dicttoxml
import os
from src.estimator import estimator
from src.logging import LogSetup

app = Flask(__name__)
app.config["DEBUG"] = True

app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "watched")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")

# File Logging Setup
app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")


logs = LogSetup()
logs.init_app(app)

# some test data
data = [{
    "region": {
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 5,
        "avgDailyIncomePopulation": 0.71
    },
    "periodType": "days",
    "timeToElapse": 58,
    "reportedCases": 674,
    "population": 66622705,
    "totalHospitalBeds": 1380614
},
    {
        "region": {
            "name": "Africa",
            "avgAge": 19.8,
            "avgDailyIncomeInUSD": 7,
            "avgDailyIncomePopulation": 0.71
        },
        "periodType": "weeks",
        "timeToElapse": 32,
        "reportedCases": 684,
        "population": 66622905,
        "totalHospitalBeds": 1390614
    }
]
print(data)


@app.route('/api/v1/on-covid-19', methods=['POST'])
def add_covid_estimates():
    raw_data = request.get_json()
    print(raw_data)
    # data.update(raw_data)
    data.append(raw_data)
    print(data)
    return {'id': len(data)}, 200


@app.route('/api/v1/on-covid-19/json', methods=['GET'])
def covid_json_estimates():
    data_set = request.get_json()
    for my_dict in data:
        data_set = my_dict

    # data_set = dict([  (k,v) for k,v in my_dict.items()] for my_dict in data)
    result = estimator(data_set)

    return json.dumps(result)


@app.route('/api/v1/on-covid-19/xml', methods=['GET'])
def covid_xml_estimates():
    data_set = request.get_json()
    for my_dict in data:
        data_set = my_dict

    result = estimator(data_set)

    xml_result = dicttoxml.dicttoxml(result)
    new_xml = xml_result.decode("UTF-8")

    return json.dumps(new_xml)


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
@app.after_request
def after_request(response):
    logger = logging.getLogger("app.access")
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.info('%s %s %s %s %s %s',
                    ts,
                    request.remote_addr,
                    request.method,
                    request.scheme,
                    request.full_path,
                    response.status)
        print(response)
    return response


app.run(host='127.0.0.1', port=5000, debug=True)
