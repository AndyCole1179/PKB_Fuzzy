import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

data = pd.read_csv('Extended_Employee_Performance_and_Productivity_Data.csv', delimiter=';')

performance = ctrl.Antecedent(np.arange(1, 6, 1), 'Performance_Score')
projects = ctrl.Antecedent(np.arange(0, 51, 1), 'Projects_Handled')
satisfaction = ctrl.Antecedent(np.arange(1, 6, 0.1), 'Employee_Satisfaction_Score')
promotions = ctrl.Antecedent(np.arange(0, 6, 1), 'Promotions')

promotion_eligibility = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Promotion_Eligibility')

performance['low'] = fuzz.trapmf(performance.universe, [1, 1, 2, 3])
performance['medium'] = fuzz.trapmf(performance.universe, [2, 3, 4, 5])
performance['high'] = fuzz.trapmf(performance.universe, [4, 5, 5, 5])

projects['few'] = fuzz.trapmf(projects.universe, [0, 0, 10, 20])
projects['average'] = fuzz.trapmf(projects.universe, [10, 20, 30, 40])
projects['many'] = fuzz.trapmf(projects.universe, [30, 40, 50, 50])

satisfaction['dissatisfied'] = fuzz.trapmf(satisfaction.universe, [1, 1, 2, 3])
satisfaction['neutral'] = fuzz.trapmf(satisfaction.universe, [2, 3, 4, 5])
satisfaction['satisfied'] = fuzz.trapmf(satisfaction.universe, [4, 5, 5, 5])

promotion_eligibility['low'] = fuzz.trapmf(promotion_eligibility.universe, [0, 0, 0.3, 0.5])
promotion_eligibility['medium'] = fuzz.trapmf(promotion_eligibility.universe, [0.3, 0.5, 0.7, 0.9])
promotion_eligibility['high'] = fuzz.trapmf(promotion_eligibility.universe, [0.7, 0.9, 1, 1])

performance_levels = ['low', 'medium', 'high']
years_levels = ['few', 'moderate', 'many']
projects_levels = ['few', 'average', 'many']
satisfaction_levels = ['dissatisfied', 'neutral', 'satisfied']

promotion_levels = ['low', 'medium', 'high']

rules = []
rule_id = 1 
for performance_level in performance_levels:
    for projects_level in projects_levels:
        for satisfaction_level in satisfaction_levels:
                if performance_level == 'high' and satisfaction_level == 'satisfied':
                    output_level = 'high'
                elif performance_level == 'medium' and projects_level == 'average':
                    output_level = 'medium'
                elif performance_level == 'low' or satisfaction_level == 'dissatisfied':
                    output_level = 'low'
                else:
                    output_level = 'medium'
                
                rule = ctrl.Rule(
                    performance[performance_level] &
                    projects[projects_level] &
                    satisfaction[satisfaction_level],
                    promotion_eligibility[output_level]
                )
                
                rules.append(rule)
                print(f"Rule {rule_id}: IF Performance={performance_level},Projects={projects_level}, Satisfaction={satisfaction_level} THEN Promotion={output_level}")
                rule_id += 1
                
promotion_ctrl = ctrl.ControlSystem(rules)
promotion_sim = ctrl.ControlSystemSimulation(promotion_ctrl)

promotion_scores = [] 
for _, row in data.iterrows():
    try:
        promotion_sim.input['Performance_Score'] = row['Performance_Score']
        promotion_sim.input['Projects_Handled'] = row['Projects_Handled']
        promotion_sim.input['Employee_Satisfaction_Score'] = row['Employee_Satisfaction_Score']

        promotion_sim.compute()
        promotion_scores.append(promotion_sim.output['Promotion_Eligibility'])
    except Exception as e:
        print(f"Error processing row {_}: {e}")
        promotion_scores.append(None)

data['Promotion_Eligibility'] = promotion_scores

data.to_csv('employee_promotion_eligibility.csv', index=False)
print("Updated dataset saved as 'employee_promotion_eligibility.csv'.")