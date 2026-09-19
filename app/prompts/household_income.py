def prompt():
    return """
Convert the user's English question into an API URL.

Never invent codes or values.

URL format:
https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_001,1.0/{Year}.{Location}.{Amenities}.{Income}.{Tenure}?dimensionAtObservation=AllDimensions

Use these codes for parameters in the URL:

Year:
2018, 2023

Location:
9999 = regional council
1 = Northland
2 = Auckland
3 = Waikato
4 = Bay of Plenty
5 = Gisborne
6 = Hawke's Bay
7 = Taranaki
8 = Manawatu / Whanganui
9 = Wellington
12 = West Coast
13 = Canterbury
14 = Otago
15 = Southland
16 = Tasman
17 = Nelson
18 = Marlborough
99 = Area Outside

Amenities:
0 = None of these
1 = Cooking facilities
2 = Tap water that is safe to drink
3 = Kitchen sink
4 = Refrigerator
5 = Bath or shower
6 = Toilet
99 = Total - access to basic amenities

Income:
1 = $20,000 or less
2 = $20,001 to $30,000
3 = $30,001 to $50,000
4 = $50,001 to $70,000
5 = $70,001 to $100,000
6 = $100,001 to $150,000
7 = $150,001 to $200,000
8 = $200,001 or more
99 = Total - total household income

Tenure:
001 = Dwelling owned / partly owned
003 = Dwelling held in a family trust
002 = Dwelling not owned / not held in a family trust
999 = Not elsewhere included
7777 = Total stated - tenure of household
9999 = Total - tenure of household

Rules:

* incomes are in dollar
* zero income = income 1
* If no amenities is specified = 99
* If no specific location or area is given = 9999
* If no income is specified = 99
* If no tenure is specified = 9999
* if income specified as more than a number or less than a number, select all values which is applied for the number. ex, more than 110000 = 6+7.
* Multiple values use "+", e.g. Refrigerator and Toilet = 4+6.
* If the requested year is unavailable, use 2023.
* Never guess a location code that has not been provided.
* Keep the dimension order exactly: Year.Location.Amenities.Income.Tenure
* Your response MUST be in these formats:
    if there is a URL -> API_URL:the url
    if no URL -> ERROR:the reason
"""
