import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# NOTES: Ramzan Eid is Gazetted Holiday (it is not marked as such in data tho)
# Guru Govind Singh Jayanti is to be considered as Restricted Holiday even though it is marked as Observance for two years but it is marked as 
# Restricted Holiday for the other 5 years

# Date is in form, date_num (MONTH IN HINDI!!), eg, 1 जनवरी
# Weekday is also in Hindi, eg, शनिवार
# Holiday Name
# Type of Holiday
# These two dictionaries map Hindi months and weekdays to English counterparts or numbers
month_hindi_to_english = {
	'जुलाई': 7, 
	'मई': 5, 
	'फरवरी': 2,
	'जनवरी': 1,
	'जून': 6,
	'अगस्त': 8,
	'नवंबर': 11, 
	'अप्रैल': 4, 
	'अक्टूबर': 10,
	'सितंबर': 9,
	'मार्च': 3,
	'दिसंबर': 12
}

weekday_hindi_to_english = {
	'रविवार': 'SUNDAY', 
	'शनिवार': 'SATURDAY', 
	'सोमवार': 'MONDAY', 
	'बुधवार': 'WEDNESDAY',
	'शुक्रवार': 'FRIDAY',
	'मंगलवार': 'MONDAY',
	'गुरुवार': 'THURSDAY'
}


# Fetching only,
# Federal/National Holidays = 1
# Common Local Holidays = 4194304 (Bakri Eid, Ramzan Eid)
# Important Observances = 16 (Ambedkar, Guru Gobind)
# Major Christian = 4096 (Not that useful)
# Major Muslim = 65536 (just the two Eids)
# Major Hinduism = 1048576 (just Ram Navami)
# Optional Holiday = 134217728 (bunch of useful holidays that we can filter through)

def holiday_scraper():
	url_template = "https://www.timeanddate.com/holidays/india/"

	# One list for each column in the required table so that we can easily convert it to a dataframe
	# years = []
	# months = []
	# days = []
	weekdays = []
	names = []
	types = []
	dates = []

	for year in range(2011, 2018):
		url = url_template + str(year)

		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")

		holiday_table_rows = soup.select("#holidays-table tbody tr")

		for table_row in holiday_table_rows:
			# There's certain empty rows in the table which will terminate the program
			# Each such empty row has its "id" property as "hol_{month_initial}", example, "hol_jan", "hol_feb", etc.
			# So here if its an empty row, the regex match will return True and so skip that row, 
			# else if its not an empty row, its id is something different and so regex match will return None and start processing this row
			if re.match("hol_[a-z]*", table_row['id']) is not None:
				continue

			holiday_day, holiday_month = table_row.select("th")[0].contents[0].strip().split()
			holiday_weekday = table_row.select("td")[0].contents[0].strip()
			holiday_title = table_row.select("td")[1].contents[0].contents[0].strip()
			holiday_type = table_row.select("td")[2].contents[0].strip()

			holiday_month = month_hindi_to_english[holiday_month]
			holiday_weekday = weekday_hindi_to_english[holiday_weekday]

			date = str(year) + "-" + str(holiday_month) + "-" + str(holiday_day)

			dates.append(date)
			# years.append(year)
			# months.append(holiday_month)
			# days.append(holiday_day)
			weekdays.append(holiday_weekday)
			names.append(holiday_title)
			types.append(holiday_type)

	# This is used for crosschecking whether correct number of entries were fetched
	print(len(names))

	dates = pd.to_datetime(dates)
	# holiay_df = pd.DataFrame({'Name': names, 'Day': days, 'Month': months, 'Year': years, 'Weekday': weekdays, 'Type': types})
	holiay_df = pd.DataFrame({'Date': dates, 'Name': names, 'Weekday': weekdays, 'Type': types})

	print(holiay_df.head())

	holiay_df.to_csv('../data/holidays_in_india_2011_2017.csv', index=False)


def get_unique_holidays():
	holiday_df = pd.read_csv('../data/holidays_in_india_2011_2017.csv')

	unique_holiday_names = holiday_df['Name'].unique()
	unique_holiday_names_types = []
	# print(unique_holiday_names)

	for name in unique_holiday_names:
		# print("{} : {}".format(name, holiday_df[holiday_df['Name'] == name].iloc[0]['Type']))
		# print(holiday_df[holiday_df['Name'] == name].iloc[0]['Type'])
		unique_holiday_names_types.append(holiday_df[holiday_df['Name'] == name].iloc[0]['Type'])

	unique_holiday_df = pd.DataFrame({'Name': unique_holiday_names, 'Type': unique_holiday_names_types})

	print(unique_holiday_df.head())

	unique_holiday_df.to_csv('../data/unique_holidays_and_types.csv', index=False)

get_unique_holidays()