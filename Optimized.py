import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

data = pd.read_csv('Input_Data.csv', delimiter=';')

performance = ctrl.Antecedent(np.arange(1, 11, 1), 'Performance_Score')
projects = ctrl.Antecedent(np.arange(0, 51, 1), 'Projects_Handled')
satisfaction = ctrl.Antecedent(np.arange(1, 11, 1), 'Employee_Satisfaction_Score')

promotion_eligibility = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Promotion_Eligibility')

# Fungsi Keanggotaan untuk Performance_Score (skala 1-10)
performance['low'] = fuzz.trapmf(performance.universe, [1, 1, 3, 5])
performance['medium'] = fuzz.trapmf(performance.universe, [3, 5, 6, 8])
performance['high'] = fuzz.trapmf(performance.universe, [6, 8, 10, 10])

# Fungsi Keanggotaan untuk Projects_Handled (skala 0-50)
projects['few'] = fuzz.trapmf(projects.universe, [0, 0, 10, 20])
projects['average'] = fuzz.trapmf(projects.universe, [10, 20, 30, 40])
projects['many'] = fuzz.trapmf(projects.universe, [30, 40, 50, 50])

# Fungsi Keanggotaan untuk Employee_Satisfaction_Score (skala 1-10)
satisfaction['dissatisfied'] = fuzz.trapmf(satisfaction.universe, [1, 1, 3, 5])
satisfaction['neutral'] = fuzz.trapmf(satisfaction.universe, [3, 5, 6, 8])
satisfaction['satisfied'] = fuzz.trapmf(satisfaction.universe, [6, 8, 10, 10])

# Fungsi Keanggotaan untuk Promotion_Eligibility (skala 0-1)
promotion_eligibility['low'] = fuzz.trapmf(promotion_eligibility.universe, [0, 0, 0.3, 0.5])
promotion_eligibility['medium'] = fuzz.trapmf(promotion_eligibility.universe, [0.3, 0.5, 0.7, 0.8])
promotion_eligibility['high'] = fuzz.trapmf(promotion_eligibility.universe, [0.7, 0.9, 1, 1])

performance_levels = ['low', 'medium', 'high']
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
promotion_level = []
for _, row in data.iterrows():
    try:
        promotion_sim.input['Performance_Score'] = row['Performance_Score']
        promotion_sim.input['Projects_Handled'] = row['Projects_Handled']
        promotion_sim.input['Employee_Satisfaction_Score'] = row['Employee_Satisfaction_Score']

        promotion_sim.compute()
        score = round(promotion_sim.output['Promotion_Eligibility'], 2)
        promotion_scores.append(score)

        if 0 <= score <= 0.3:
            promotion_level.append('low')
        elif 0.3 < score <= 0.7:
            promotion_level.append('medium')
        elif 0.7 < score <= 1:
            promotion_level.append('high')
        else:
            promotion_level.append(None)
    except Exception as e:
        print(f"Error processing row {_}: {e}")
        promotion_scores.append(None)
        promotion_level.append(None)

data['Promotion_Eligibility'] = promotion_scores
data['Promotion_Level'] = promotion_level

data.to_csv('Output_Data.csv', index=False)
print("Updated dataset saved as 'Output_Data.csv'.")