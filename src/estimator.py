import itertools
import json

from src import impact, severeimpact


def estimator(data):
    data = data
    impacts = impact.Impact.impact(data)
    severe_impacts = severeimpact.Severe.severe_impact(data)

    result = {'data': data, 'impact': impacts, 'severe_impact': severe_impacts}

    print(result)

    return result


def covid19_impact_estimator(data):
    if __name__ == '__main__':
        estimate_currently_infected = impact.Impact.impact(data).estimate_currently_infected
        estimate_projected_infections = impact.Impact.impact(data).estimate_projected_infections
        estimate_severe_cases = severeimpact.Severe.severe_impact(data).estimate_severe_cases
        estimate_bed_space_availability = severeimpact.Severe.severe_impact(data).estimate_bed_space_availability
        estimate_cases_for_icu = severeimpact.Severe.severe_impact(data).estimate_cases_for_icu
        estimate_cases_for_ventilators = severeimpact.Severe.severe_impact(data).estimate_cases_for_ventilators
        estimate_dollars_in_flight = severeimpact.Severe.severe_impact(data).estimate_dollars_in_flight

        # def estimator():
        result = itertools.chain(data,
                                 # challenge1
                                 estimate_currently_infected, estimate_projected_infections,
                                 # challenge2
                                 estimate_severe_cases, estimate_bed_space_availability,
                                 # challenge3
                                 estimate_cases_for_icu, estimate_cases_for_ventilators, estimate_dollars_in_flight
                                 )

        for estimates in result:

            return json.dumps(estimates.__dict__)

        return estimator(result)
