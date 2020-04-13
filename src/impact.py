import json
import math


class Impact:
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
    def impact():

        data_object = json.loads(__dict__.data)

        # data_pickle = jsonpickle.decode(data)

        reported_cases = data_object.get("reportedCases")
        period_type = data_object.get("periodType")
        time_to_elapse = data_object.get("timeToElapse")

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
        estimate_cases_for_icu = math.trunc(0.5 * estimate_projected_infections)
        estimate_cases_for_ventilators = math.trunc(0.2 * estimate_projected_infections)

        average_daily_dollar = math.trunc(estimate_projected_infections * 0.65 * 1.5) / 30
        estimate_dollars_in_flight = average_daily_dollar * population

        data = {'currently_infected': estimate_currently_infected,
                'projected_infections': estimate_projected_infections,
                'estimate_cases_for_icu': estimate_cases_for_icu,
                'estimate_cases_for_ventilators': estimate_cases_for_ventilators,
                'estimate_dollars_in_flight': estimate_dollars_in_flight}

        return json.dumps(data)
