# Read plant input from database
# Database table contains rows for each day
# Inputs are x1, x2, x3 columns in the database
# Select the row with the curent input vector for the current day (column: is_current==true)

import time
from dotenv import dotenv_values
from supabase import create_client, Client

# Get Supabase url and api key from .env file
config = dotenv_values(".env")
url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")

# In case of error we set platn inputs to some default values
# !!!! Better to set this to previous day values
X1_DEFAULT = 1
X2_DEFAULT = 1
X3_DEFAULT = 1

# Initialize supabase client
supabase: Client = create_client(url, key)

# Try 5 times to read data from database
attempts = 0
success = False
MAX_ATTEMPTS = 5
SLEEP_TIME = 5 # seconds

while attempts < MAX_ATTEMPTS:
    try:
        # Read plant current plant inputs from database
        response = supabase.table('plant_data').select('x1,x2,x3').eq('is_current', 'true').execute()
        # Terminate if read data succesfull
        if response['status_code']==200:
            success = True
            print("Success in fetching data!")
            break
    except:
        print("Error in fetching data")
        attempts += 1
    # wait for a few seconds before trying again
    time.sleep(SLEEP_TIME)



if success:
    plant_inputs =  response['data'][0]
    x1 = plant_inputs['x1']
    x2 = plant_inputs['x2']
    x3 = plant_inputs['x3']
else:
    x1 = X1_DEFAULT
    x2 = X2_DEFAULT
    x3 = X3_DEFAULT


print(x1,x2,x3)
