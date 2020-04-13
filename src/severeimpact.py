import math
import json


class Severe:
    def __init__(self):
        self.data = {
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

    @staticmethod
    def severe_impact():

        data_object = json.loads(__dict__.data)

        # data_pickle = jsonpickle.decode(data)

        reported_cases = data_object.get("reportedCases")
        period_type = data_object.get("periodType")
        time_to_elapse = data_object.get("timeToElapse")
        total_hospital_beds = data_object.get("totalHospitalBeds")
        population = data_object.get("population")

        estimate_currently_infected = reported_cases * 10

        if period_type.tolowercase() == "months":
            elapse = math.trunc(time_to_elapse / 3) * 30
        elif period_type.tolowercase() == "weeks":
            elapse = math.trunc(time_to_elapse / 3) * 7
        elif period_type.tolowercase() == "days":
            elapse = math.trunc(time_to_elapse / 3)
        else:
            elapse = 0

        estimate_projected_infections = estimate_currently_infected * (2 ** elapse)
        estimate_severe_cases = math.trunc(0.15 * estimate_projected_infections)
        severe_hospital_beds = math.trunc(0.35 * total_hospital_beds)
        estimate_bed_space_availability = severe_hospital_beds - estimate_severe_cases
        estimate_cases_for_icu = math.trunc(0.5 * estimate_projected_infections)
        estimate_cases_for_ventilators = math.trunc(0.2 * estimate_projected_infections)

        average_daily_dollar = math.trunc((estimate_projected_infections * 0.65 * 1.5) / 30)
        estimate_dollars_in_flight = average_daily_dollar * population

        data = {'currently_infected': estimate_currently_infected,
                'projected_infections': estimate_projected_infections,
                'estimate_severe_cases': estimate_severe_cases,
                'bed_space_availability': estimate_bed_space_availability,
                'estimate_cases_for_icu': estimate_cases_for_icu,
                'estimate_cases_for_ventilators': estimate_cases_for_ventilators,
                'estimate_dollars_in_flight': estimate_dollars_in_flight}

        return json.dumps(data)
