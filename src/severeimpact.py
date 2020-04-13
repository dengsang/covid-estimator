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
    def severe_impact(data):

        severe_data = json.loads(data)

        reported_cases = severe_data.get("reportedCases")
        period_type = severe_data.get("periodType")
        time_to_elapse = severe_data.get("timeToElapse")
        total_hospital_beds = severe_data.get("totalHospitalBeds")
        population = severe_data.get("population")

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

        self = {'currently_infected': estimate_currently_infected,
                'projected_infections': estimate_projected_infections,
                'estimate_severe_cases': estimate_severe_cases,
                'bed_space_availability': estimate_bed_space_availability,
                'estimate_cases_for_icu': estimate_cases_for_icu,
                'estimate_cases_for_ventilators': estimate_cases_for_ventilators,
                'estimate_dollars_in_flight': estimate_dollars_in_flight}

        return json.dumps(self)
