import json
import math


def estimator(data):
    string_data = json.dumps(data)
    data_object = json.loads(string_data)

    reported_cases = data_object.get("reportedCases")
    period_type = data_object.get("periodType")
    time_to_elapse = data_object.get("timeToElapse")
    total_hospital_beds = data_object.get("totalHospitalBeds")
    population = data_object.get("population")

    estimate_currently_infected = reported_cases * 10

    if period_type == "months":
        elapse = math.trunc(time_to_elapse / 3) * 30
    elif period_type == "weeks":
        elapse = math.trunc(time_to_elapse / 3) * 7
    elif period_type == "days":
        elapse = math.trunc(time_to_elapse / 3)
    else:
        elapse = 0

    estimate_projected_infections = estimate_currently_infected * (2 ** elapse)
    estimate_cases_for_icu = math.trunc(0.5 * estimate_projected_infections)
    estimate_cases_for_ventilators = math.trunc(0.2 * estimate_projected_infections)

    estimate_severe_cases = math.trunc(0.15 * estimate_projected_infections)
    severe_hospital_beds = math.trunc(0.35 * total_hospital_beds)
    estimate_bed_space_availability = severe_hospital_beds - estimate_severe_cases
    estimate_severe_cases = math.trunc(0.15 * estimate_projected_infections)

    average_daily_dollar = math.trunc(estimate_projected_infections * 0.65 * 1.5) / 30
    estimate_dollars_in_flight = average_daily_dollar * population

    impact_data = {'currently_infected': estimate_currently_infected,
                   'projected_infections': estimate_projected_infections,
                   'estimate_cases_for_icu': estimate_cases_for_icu,
                   'estimate_cases_for_ventilators': estimate_cases_for_ventilators,
                   'estimate_dollars_in_flight': estimate_dollars_in_flight}

    severe_data = {'currently_infected': estimate_currently_infected,
                   'projected_infections': estimate_projected_infections,
                   'estimate_severe_cases': estimate_severe_cases,
                   'bed_space_availability': estimate_bed_space_availability,
                   'estimate_cases_for_icu': estimate_cases_for_icu,
                   'estimate_cases_for_ventilators': estimate_cases_for_ventilators,
                   'estimate_dollars_in_flight': estimate_dollars_in_flight}

    result = {'data': data, 'impact': impact_data, 'severe_impact': severe_data}

    print(result)

    return json.dumps(result)


def covid19_impact_estimator():
    input_data = {
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
    estimator(input_data)


if __name__ == "__main__":
    covid19_impact_estimator()
