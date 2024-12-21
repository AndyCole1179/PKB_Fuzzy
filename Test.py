import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import pandas as pd

data = pd.read_excel('Extended_Employee_Performance_and_Productivity_Data.csv', sheet_name='Extended_Employee_Performance_a')
# Define input variables
performance = ctrl.Antecedent(np.arange(1, 6, 1), 'Performance_Score')
years = ctrl.Antecedent(np.arange(0, 31, 1), 'Years_At_Company')
satisfaction = ctrl.Antecedent(np.arange(1.0, 5.1, 0.1), 'Employee_Satisfaction_Score')

# Define output variables
salary_increase = ctrl.Consequent(np.arange(0, 21, 1), 'Salary_Increase')
promotion = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Promotion_Eligibility')

# Membership functions
performance['low'] = fuzz.trapmf(performance.universe, [1, 1, 2, 3])
performance['medium'] = fuzz.trapmf(performance.universe, [2, 3, 4, 5])
performance['high'] = fuzz.trapmf(performance.universe, [4, 5, 5, 5])

# Add more membership functions and rules...

# Example rule
rule1 = ctrl.Rule(performance['high'] & years['many'], salary_increase['large'])

# Create control system and simulation
salary_ctrl = ctrl.ControlSystem([rule1, ...])
salary_sim = ctrl.ControlSystemSimulation(salary_ctrl)

# Input values
salary_sim.input['Performance_Score'] = 4.5
salary_sim.input['Years_At_Company'] = 10

# Compute
salary_sim.compute()
print(salary_sim.output['Salary_Increase'])
