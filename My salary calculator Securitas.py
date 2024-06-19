#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np

# Define the pay rates
pay_rates = {
    'N1': 26.43,
    'N2': 32.17,
    'N3': 39.65,
    'N4': 52.86,
    'PH1': 66.08,
    'PH2': 66.08,
    'OT1': 39.65,
    'OT2': 52.86
}

# Define the shift cycle (2 days N1, 2 days N2, 4 days off)
shift_cycle = ['N2', 'N2', 'Off', 'Off', 'Off', 'Off', 'N1', 'N1']

# Generate dates for the given period
dates = pd.date_range(start="2024-06-10", end="2024-12-31", freq='D')


# Create a DataFrame with these dates
schedule = pd.DataFrame(dates, columns=['Date'])

# Assign shifts to dates based on the cycle
schedule['Shift'] = np.tile(shift_cycle, len(schedule) // len(shift_cycle) + 1)[:len(schedule)]

# Function to calculate pay for a single shift
def calculate_shift_pay(shift):
    if shift == 'Off':
        return 0
    elif shift == 'N1':
        return (10.86 * pay_rates[shift]) + (1.14 * pay_rates['OT1'])
    elif shift == 'N2':
        return (6 * pay_rates[shift]) + (4.86 * pay_rates[shift]) + (1.14 * pay_rates['OT1'])
    elif shift == 'N3':
        return (10.86 * pay_rates[shift]) + (1.14 * pay_rates['OT1'])
    elif shift == 'N4':
        return (10.86 * pay_rates[shift]) + (1.14 * pay_rates['OT1'])
    elif shift == 'PH2':
        return (6 * pay_rates[shift]) + (4.86 * pay_rates['N2']) + (1.14 * pay_rates['OT1'])
    elif shift == 'PH1':
        return (10.86 * pay_rates[shift]) + (1.14 * pay_rates['OT1'])
    return 0

# Calculate pay for each shift in the schedule
schedule['Pay'] = schedule['Shift'].apply(calculate_shift_pay)

# Function to calculate fortnightly salary with additional overtime shifts
def calculate_fortnightly_salary(schedule, start_date, additional_ot_shifts=[]):
    end_date = start_date + pd.Timedelta(days=13)
    fortnight_schedule = schedule[(schedule['Date'] >= start_date) & (schedule['Date'] <= end_date)]
    total_pay = fortnight_schedule['Pay'].sum()
    
    # Add additional overtime shifts
    for ot_shift in additional_ot_shifts:
        if ot_shift in pay_rates:
            total_pay += (10.86 * pay_rates[ot_shift]) + (1.14 * pay_rates['OT1'])
    
    return {
        'Start Date': start_date,
        'End Date': end_date,
        'Total Pay': total_pay
    }

# Example usage
start_date = pd.Timestamp("2024-06-10")
additional_ot_shifts = ['OT2', 'OT2', 'OT2']  # Add two additional overtime shifts
fortnightly_salary = calculate_fortnightly_salary(schedule, start_date, additional_ot_shifts)

print(fortnightly_salary)


# In[ ]:





# In[ ]:





# In[ ]:




