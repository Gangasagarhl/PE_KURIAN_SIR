import pandas as pd
import datetime




    
    

class extract_csv_data:
    """
    The whole day is divided into 4 different sections
    This should be done because of the RAG with chatbots 
    This should be useful to work
    """
    
    def extract_total():
        """Return the entire CSV (data.csv) as a DataFrame."""
        data = pd.read_csv("data.csv", header=None)
        return data



    def time_based_extraction(self): 
        # === Step 1: Load and Prepare Data ===
        # Load the CSV file. If your CSV does not have headers, we assign "timings" and "description".
        df = pd.read_csv("data.csv", names=["timings", "description"])

        # Convert the "timings" column to datetime format.
        df["timings"] = pd.to_datetime(df["timings"], format="%Y-%m-%d_%H-%M-%S")
        # Extract only the time portion.
        df["time_only"] = df["timings"].dt.time

        # === Step 2: Define Time Boundaries for Each Period ===
        morning_start   = datetime.time(5, 0, 0)
        morning_end     = datetime.time(11, 59, 59)

        afternoon_start = datetime.time(12, 0, 0)
        afternoon_end   = datetime.time(16, 59, 59)

        evening_start   = datetime.time(17, 0, 0)
        evening_end     = datetime.time(20, 59, 59)

        night_start     = datetime.time(21, 0, 0)
        night_end       = datetime.time(4, 59, 59)

        # === Step 3: Determine the Current Period Based on the Current Time ===
        def get_current_period(current_time):
            """Determine the current period based on current_time (a time object)."""
            if morning_start <= current_time <= morning_end:
                return "morning"
            elif afternoon_start <= current_time <= afternoon_end:
                return "afternoon"
            elif evening_start <= current_time <= evening_end:
                return "evening"
            # Night spans midnight: it's either after 21:00 OR before 05:00.
            elif current_time >= night_start or current_time <= night_end:
                return "night"
            else:
                return None

        # Get the current time.
        current_time = datetime.datetime.now().time()
        current_period = get_current_period(current_time)

        period_mapping = {
            "morning": "night",     # If current is morning, previous is night.
            "afternoon": "morning", # If current is afternoon, previous is morning.
            "evening": "afternoon", # If current is evening, previous is afternoon.
            "night": "evening"      # If current is night, previous is evening.
        }

        previous_period = period_mapping.get(current_period)

        def filter_by_period(df, period):
            if period == "morning":
                return df[(df["time_only"] >= morning_start) & (df["time_only"] <= morning_end)]
            elif period == "afternoon":
                return df[(df["time_only"] >= afternoon_start) & (df["time_only"] <= afternoon_end)]
            elif period == "evening":
                return df[(df["time_only"] >= evening_start) & (df["time_only"] <= evening_end)]
            elif period == "night":
                # Night: either >= 21:00 OR <= 04:59:59 (spanning midnight)
                return df[(df["time_only"] >= night_start) | (df["time_only"] <= night_end)]
            else:
                return pd.DataFrame()  # Return empty DataFrame if period is unknown

        # Extract data for the previous period.
        previous_data = filter_by_period(df, previous_period)
        return previous_data
    

    

