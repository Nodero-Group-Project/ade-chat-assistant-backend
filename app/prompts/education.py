def prompt():
    return """
Convert the user's English question into an API URL.

Return ONLY the URL. If the request cannot be mapped unambiguously, return:
ERROR: <reason>

Never invent codes or values.

URL format:
https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_EDU_003,1.0/{Year}.{Location}.{Qualification}.{Industry}.{Age}.{Gender}?dimensionAtObservation=AllDimensions

Use these codes for parameters in the URL:

Year:
2013, 2018, 2023

Location:
9999 = regional council
99999 = health region/health district
999999 = territorial authority/Auckland local board

Qualification:
000 = No qualification
001 = Level 1 certificate
002 = Level 2 certificate
003 = Level 3 certificate
004 = Level 4 certificate
005 = Level 5 diploma
006 = Level 6 diploma
007 = Bachelor degree / level 7 qualification
008 = Post-graduate / honours degrees
009 = Masters degree
010 = Doctorate degree
011 = Overseas secondary school qualification
999 = Not elsewhere included
7777 = Total stated - highest qualification
9999 = Total - highest qualification

Industry:
9 = Total - industry
K = Financial / Insurance Services
S = Other Services
G = Retail Trade
L = Rental / Hiring / Real Estate Services
7 = Total stated - industry
A = Agriculture / Forestry / Fishing
C = Manufacturing
E = Construction
O = Public Administration / Safety
H = Accommodation / Food Services
P = Education / Training
J = Information Media / Telecommunications
M = Professional / Scientific / Technical Services
R = Arts / Recreation Services
B = Mining
F = Wholesale Trade
D = Electricity / Gas / Water / Waste Services
Q = Health Care / Social Assistance
N = Administrative / Support Services
T = Not Elsewhere Included
I = Transport / Postal / Warehousing

Age:
2 = 15-29
3 = 30-64
4 = 65+
5 = median
99 = total

Gender:
1 = male
2 = female
3 = another gender
99 = total

Rules:

* "youth" / "young people" = age 2
* "men" / "male" = gender 1
* "women" / "female" = gender 2
* "educated" = Qualification 9999
* "uneducated" = Qualification 000
* If no industry is specified = 9
* If no age is specified = 99
* If no gender is specified = 99
* If no specific location or area is given = 9999
* Multiple values use "+", e.g. Male and Female = 1+2.
* If the requested year is unavailable, use 2023.
* Never guess a location code that has not been provided.
* Keep the dimension order exactly: Year.Location.Qualification.Industry.Age.Gender.
* ONLY RETURN THE URL IF THERE WAS ANY or ERROR. NOTHING ELSE MATTERS.

"""
