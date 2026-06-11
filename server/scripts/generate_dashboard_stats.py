import json
from datetime import datetime, timedelta


""" 
 XX = completed


We want this script to calculate useful metrics like:
 XX Number of Runs Imported

Mileage:
 XX Average weekly mileage (the last 12 weeks)
 XX total lifetime mileage
 XX mileages each year
 XX mileages each month
 XX mileages each week

Training:
 XX Longest single Run ever
 XX Highest mileage week ever
 XX Highest mileage month ever
 XX highest mileage year ever 

Heart Rate:
- average Heart rate per year
- Average heart rate per easy run

Racing:
- fastest 5k
- fastest 10k
- fastest half marathon
- fastest full marathon

Consistency:
- longest running streak (consecutive days or weeks)
- runs each month



Trend data may be another script or just later.
Stuff like improved easy paces and threshold paces over time.
"""



default_measurement = 'meters'
preferred_measurement = 'miles'

############ DATASET PROCESSING ############
FILE_PATH = r'.\Dashboard\data\fitness-data\normalized_data\summary_list.json'
with open(FILE_PATH, 'r') as file:
    dataset = json.load(file)

# Flattens the dataset to make extracting easier
all_runs = []
for file_obj in dataset:
    summaries = file_obj.get('summaries', [])
    for run in summaries:
        if run.get('sport') == 'running':
            all_runs.append(run)
run_dataset = all_runs







############ UTILITIES ############
def distance_converter(type1=str, type2=str, type1_amount=0.0):
    """ Converts type1 distance to type2 distance. Accepts 'km', 'miles', and 'meters' """
    type1 = type1.lower()
    type2 = type2.lower()
    
    if type1 == type2:
        return type1_amount
    elif type1 == 'meters':
        if type2 == 'km':
            return type1_amount / 1000
        else: # Meters -> miles
            return type1_amount / 1609
    elif type1 == 'km':
        if type2 == 'meters':
            return type1_amount * 1000
        else: # Km -> miles
            return type1_amount / 1.60934
    elif type1 == 'miles':
        if type2 == 'km':
            return type1_amount * 0.621371
        else: # miles -> meters
            return type1_amount * 1609.34










############ DISTANCES ############
# Total lifetime distance
def total_lifetime_distance():
    """ Totals the distance of all runs into a lifetime total """
    total_distance = 0
    for each_run in run_dataset:
        total_distance += each_run.get('total_distance', 0)
    print(f"Total Lifetime Miles: {distance_converter('meters', 'miles', total_distance):.2f}")
    return total_distance # Still in meters


# Each time-frame distances
def each_distance_year():
    """ Gets the distances for each year """
    year_distance = {}
    run_date = {}
    
    for each_run in run_dataset:
        distance = each_run.get('total_distance', 0)
        start_time_str = each_run.get('start_time', '')
        try:
            run_date = datetime.fromisoformat(start_time_str)
            year_key = (run_date.year)
            year_distance[year_key] = round(year_distance.get(year_key, 0.0) + distance_converter(default_measurement, preferred_measurement, distance), 2)
        except ValueError:
            continue
    return year_distance

def each_distance_month():
    """ Gets the distances for each month """
    month_distance = {}
    run_date = {}
    
    for each_run in run_dataset:
        distance = each_run.get('total_distance', 0)
        start_time_str = each_run.get('start_time', '')
        try:
            run_date = datetime.fromisoformat(start_time_str)
            month_key = (run_date.year, run_date.month)
            month_distance[month_key] = round(month_distance.get(month_key, 0.0) + distance_converter(default_measurement, preferred_measurement, distance), 2)
        except ValueError:
            continue
    return month_distance

def each_distance_week():
    """ Gets the distances for each week """
    week_distance = {}
    run_date = {}
    
    for each_run in run_dataset:
        distance = each_run.get('total_distance', 0)
        start_time_str = each_run.get('start_time', '')
        try:
            run_date = datetime.fromisoformat(start_time_str)
            week_key = (run_date.year, run_date.isocalendar()[1])
            week_distance[week_key] = round(week_distance.get(week_key, 0.0) + distance_converter(default_measurement, preferred_measurement, distance), 2)
        except ValueError:
            continue
    return week_distance


# Highest time-based distances
def max_distance_year():
    return max(each_distance_year(), key=each_distance_year().get), max(each_distance_year().values())
def max_distance_month():
    return max(each_distance_month(), key=each_distance_month().get), max(each_distance_month().values())
def max_distance_week():
    return max(each_distance_week(), key=each_distance_week().get), max(each_distance_week().values())


# Last 12 weeks avg mileage
def avg_last_12_weeks():
    weekly_mileage = {}
    for each_run in run_dataset:
        distance = each_run.get('total_distance')
        start_time_str = each_run.get('start_time')
        try:
            run_date = datetime.fromisoformat(start_time_str)
            week_key = (run_date.year, run_date.isocalendar()[1])
            weekly_mileage[week_key] = weekly_mileage.get(week_key, 0.0) + distance
        except ValueError:
            continue
    # Find the newest run
    newest_run_str = max(run_dataset, key=lambda x: x.get('start_time', ''))['start_time']
    newest_date = datetime.fromisoformat(newest_run_str)
    last_12_weeks_total = 0.0
    # Now we can check backwards from the last tracked acitivty date
    for i in range(12):
        check_date = newest_date - timedelta(weeks=i)
        check_key = (check_date.year, check_date.isocalendar()[1])
        last_12_weeks_total += weekly_mileage.get(check_key, 0.0)
    avg_12_weeks = last_12_weeks_total / 12
    return round(distance_converter(default_measurement, preferred_measurement, avg_12_weeks), 2)





# Individual Runs
def longest_single_run():
    """ Finds longest single run and the date it happened """
    run_distance = {}
    for each_run in run_dataset:
        distance = each_run.get('total_distance', 0)
        start_time_str = each_run.get('start_time', '')
        try:
            run_date = datetime.fromisoformat(start_time_str)
            day_key = (run_date.year, run_date.month, run_date.day)
            run_distance[day_key] = round(run_distance.get(day_key, 0.0) + distance_converter(default_measurement, preferred_measurement, distance), 2)
        except ValueError:
            continue
    longest_day = max(run_distance, key=run_distance.get)
    longest_run = run_distance[longest_day]
    return longest_day, longest_run

def fastest_mile():
    """ Finds fastest 1-mile time and the date it happened """
def fastest_5k():
    """ Finds fastest 5k time and the date it happened """




























#### Main function to calculate metrics
def dashboard_stats():
    if not all_runs:
        print("No running data found in the file.")
        return
    
    print(f"\n** Converting default {default_measurement.upper()} into {preferred_measurement.upper()} **")
    # Num of runs imported
    total_runs = len(all_runs)
    print(f"# of runs imported: {total_runs}")
    
    # Longest Run
    longest_run = max(all_runs, key=lambda x: x.get('total_distance', 0))
    longest_run_km = longest_run.get('total_distance', 0) / 1000
    print(f"Longest run of all time is {longest_run.get('start_time')} covering {distance_converter(default_measurement,preferred_measurement,longest_run_km):.2f} {preferred_measurement} ({longest_run_km:.2f} {default_measurement})")
    
    # Time-based tracking initialization
    weekly_mileage = {} # key: (Year, ISO_week_number)
    monthly_mileage = {} # key: (Year, Month)
    
    for run in all_runs:
        distance_km = run.get('total_distance', 0) / 1000
        start_time_str = run.get('start_time', '')
        
        try:
            # Parse format "2023-10-30 22:23:20+00:00" using fromisoformat
            run_date = datetime.fromisoformat(start_time_str)
            
            # Generate caldenar grouping keys
            week_key = (run_date.year, run_date.isocalendar()[1])
            month_key = (run_date.year, run_date.month)
            
            # Aggregate distance
            weekly_mileage[week_key] = weekly_mileage.get(week_key, 0.0) + distance_km
            monthly_mileage[month_key] = monthly_mileage.get(month_key, 0.0) + distance_km
        except ValueError:
            continue
    
    
    # Highest Mileage week
    if weekly_mileage:
        best_week_key = max(weekly_mileage, key=weekly_mileage.get)
        print(f"Highest mileage week: Year {best_week_key[0]} Week{best_week_key} with {distance_converter(default_measurement,preferred_measurement,weekly_mileage[best_week_key]):.2f} {preferred_measurement} ({weekly_mileage[best_week_key]:.2f} {default_measurement})")
    
    
    # Highest mileage Month
    if monthly_mileage:
        best_month_key = max(monthly_mileage, key=monthly_mileage.get)
        print(f"Highest mileage month: Year {best_month_key[0]} Month {best_month_key[1]} with {distance_converter(default_measurement,preferred_measurement,monthly_mileage[best_month_key]):.2f} {preferred_measurement} ({monthly_mileage[best_month_key]:.2f} {default_measurement})")
    
    
    # Average weekly mileage (Last 12 weeks of the newest run)
    if weekly_mileage:
        # Find the date of the most recent run in the dataset
        newest_run_str = max(all_runs, key=lambda x: x.get('start_time', ''))['start_time']
        newest_date = datetime.fromisoformat(newest_run_str)
        
        last_12_weeks_total = 0.0
        # Check backwards 12 weeks from the latest tracked activity date
        for i in range(12):
            check_date = newest_date - timedelta(weeks=i)
            check_key = (check_date.year, check_date.isocalendar()[1])
            last_12_weeks_total += weekly_mileage.get(check_key, 0.0)
        
        avg_twelve_weeks = last_12_weeks_total / 12
        print(f"Average weekly milage (last 12 weeks): {distance_converter(default_measurement,preferred_measurement,avg_twelve_weeks):.2f} {preferred_measurement} ({avg_twelve_weeks:.2f} {default_measurement})\n")








def main():
    dashboard_stats()
if __name__ == "__main__":
    print()
    # main()
    # total_lifetime_distance()
    # print(each_distance_year(),"\n\n")
    # print("Highest Mileage Year Ever: (Year, Miles)\n",max_distance_year(), "\n\n")
    # print(each_distance_month(),"\n\n")
    # print("Highest Mileage Month Ever: (Year, Month, Miles)\n",max_distance_month(), "\n\n")
    # print(each_distance_week(),"\n\n")
    # print("Highest Mileage Week Ever: (Year, Week, Miles)\n",max_distance_week(), "\n\n")
    # print("Longest Single Run Ever: (Year, Month, Day, Miles)\n", longest_single_run())
    print(avg_last_12_weeks())
    