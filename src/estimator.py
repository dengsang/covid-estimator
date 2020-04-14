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
    severe_impact_currently_infected = reported_cases * 50

    if period_type == "months":
        elapse = math.trunc(time_to_elapse / 3) * 30
    elif period_type == "weeks":
        elapse = math.trunc(time_to_elapse / 3) * 7
    elif period_type == "days":
        elapse = math.trunc(time_to_elapse / 3)
    else:
        elapse = 0

    estimate_projected_infections = estimate_currently_infected * (2 ** elapse)
    severe_projected_infections = severe_impact_currently_infected * (2 ** elapse)
    # impact
    estimate_cases_for_icu = math.trunc(0.5 * estimate_projected_infections)
    estimate_cases_for_ventilators = math.trunc(0.2 * estimate_projected_infections)
    # severe
    severe_estimate_cases_for_icu = math.trunc(0.5 * severe_projected_infections)
    severe_estimate_cases_for_ventilators = math.trunc(0.2 * severe_projected_infections)

    severe_hospital_beds = math.trunc(0.35 * total_hospital_beds)

    # impact
    estimate_severe_cases = math.trunc(0.15 * estimate_projected_infections)
    estimate_bed_space_availability = severe_hospital_beds - estimate_severe_cases
    # severe
    severe_estimate_severe_cases = math.trunc(0.15 * severe_projected_infections)
    severe_estimate_bed_space_availability = severe_hospital_beds - severe_estimate_severe_cases

    # impact
    average_daily_dollar = math.trunc(estimate_projected_infections * 0.65 * 1.5) / 30
    estimate_dollars_in_flight = math.trunc(average_daily_dollar * population)

    # severe
    severe_average_daily_dollar = math.trunc(severe_projected_infections * 0.65 * 1.5) / 30
    severe_estimate_dollars_in_flight = math.trunc(severe_average_daily_dollar * population)

    impact_data = {'currentlyInfected': estimate_currently_infected,
                   'infectionsByRequestedTime': estimate_projected_infections,
                   'severeCasesByRequestedTime': estimate_severe_cases,
                   'hospitalBedsByRequestedTime': estimate_bed_space_availability,
                   'casesForICUByRequestedTime': estimate_cases_for_icu,
                   'casesForVentilatorsByRequestedTime': estimate_cases_for_ventilators,
                   'dollarsInFlight': estimate_dollars_in_flight}

    severe_data = {'currentlyInfected': severe_impact_currently_infected,
                   'infectionsByRequestedTime': severe_projected_infections,
                   'severeCasesByRequestedTime': severe_estimate_severe_cases,
                   'hospitalBedsByRequestedTime': severe_estimate_bed_space_availability,
                   'casesForICUByRequestedTime': severe_estimate_cases_for_icu,
                   'casesForVentilatorsByRequestedTime': severe_estimate_cases_for_ventilators,
                   'dollarsInFlight': severe_estimate_dollars_in_flight}

    result = {'data': data, 'impact': impact_data, 'severeImpact': severe_data}

    print(result)

    return json.dumps(result)


def covid19ImpactEstimator():
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
    covid19ImpactEstimator()
