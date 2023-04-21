from datetime import datetime, timedelta

import random
import string

# Get the current date and time in UTC+1
now = datetime.utcnow() + timedelta(hours=1)  # Add 1 hour to get UTC+1

# Format the date and time
formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

# Print the formatted date and time


#this is for reference in wallet if the reference is not provided
# Define the length of the random string
length = 12

# Generate the random string
random_string = ''.join(random.choice(string.digits) for _ in range(length))

# Store the random string in a variable
ref = random_string

# Print the generated random string


