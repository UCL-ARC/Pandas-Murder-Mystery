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

# find out more about the data frames
# %%
drivers_license.info()
income.info()
get_fit_now_members.info()
interview.info()
person.info()
facebook_event_check_in.info()
get_fit_now_check_in.info()
crime_scene_report.info()


# %% [markdown]
# ![image.png](https://mystery.knightlab.com/schema.png)

# %%
deposition = (
    crime_scene_report.assign(
        date=pd.to_datetime(crime_scene_report["date"], format="%Y%m%d")
    )
    .set_index("date")
    .loc["1/15/2018"]
    .query("type == 'murder' and city == 'SQL City'")
)
display(deposition)

# %%
display(Markdown("## Clue 2"))
display(Markdown(deposition["description"].values[0]))


# %%
def namestr(obj, namespace=locals()) -> str:
    return [name for name in namespace if namespace[name] is obj][0]


# %%
def print_table_names():
    print([namestr(d) for d in db])


# %%
for d in db:
    print(namestr(d))
    display(d.sample())
    print()

# %%
witness_1 = person.loc[person["address_street_name"] == "Northwestern Dr"].loc[
    lambda df: df["address_number"] == df["address_number"].max()
]
display(witness_1)

# %%
witness_2 = person.loc[
    (person["name"].str.contains("Annabel"))
    & (person["address_street_name"] == "Franklin Ave")
]
display(witness_2)

# %%
witnesses = pd.concat([witness_1, witness_2])

# %%
clue_3 = interview.loc[interview["person_id"].isin(witnesses["id"])].merge(
    witnesses, left_on="person_id", right_on="id"
)

# %%
display(Markdown("## Clue 3"))
for t in clue_3["transcript"]:
    display(Markdown(t))
    print()

# %%
suspect = (
    get_fit_now_members.loc[
        (get_fit_now_members["membership_status"] == "gold")
        & (get_fit_now_members["id"].str[:3] == "48Z")
    ]
    .merge(person, left_on="person_id", right_on="id", suffixes=["_gym", "_person"])
    .merge(
        drivers_license.loc[drivers_license["plate_number"].str.contains("H42W")],
        left_on="license_id",
        right_on="id",
        suffixes=["_person", "_driver"],
    )
).merge(
    get_fit_now_check_in.assign(
        check_in_date=pd.to_datetime(
            get_fit_now_check_in["check_in_date"], format="%Y%m%d"
        ),
    )
    .set_index("check_in_date")
    .loc["1/9/2018"],
    left_on="id_gym",
    right_on="membership_id",
)

# %%
display(suspect.T)

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
