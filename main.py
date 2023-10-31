import random
import pandas as pd
import datetime as dt
import smtplib
import config

chosen_letter = f"./letter_templates/letter_{random.randint(1,3)}.txt"

now = dt.datetime.now()
day = now.day
month = now.month

birthdays_data = pd.read_csv("birthdays.csv")
birthdays_df = pd.DataFrame(birthdays_data)

date_meet = birthdays_df.loc[
    (birthdays_df["day"] == day) & (birthdays_df["month"] == month)
]
name_email = date_meet[["name", "email"]]
name_email_dict = name_email.to_dict(orient="dict")
number_of_people_having_birthday = len(name_email_dict["name"])

email_sender = config.email_sender
password = config.password

for person in range(number_of_people_having_birthday):
    with open(chosen_letter) as letter:
        letter_text = letter.read()
    letter_replaced = letter_text.replace("[NAME]", name_email_dict["name"][person + 1])
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email_sender, password=password)
        connection.sendmail(
            from_addr=email_sender,
            to_addrs=name_email_dict["email"][person + 1],
            msg=f"Subject:Happy Birthday!\n\n{letter_replaced}",
        )
