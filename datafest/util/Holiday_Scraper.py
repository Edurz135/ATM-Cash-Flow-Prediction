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
month_on_english = {
	'Jul': 7, 
	'May': 5, 
	'Feb': 2,
	'Jan': 1,
	'Jun': 6,
	'Aug': 8,
	'Nov': 11, 
	'Apr': 4, 
	'Oct': 10,
	'Sep': 9,
	'Mar': 3,
	'Dec': 12
}

weekday_on_english = {
	'Sunday': 'SUNDAY', 
	'Saturday': 'SATURDAY', 
	'Monday': 'MONDAY', 
	'Wednesday': 'WEDNESDAY',
	'Friday': 'FRIDAY',
	'Tuesday': 'TUESDAY',
	'Thursday': 'THURSDAY'
}

"""
	Scrapes holidays from 2011 to 2017 and saves it in the csv file "peru_holidays" in data folder
	Has multiple entries for some specific dates which has to be manually removed if scraping is done again
"""
def holiday_scraper():
	url_template = "https://www.timeanddate.com/holidays/peru/"

	# One list for each column in the required table so that we can easily convert it to a dataframe
	weekdays = []
	names = []
	types = []
	dates = []

	for year in range(2020, 2025):
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


			holiday_month = month_on_english[holiday_month]
			holiday_weekday = weekday_on_english[holiday_weekday]

			date = str(year) + "-" + str(holiday_month) + "-" + str(holiday_day)

			dates.append(date)
			weekdays.append(holiday_weekday)
			names.append(holiday_title)
			types.append(holiday_type)

	# This is used for crosschecking whether correct number of entries were fetched
	print(len(names))

	dates = pd.to_datetime(dates)
	holiday_df = pd.DataFrame({'Date': dates, 'Name': names, 'Weekday': weekdays, 'Type': types})

	print(holiday_df.head())

	holiday_df.to_csv('./datafest/data/peru_holidays.csv', index=False)


"""
	This function maps each unique Holiday Name to their respective unique Holiday Type so as to avoid Holidays with multiple Types
"""
def get_unique_holidays():
	holiday_df = pd.read_csv('./datafest/data/peru_holidays.csv')

	unique_holiday_names_dict = dict()
	unique_holiday_names = set(holiday_df['Name'])	

	for name in unique_holiday_names:
		unique_holiday_names_dict[name] = holiday_df[holiday_df['Name'] == name].iloc[0]['Type']

	return unique_holiday_names_dict


"""
	Used for filtering holidays, the holidays which must be retained are to be specified in the set given below
	Also does case by case fixing of data
"""
def filter_holidays():
	original_holidays_set = {'Ambedkar Jayanti', 'Pongal', 'Holi', 'Independence Day', 
	'Beti Bachao, Beti Padhao Campaign Launch Day', 'Raksha Bandhan (Rakhi)', 'First day of Passover', 
	'Maharishi Dayanand Saraswati Jayanti', 'Vasant Panchami', 'Bakr Id/Eid ul-Adha', 
	'Guru Nanak Jayanti', 'Maha Shivaratri/Shivaratri', 'Shivaji Jayanti', 'Holika Dahana', 
	"Guru Tegh Bahadur's Martyrdom Day", 'Christmas', 'Maundy Thursday', 'December Solstice', 
	"Father's Day", 'Halloween', "Valentine's Day", 'Janmashtami', 'Makar Sankranti', 
	'Maha Navami', 'Chinese New Year', 'Ganesh Chaturthi/Vinayaka Chaturthi', 'Maha Saptami', 
	'Chhat Puja (Pratihar Sashthi/Surya Sashthi)', 'May Day', 'Guru Purnima', 'Mahatma Gandhi Jayanti', 
	'Republic Day', 'Dussehra', 'Vaisakhi', "New Year's Eve", "New Year's Day", 'Rath Yatra', 
	'Govardhan Puja', 'Muharram/Ashura', 'Guru Govind Singh Jayanti', 'Guru Ravidas Jayanti', 
	'Buddha Purnima/Vesak', 'June Solstice', 'Rama Navami', 'Onam', 'Friendship Day', 
	'Diwali/Deepavali', 'Jamat Ul-Vida', 'Birthday of Ravindranath', 'First Day of Hanukkah', 
	'Naraka Chaturdasi', 'Christmas Eve', 'Karaka Chaturthi (Karva Chauth)', "Mother's Day", 
	'March Equinox', "Hazarat Ali's Birthday", 'Parsi New Year', 'Ramzan Id/Eid-ul-Fitar', 
	'Maha Ashtami', 'Mesadi/Vaisakhadi', 'September Equinox', 'Easter Day', 'Bhai Duj', 
	'Last day of Hanukkah', 'Chaitra Sukhladi', 'Good Friday', 'Mahavir Jayanti', 
	'Maharishi Valmiki Jayanti', 'Milad un-Nabi/Id-e-Milad'}


	required_holidays_set = {'Ambedkar Jayanti', 'Pongal', 'Holi', 'Independence Day', 'Raksha Bandhan (Rakhi)', 
	'Bakr Id/Eid ul-Adha', 'Guru Nanak Jayanti', 'Maha Shivaratri/Shivaratri', 
	'Shivaji Jayanti', 'Holika Dahana', 'Christmas', "Father's Day", 'Halloween', "Valentine's Day", 'Janmashtami', 
	'Makar Sankranti', 'Maha Navami', 'Ganesh Chaturthi/Vinayaka Chaturthi', 
	'May Day', 'Guru Purnima', 'Mahatma Gandhi Jayanti', 'Republic Day', 'Dussehra', 
	"New Year's Eve", "New Year's Day", 'Muharram/Ashura', 'Guru Govind Singh Jayanti', 
	'Buddha Purnima/Vesak', 'Rama Navami', 'Onam', 'Friendship Day', 'Diwali/Deepavali', 
	'Jamat Ul-Vida', 'Christmas Eve', "Mother's Day", 'Parsi New Year', 
	'Ramzan Id/Eid-ul-Fitar', 'Easter Day', 'Bhai Duj', 'Good Friday', 
	'Mahavir Jayanti', 'Milad un-Nabi/Id-e-Milad'
	}

	holiday_df = pd.read_csv('./datafest/data/peru_holidays.csv')

	# Filter by required_holidays_set
	holiday_df_filtered = holiday_df[holiday_df.apply(lambda x: x['Name'] in required_holidays_set, axis=1)]

	unique_names_to_type_dict = get_unique_holidays()

	# There's two entries for Holi, one is Gazetted Holiday other is Restricted Holiday, so this ensures all are marked as Gazetted Holiday
	unique_names_to_type_dict['Holi'] = 'Gazetted Holiday'
	holiday_df_filtered['Type'] = holiday_df_filtered.apply(lambda x: unique_names_to_type_dict[x['Name']], axis=1)

	# Ramzan Eid has two Holiday Types, one is "Gazetted Holiday" and other is "Muslim, Common local holiday", so this is for fixing that
	holiday_df_filtered['Type'] = holiday_df_filtered['Type'].apply(lambda x: 'Gazetted Holiday' if x == 'Muslim, Common local holiday' else x)

	""" 
		Use this code block to determine whether there are multiple entries for certain days like 14th January of 2014 had 3 holidays on same day
		So there were 3 separate entries for same date
		In such case, you will have to manually clean the Holidays in India csv on your own
		vc = holiday_df_filtered['Date'].value_counts()
		print(vc[vc > 1])
	"""

	# Difference between how many holidays were removed
	print(len(holiday_df))
	print(len(holiday_df_filtered))

	holiday_df_filtered.to_csv('../data/peru_holidays_filtered.csv', index=False)

holiday_scraper()
# get_unique_holidays()
# filter_holidays()
