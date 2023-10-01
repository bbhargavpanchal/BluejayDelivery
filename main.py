import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a DataFrame
csv_file = "cs.csv"
df = pd.read_csv(csv_file)

# Drop rows with missing values in the 'Time' and 'Time Out' columns
df.dropna(subset=['Time', 'Time Out'], inplace=True)

# Convert the 'Time' and 'Time Out' columns to datetime format
df['Time'] = pd.to_datetime(df['Time'].str.replace('-', '/'), format='%m/%d/%Y %I:%M %p')
df['Time Out'] = pd.to_datetime(df['Time Out'].str.replace('-', '/'), format='%m/%d/%Y %I:%M %p')

# Sort the DataFrame by 'Employee Name' and 'Time'
df.sort_values(by=['Employee Name', 'Time'], inplace=True)

# Initialize variables to track consecutive dates and shifts
consecutive_count = 1
consecutive_dates = []
current_employee = None
previous_date = None
max_shift_duration = timedelta(hours=14)

# Lists to store results
consecutive_results = []
more_than_14_hours_results = []
shift_between_10_hours_results = []

# Iterate through the DataFrame to find employees who meet the criteria
for index, row in df.iterrows():
    if row['Employee Name'] == current_employee:
        # Check consecutive dates
        if previous_date and (row['Time'].date() - previous_date.date()).days == 1:
            consecutive_dates.append(row['Time'].date())
            consecutive_count += 1
        elif previous_date and (row['Time'].date() - previous_date.date()).days > 1:
            consecutive_dates = [row['Time'].date()]
            consecutive_count = 1

        # Check shift duration
        shift_duration = row['Time Out'] - row['Time']
        if shift_duration > max_shift_duration:
            more_than_14_hours_results.append(
                f"Employee Name: {current_employee}, Position ID: {row['Position ID']} - Shift duration exceeds 14 hours")

        previous_date = row['Time']
    else:
        consecutive_dates = [row['Time'].date()]
        consecutive_count = 1
        current_employee = row['Employee Name']
        previous_date = row['Time']

    # Check consecutive days
    if consecutive_count == 7:
        consecutive_results.append(
            f"Employee Name: {current_employee}, Position ID: {row['Position ID']} - Worked 7 consecutive days: {', '.join([d.strftime('%m/%d/%Y') for d in consecutive_dates])}")
        consecutive_dates = []
print("----------------------------------------------------")
print("who has worked for 7 consecutive days.")
print("----------------------------------------------------")
print("\n".join(consecutive_results))

# who have less than 10 hours of time between shifts but greater than 1 hour
df['Duration'] = (df['Time Out'] - df['Time']).dt.total_seconds() / 3600

# Filter employees who worked less than 1 hour or more than 10 hours
filtered_df = df[(df['Duration'] > 1) | (df['Duration'] < 10)]

# Get unique employee names and positions
unique_df = filtered_df[['Employee Name', 'Position ID']].drop_duplicates()

#print
print("\n\n----------------------------------------------------")
print("who have less than 10 hours of time between shifts but greater than 1 hour")
print("----------------------------------------------------")
# Iterate through the unique DataFrame and print each record
for index, row in unique_df.iterrows():
    print(f"Employee Name:  {row['Employee Name']} ({row['Position ID']})")


print("\n\n----------------------------------------------------")
print("Who has worked for more than 14 hours in a single shift")
print("----------------------------------------------------")
print("\n".join(more_than_14_hours_results))
