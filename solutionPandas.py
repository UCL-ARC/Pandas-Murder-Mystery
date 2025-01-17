# %% [markdown]
# # Pandas Murder Mystery
#
# A crime has taken place and the detective needs your help. The detective gave
# you the crime scene report, but you somehow lost it.
#
# ## Clue 1
#
# You vaguely remember that the crime was a **murder** that occurred sometime on
# **Jan. 15, 2018** and that it took place in **SQL City**. Start by retrieving
# the corresponding crime scene report from the police department's files. If
# you want to get the most out of this mystery, try to work through it only
# using your Python environment and refrain from using a notepad.

# %%
import pandas as pd
from IPython.display import Markdown, display

# %%
drivers_license = pd.read_csv("drivers_license.zip")
income = pd.read_csv("income.zip")
get_fit_now_members = pd.read_csv("get_fit_now_members.zip")
interview = pd.read_csv("interview.zip")
person = pd.read_csv("person.zip")
facebook_event_check_in = pd.read_csv("facebook_event_check_in.zip")
get_fit_now_check_in = pd.read_csv("get_fit_now_check_in.zip")
crime_scene_report = pd.read_csv("crime_scene_report.zip")

# view crime_scene_report df
# %%

crime_scene_report.info()
print(crime_scene_report)


# %% [markdown]
# ![image.png](https://mystery.knightlab.com/schema.png)

# %%
deposition = crime_scene_report.loc[(crime_scene_report['date'] == 20180115) & (crime_scene_report['type'] == "murder") & (crime_scene_report['city'] == "SQL City")]
display(deposition)
# %%
# set Pandas to return upto 250chars to prevent text from trunccating
pd.set_options("max_colwidth",250)


# %%
display("## Clue 2")
display(deposition['description'])


# Identify the witness who lives in the last house on Northwestern Dr
person.info()
print(person)
# %%
nwd_addresses = person.loc[person["address_street_name"] == "Northwestern Dr"]
]
display(nwd_addresses)

#narrow down
witness_1 = nwd_addresses.loc[
    (nwd_addresses['address_street_name'] == "Northwestern Dr") 
    & (nwd_addresses['address_number'] == nwd_addresses['address_number'].max())
]

# %%
witness_2 = person.loc[
    (person["name"].str.contains("Annabel"))
    & (person["address_street_name"] == "Franklin Ave")
]
display(witness_2)

# %%
witnesses = pd.concat([witness_1, witness_2])

# %%
clue_3 = interview.loc[interview["person_id"].isin(witnesses["id"])]


# %%
display("## Clue 3")
display(clue_3)

# %%

#identify car and driver
confirm_suspects.info()
drivers_license.info()

# rename drivers_license['id'] to 'license_id'] so can be merged with person data
drivers_license.rename(columns = {'id':'license_id'}, inplace = True)

#merge person and drivers_license
driver_person_info = pd.merge(person, drivers_license, on=['license_id'])

# identify driver
identify_driver = driver_person_info.loc[(driver_person_info['plate_number'].str.contains("H42W"))]
display(identify_driver)

#check if member and get member info
get_fit_now_members.info()
get_member_data = get_fit_now_members.loc[get_fit_now_members['person_id'].isin(identify_driver["id"])]
display(get_member_data)

#have they made a statemen?
member_statement = interview.loc[interview['person_id'].isin(get_member_data['person_id'])]
display(member_statement)

# %%
display("## Clue 4")
#clue 4
display(member_statement)
   
#find driver of the tesla
# %%
tesla_drivers = (
    drivers_license.loc[
        (drivers_license["height"].isin(range(65, 68)))
        & (drivers_license["car_make"] == "Tesla")
        & (drivers_license["hair_color"] == "red")
        & (drivers_license["gender"] == "female")
    ])

# %%
display(tesla_drivers)

#merge info re: tesla driver registration with person data
tesla_driver_person_info = pd.merge(person, tesla_drivers, on=['license_id'])

#check to see who booked concert
facebook_event_check_in.info()
facebook_event_check_in.head()

 driver_event_bookings = facebook_event_check_in.loc[facebook_event_check_in['person_id'].isin(tesla_driver_person_info['id'])]
 display(driver_event_bookings)

# %%
suspect = person.loc[person['id'].isin(driver_event_bookings['person_id'])]
display (suspect)

# %%
query = f"INSERT INTO solution VALUES (1, '{suspect['name'].iloc[0]}');SELECT value FROM solution;"
print(query)

# %% language="bash"
#
# sqlite3 sql-murder-mystery.db "INSERT INTO solution VALUES (1, 'Miranda Priestly');SELECT value FROM solution;"
