# Write plant input to database
# Database table contains rows for each day
# Outputs are y1, y2 are columns in the database (biogas and amonia)
# Write to row with is_current==true


import time
from dotenv import dotenv_values
from supabase import create_client, Client

# Get Supabase url and api key from .env file
config = dotenv_values(".env")
url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")

# Initialize supabase client
supabase: Client = create_client(url, key)


# Try 5 times to write data to database
attempts = 0
success = False
MAX_ATTEMPTS = 5
SLEEP_TIME = 1 # seconds

while attempts < MAX_ATTEMPTS:
    try:
        # Update plant current plant outputs to database
        response = supabase.table('plant_data').update({'methane':10, 'ammonia':11}).eq('is_current', 'true').execute()

        # Terminate if update data succesfull
        if response['status_code']==200:
            success = True
            print("Success in writting data!")
            break
    except:
        print("Error in writting data")
        attempts += 1
    # wait for a few seconds before trying again
    time.sleep(SLEEP_TIME)



if success:
    plant_outputs =  response['data'][0]
    methane = plant_outputs['methane']
    ammonia = plant_outputs['ammonia']
    print(methane, ammonia)
    
else:
    print("Failure writing output!!!!")
