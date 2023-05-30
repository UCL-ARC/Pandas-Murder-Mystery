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
# identify suspect member(s)
identify_suspects = (
    get_fit_now_members.loc[
        (get_fit_now_members["membership_status"] == "gold")
        & (get_fit_now_members["id"].str[:3] == "48Z")
    ])


# %%
display(identify_suspects)
identify_suspects.info()
get_fit_now_check_in.info()

#check suspects were in gym
confirm_suspects = get_fit_now_check_in.loc[get_fit_now_check_in['membership_id'].isin(identify_suspects["id"])
                                   & (get_fit_now_check_in['check_in_date'] == 20180109)]

display(confirm_suspects)

#identify car and driver
confirm_suspects.info()
drivers_license.info()

identify_driver = drivers_license.loc[(drivers_license['plate_number'].str.contains("H42W")) & (drivers_license['gender'] == "male")]
display(identify_driver)

# %%
display(Markdown("## Clue 4"))
display(
    Markdown(
        interview.loc[interview["person_id"].isin(suspect["person_id"])][
            "transcript"
        ].iloc[0]
    )
)

# %%
mastermind_concert = (
    drivers_license.loc[
        (drivers_license["height"].isin(range(65, 68)))
        & (drivers_license["car_make"] == "Tesla")
        & (drivers_license["hair_color"] == "red")
        & (drivers_license["gender"] == "female")
    ]
    .merge(person, left_on="id", right_on="license_id", suffixes=["_driver", "_person"])
    .merge(
        (
            facebook_event_check_in.assign(
                date=pd.to_datetime(facebook_event_check_in["date"], format="%Y%m%d")
            )
            .set_index("date")
            .loc["12/2017"]
            .reset_index()
            .query("event_name == 'SQL Symphony Concert'")
        ),
        left_on="id_person",
        right_on="person_id",
    )
)

# %%
display(mastermind_concert)

# %%
mastermind = person.loc[
    person["id"].isin(mastermind_concert.drop_duplicates()["person_id"])
]

# %%
display(mastermind)

# %%
query = f"INSERT INTO solution VALUES (1, '{mastermind['name'].iloc[0]}');SELECT value FROM solution;"
print(query)

# %% language="bash"
#
# sqlite3 sql-murder-mystery.db "INSERT INTO solution VALUES (1, 'Miranda Priestly');SELECT value FROM solution;"
