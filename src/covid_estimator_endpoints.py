import json
import flask
import dicttoxml
from src.estimator import estimator

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# some test data
data = {
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
}
print(data)


@app.route('/api/v1/on-covid-19/json', methods=['GET'])
def covid_json_estimates():

    result = estimator(data)
    print(result)

    return json.dumps(result)


@app.route('/api/v1/on-covid-19/xml', methods=['GET'])
def covid_xml_estimates():

    result = estimator(data)
    xml_result = dicttoxml.dicttoxml(result)

    new_xml = xml_result.decode("UTF-8")
    print(new_xml)

    return json.dumps(new_xml)


app.run(host='127.0.0.1', port=5000, debug=True)
