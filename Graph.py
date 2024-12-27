import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# Define universes
performance_universe = np.linspace(0, 11, 100)
projects_universe = np.linspace(0, 50, 100)
satisfaction_universe = np.linspace(0, 11, 100)
promotion_universe = np.linspace(0, 1, 100)

# Define membership functions for each category
# Performance
performance_low = fuzz.trapmf(performance_universe, [1, 1, 3, 5])
performance_medium = fuzz.trapmf(performance_universe, [3, 5, 6, 8])
performance_high = fuzz.trapmf(performance_universe, [6, 8, 10, 10])

# Projects
projects_few = fuzz.trapmf(projects_universe, [0, 0, 10, 20])
projects_average = fuzz.trapmf(projects_universe, [10, 20, 30, 40])
projects_many = fuzz.trapmf(projects_universe, [30, 40, 50, 50])

# Satisfaction
satisfaction_dissatisfied = fuzz.trapmf(satisfaction_universe, [1, 1, 3, 5])
satisfaction_neutral = fuzz.trapmf(satisfaction_universe, [3, 5, 6, 8])
satisfaction_satisfied = fuzz.trapmf(satisfaction_universe, [6, 8, 10, 10])

# Promotion Eligibility
promotion_low = fuzz.trapmf(promotion_universe, [0, 0, 0.3, 0.5])
promotion_medium = fuzz.trapmf(promotion_universe, [0.3, 0.5, 0.7, 0.9])
promotion_high = fuzz.trapmf(promotion_universe, [0.7, 0.9, 1, 1])



# Plot all membership functions
fig, axs = plt.subplots(4, 1, figsize=(10, 20))

# Performance plot
axs[0].plot(performance_universe, performance_low, label='Low')
axs[0].plot(performance_universe, performance_medium, label='Medium')
axs[0].plot(performance_universe, performance_high, label='High')
axs[0].set_title('Performance Membership Functions')
axs[0].legend()

# Projects plot
axs[1].plot(projects_universe, projects_few, label='Few')
axs[1].plot(projects_universe, projects_average, label='Average')
axs[1].plot(projects_universe, projects_many, label='Many')
axs[1].set_title('Projects Membership Functions')
axs[1].legend()

# Satisfaction plot
axs[2].plot(satisfaction_universe, satisfaction_dissatisfied, label='Dissatisfied')
axs[2].plot(satisfaction_universe, satisfaction_neutral, label='Neutral')
axs[2].plot(satisfaction_universe, satisfaction_satisfied, label='Satisfied')
axs[2].set_title('Satisfaction Membership Functions')
axs[2].legend()

# Promotion Eligibility plot
axs[3].plot(promotion_universe, promotion_low, label='Low')
axs[3].plot(promotion_universe, promotion_medium, label='Medium')
axs[3].plot(promotion_universe, promotion_high, label='High')
axs[3].set_title('Promotion Eligibility Membership Functions')
axs[3].legend()

# Adjust layout
plt.tight_layout()
plt.show()
