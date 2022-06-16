import streamlit as st 
from retirement_model import ModelInputs, years_to_retirement
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(layout="wide")

confirm_button = st.sidebar.button("Calculate")
starting_salary = st.sidebar.slider('Starting Salary', value=60000, min_value=0, max_value=1000000, step=1000)
promos_every_n_years = st.sidebar.number_input('Promos Every N Years', value=5)
cost_of_living_raise = st.sidebar.number_input('Cost of Living Raise', value=0.02)
promo_raise = st.sidebar.number_input('Promo Raise', value=0.15)
savings_rate = st.sidebar.number_input('Savings Rate', value=0.25)
interest_rate = st.sidebar.number_input('Interest Rate', value=0.05)
desired_cash = st.sidebar.slider('Desired Cash', value=1500000, min_value=0, max_value=10000000, step=1000000)


model_data = ModelInputs(starting_salary, promos_every_n_years, cost_of_living_raise, promo_raise, savings_rate, interest_rate, desired_cash)

st.write("### Model Outputs")

if confirm_button:
    st.title("Az Retirement Calculator")

    years, wealth_predictions = years_to_retirement(model_data)
    
    old_years, old_wealth_predictions = years, wealth_predictions

    st.write(f'It will take {years} years to reach PKR.{desired_cash:,.0f} of wealth.')

    "#### Visualizations"
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(wealth_predictions.index, wealth_predictions['Wealth'])
    plt.xticks(rotation=90)
    ax.plot((0, years), (desired_cash,desired_cash), '--', color='red')

    scale_y = 1000000
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))

    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    ax.yaxis.set_major_formatter(ticks_y)
    ax.set_ylabel('Wealth (val in millions)')
    ax.set_xlabel('Years')
    st.pyplot(fig)


    st.write("#### Prediction Details")
    st.dataframe(wealth_predictions[['Annual Salary', 'Cash Saved', 'Wealth']])
else:
    st.write("*Select your parameters and click on the calculate button from the side menu.")
