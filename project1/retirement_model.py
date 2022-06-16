from dataclasses import dataclass
import pandas as pd

@dataclass
class ModelInputs:
    starting_salary: int = 28000
    promos_every_n_years: float = 5.0
    cost_of_living_raise: float = 0.02
    promo_raise: float = 0.15
    savings_rate: float = 0.50
    interest_rate: float = 0.15
    desired_cash: int = 1500000



def salary_at_year(data, year):
    """
    Calculates the salary at a given year using the data from the ModelInputs class
    """
    num_promos = int(year / data.promos_every_n_years)
    return data.starting_salary * ((1 + data.cost_of_living_raise) ** year) * ((1 + data.promo_raise)  ** num_promos)

#print(salary_at_year(model_data, 1))

def cash_saved_during_year(data, year):
    """
    Calculates the cash saved during a given year using the data from the ModelInputs class
    """
    return salary_at_year(data, year) * data.savings_rate

def wealth_at_year(data, year, prior_wealth):
    """
    Calculates the wealth at a given year using the data from the ModelInputs class
    """
    return prior_wealth * (1 + data.interest_rate) + cash_saved_during_year(data, year)

def years_to_retirement(data):
    """
    Calculates the number of years it will take to reach the desired cash amount
    """
    year = 0
    prior_wealth = 0
    wealth = 0

    print("calculating years to retirement..")   
    wealth_predictions = pd.DataFrame(columns=['Wealth', 'Year', 'Annual Salary', 'Cash Saved'])
    wealth_predictions.index.name = 'year'
    while wealth < data.desired_cash:
        year += 1
        wealth = wealth_at_year(data, year, prior_wealth)
        #print(wealth < data.desired_cash)
        #print(f"{wealth:,.0f}")
        prior_wealth = wealth
        wealth_predictions.loc[year] = [wealth, year, salary_at_year(data, year), cash_saved_during_year(data, year)]
    return (year, wealth_predictions)


model_data = ModelInputs()
years_to_retirement(model_data)
