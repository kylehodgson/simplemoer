#!/usr/bin/env pythob
from client import WattTime

# see https://www.watttime.org/api-documentation/#register-new-user for more 
response=WattTime.register("freddo","the_frog","freddo@frog.org")
print(f"response: {response}")
