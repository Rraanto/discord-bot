import fastf1 as ff
from fastf1 import plotting
import pandas as pd
from matplotlib import pyplot
from matplotlib.pyplot import figure
from matplotlib import cm
import numpy as np
from datetime import datetime as dt
import os

# defining usefule constants
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
LATEST_SEASON = 2023 # hardcode
SESSION_TYPE = "R"   # race session

# enabling ff1 cache
done = False
while not done:
    try:
        ff.Cache.enable_cache(f'{CURRENT_PATH}.cache')
        done = True
    except NotADirectoryError:
        os.mkdir(f'{CURRENT_PATH}.cache/')

# pandas setting
pd.options.mode.chained_assignment = None 

def get_latest_race_name(schedule):
    """
    Given a schedule, return the name of the latest race that has already happened. 
    :param schedule: the schedule dataframe
    :return: The latest race name.
    """
    today_date = dt.now()
    latest = None
    for _, event in schedule.iterrows():
        if event['EventDate'] < today_date or dt.now().year > LATEST_SEASON:
            latest = event
        else:
            return latest['EventName']
    print(f"Latest race is : {latest['EventName']}")
    return latest['EventName']

def generate_file(drivers):
    """
    Generates a .png file containing the graphs
    """
# loading info about latest grand prix 
    schedule = ff.get_event_schedule(LATEST_SEASON)
    latest_gp_name = get_latest_race_name(schedule)

    gp = ff.get_session(LATEST_SEASON, latest_gp_name, SESSION_TYPE)
    gp.load()
    laps = gp.laps
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    if drivers == ():
        drivers = [driver[1][2] for driver in gp.results.iterrows()] # if no args given, plots all drivers

    # Exclude outliers (including pit stops)
    laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]

    # IQR 
    q75, q25 = laps['LapTimeSeconds'].quantile(
    0.75), laps['LapTimeSeconds'].quantile(0.25)
    inter = q75 - q25
    laptime_max = q75 + (1.5 * inter)
    laptime_min = q25 - (1.5 * inter)

    laps.loc[laps['LapTimeSeconds'] < laptime_min, 'LapTimeSeconds'] = np.nan
    laps.loc[laps['LapTimeSeconds'] > laptime_max, 'LapTimeSeconds'] = np.nan
    
    # plotting
    teams = []

    # plot size configurations 
    pyplot.rcParams['figure.figsize'] = [10, 10]
    # subplots (average pace, lap-by-lap pace)
    fig, ax = pyplot.subplots(2)

    # average racepace
    laptimes = [laps.pick_driver(x)['LapTimeSeconds'].dropna() for x in drivers]
    ax[0].boxplot(laptimes, labels=drivers)
    ax[0].set_title('Average pace')
    ax[0].set(ylabel='Laptime')

# laptimes (lap-by-lap)
    for driver in drivers:
        try:
            driver_laps = laps.pick_driver(
                driver)[['LapNumber', 'LapTimeSeconds', 'Team']]
            driver_laps = driver_laps.dropna()
            team = pd.unique(driver_laps['Team'])[0]
            x = driver_laps['LapNumber']
            y = driver_laps['LapTimeSeconds']
            poly = np.polyfit(driver_laps['LapNumber'],
                            driver_laps['LapTimeSeconds'], 5)
            y_poly = np.poly1d(poly)(driver_laps['LapNumber'])

            linestyle = '-' if team not in teams else ':'
            # labels and headers
            ax[1].plot(x, y, label=driver,
                    color=ff.plotting.team_color(team), linestyle=linestyle) # use y_poly to plot smooth curve
            ax[1].set(ylabel='Laptime (seconds)')
            ax[1].set(xlabel='Lap')

            ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
            if team not in teams:
                teams.append(team)
        except IndexError:
            pass
    
    ax[1].set_facecolor("grey")
    fig.suptitle(f"{gp.event['EventName']}")

    # saving the picture 
    filename = f"{str(gp.event['EventDate'])[:4]}-{gp.event['Country']}-{gp.name}.png"
    pyplot.savefig(filename, dpi=300)
    return filename


if __name__ == "__main__":
    _ = generate_file()
