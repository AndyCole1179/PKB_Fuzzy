import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Load dataset
data = pd.read_csv('Extended_Employee_Performance_and_Productivity_Data.csv', delimiter=';')

# Define fuzzy variables
performance = ctrl.Antecedent(np.arange(1, 6, 1), 'Performance_Score')
years = ctrl.Antecedent(np.arange(0, 31, 1), 'Years_At_Company')
projects = ctrl.Antecedent(np.arange(0, 51, 1), 'Projects_Handled')
satisfaction = ctrl.Antecedent(np.arange(1, 6, 0.1), 'Employee_Satisfaction_Score')
promotions = ctrl.Antecedent(np.arange(0, 6, 1), 'Promotions')

promotion_eligibility = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Promotion_Eligibility')

# Define membership functions
performance['low'] = fuzz.trapmf(performance.universe, [1, 1, 2, 3])
performance['medium'] = fuzz.trapmf(performance.universe, [2, 3, 4, 5])
performance['high'] = fuzz.trapmf(performance.universe, [4, 5, 5, 5])

years['few'] = fuzz.trapmf(years.universe, [0, 0, 3, 6])
years['moderate'] = fuzz.trapmf(years.universe, [3, 6, 12, 18])
years['many'] = fuzz.trapmf(years.universe, [12, 18, 30, 30])

projects['few'] = fuzz.trapmf(projects.universe, [0, 0, 10, 20])
projects['average'] = fuzz.trapmf(projects.universe, [10, 20, 30, 40])
projects['many'] = fuzz.trapmf(projects.universe, [30, 40, 50, 50])

satisfaction['dissatisfied'] = fuzz.trapmf(satisfaction.universe, [1, 1, 2, 3])
satisfaction['neutral'] = fuzz.trapmf(satisfaction.universe, [2, 3, 4, 5])
satisfaction['satisfied'] = fuzz.trapmf(satisfaction.universe, [4, 5, 5, 5])

promotions['none'] = fuzz.trapmf(promotions.universe, [0, 0, 1, 2])
promotions['few'] = fuzz.trapmf(promotions.universe, [1, 2, 3, 4])
promotions['many'] = fuzz.trapmf(promotions.universe, [3, 4, 5, 5])

promotion_eligibility['low'] = fuzz.trapmf(promotion_eligibility.universe, [0, 0, 0.3, 0.5])
promotion_eligibility['medium'] = fuzz.trapmf(promotion_eligibility.universe, [0.3, 0.5, 0.7, 0.9])
promotion_eligibility['high'] = fuzz.trapmf(promotion_eligibility.universe, [0.7, 0.9, 1, 1])

# Input membership categories
performance_levels = ['low', 'medium', 'high']
years_levels = ['few', 'moderate', 'many']
projects_levels = ['few', 'average', 'many']
satisfaction_levels = ['dissatisfied', 'neutral', 'satisfied']
promotions_levels = ['none', 'few', 'many']

# Output membership categories
promotion_levels = ['low', 'medium', 'high']

import itertools

# Generate all possible combinations of input levels
rules = []
rule_id = 1  # To keep track of rule numbering
for performance_level in performance_levels:
    for years_level in years_levels:
        for projects_level in projects_levels:
            for satisfaction_level in satisfaction_levels:
                for promotions_level in promotions_levels:
                    # Define the condition for the rule
                    # Adjust output logic based on your needs
                    if performance_level == 'high' and years_level == 'many' and satisfaction_level == 'satisfied':
                        output_level = 'high'
                    elif performance_level == 'medium' and years_level == 'moderate' and projects_level == 'average':
                        output_level = 'medium'
                    elif performance_level == 'low' or satisfaction_level == 'dissatisfied':
                        output_level = 'low'
                    elif promotions_level == 'none' and years_level == 'few':
                        output_level = 'low'
                    else:
                        output_level = 'medium'  # Default fallback logic
                    
                    # Create the rule
                    rule = ctrl.Rule(
                        performance[performance_level] &
                        years[years_level] &
                        projects[projects_level] &
                        satisfaction[satisfaction_level] &
                        promotions[promotions_level],
                        promotion_eligibility[output_level]
                    )
                    
                    rules.append(rule)
                    print(f"Rule {rule_id}: IF Performance={performance_level}, Years={years_level}, Projects={projects_level}, Satisfaction={satisfaction_level}, Promotions={promotions_level} THEN Promotion={output_level}")
                    rule_id += 1
# Create control system with all generated rules
promotion_ctrl = ctrl.ControlSystem(rules)
promotion_sim = ctrl.ControlSystemSimulation(promotion_ctrl)


# Define fuzzy rules
# rule1 = ctrl.Rule(performance['high'] & years['many'] & satisfaction['satisfied'], promotion_eligibility['high'])
# rule2 = ctrl.Rule(performance['medium'] & years['moderate'] & projects['average'], promotion_eligibility['medium'])
# rule3 = ctrl.Rule(performance['low'] | satisfaction['dissatisfied'], promotion_eligibility['low'])
# rule4 = ctrl.Rule(promotions['none'] & years['few'], promotion_eligibility['low'])
# rule5 = ctrl.Rule(performance['medium'] & projects['many'], promotion_eligibility['medium'])
# rule6 = ctrl.Rule(satisfaction['neutral'] & promotions['few'], promotion_eligibility['medium'])
# rule7 = ctrl.Rule(years['few'] & projects['average'], promotion_eligibility['low'])

# Create control system
# promotion_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
# promotion_sim = ctrl.ControlSystemSimulation(promotion_ctrl)

# Apply fuzzy logic to all rows
promotion_scores = []  # List to store results
for _, row in data.iterrows():
    try:
        promotion_sim.input['Performance_Score'] = row['Performance_Score']
        promotion_sim.input['Years_At_Company'] = row['Years_At_Company']
        promotion_sim.input['Projects_Handled'] = row['Projects_Handled']
        promotion_sim.input['Employee_Satisfaction_Score'] = row['Employee_Satisfaction_Score']
        promotion_sim.input['Promotions'] = row['Promotions']

        promotion_sim.compute()
        promotion_scores.append(promotion_sim.output['Promotion_Eligibility'])
    except Exception as e:
        print(f"Error processing row {_}: {e}")
        promotion_scores.append(None)

# Add results to the dataset
data['Promotion_Eligibility'] = promotion_scores

# Save the updated dataset
data.to_csv('employee_promotion_eligibility.csv', index=False)
print("Updated dataset saved as 'employee_promotion_eligibility.csv'.")
