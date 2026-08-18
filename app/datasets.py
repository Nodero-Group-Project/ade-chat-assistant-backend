DATASETS = [
    {
        "id": "CEN23_HAD_020",
        "name": "Cigarette smoking behaviour, ethnicity, age, and gender for the census usually resident population count aged 15 years and over, (RC, TALB, Health), 2013, 2018, and 2023 Censuses",
        "description": "Cigarette smoking behaviour, ethnicity (detailed total responses level 4), age (life cycle groups), and gender for the census usually resident population count aged 15 years and over, for regional councils, territorial authorities and Auckland local boards, health regions, health districts, 2013, 2018, and 2023 Censuses."
    },
    {
        "id": "CEN23_HOU_001",
        "name": "Access to basic amenities, total household income, and tenure of household for households in occupied private dwellings, (RC, TALB, SA2, Health), 2018 and 2023 Censuses",
        "description": "Access to basic amenities (total responses), total household income, and tenure of household (level 1) for households in occupied private dwellings, for regional councils, territorial authorities and Auckland local boards, statistical area 2, health regions, health districts, 2018 and 2023 Censuses.",
    },
    {
        "id": "CEN23_FHH_017",
        "name": "Access to telecommunication systems, ethnicity, age, and gender for people in households in occupied private dwellings, (RC, TALB, SA2, Health), 2013, 2018, and 2023 Censuses",
        "description": "Access to telecommunication systems (total responses), ethnicity (grouped total responses level 1), age (life cycle groups), and gender for people in households in occupied private dwellings, for regional councils, territorial authorities and Auckland local boards, statistical area 2, health regions, health districts, 2013, 2018, and 2023 Censuses.",
    },
    {
        "id": "CEN23_EDU_003",
        "name": "Highest qualification, industry, and gender for the employed census usually resident population count aged 15 years and over, (RC, TALB, SA2, Health), 2013, 2018, and 2023 Censuses",
        "description": "Highest qualification, industry (level 1), and gender for the employed census usually resident population count aged 15 years and over, for regional councils, territorial authorities and Auckland local boards, statistical area 2, health regions, health districts, 2013, 2018, and 2023 Censuses."
    },
    {
        "id": "CEN23_HAD_014",
        "name": "Activity limitations, main means of travel to education, and age for the census usually resident population count aged 5 years and over who are studying, (RC, TALB, Health), 2018 and 2023 Censuses",
        "description": "Activity limitations, main means of travel to education, and age (5-year groups) for the census usually resident population count aged 5 years and over who are studying (part time or full time) in any educational institute, from early education (childcare) to tertiary education, for regional councils, territorial authorities and Auckland local boards, health regions, health districts, 2018 and 2023 Censuses."
    },
]

INTENTS = [
    "find_population_estimates",
    "find_population_projections",
    "find_census_data",
    "find_migration_statistics",
    "find_birth_death_statistics",
    "find_ethnicity_data",
    "find_age_sex_demographics",
    "find_education_statistics",
    "find_qualification_statistics",
    "find_student_travel_statistics",
    "find_crime_justice_statistics",
    "find_health_statistics",
    "find_smoking_alcohol_drug_statistics",
    "find_disability_statistics",
    "find_activity_limitation_statistics",
    "find_housing_statistics",
    "find_household_amenities_statistics",
    "find_household_family_statistics",
    "find_household_income_statistics",
    "find_tenure_statistics",
    "find_wellbeing_statistics",
    "find_religion_statistics",
    "find_language_statistics",
    "find_telecommunications_access_statistics",
    "find_internet_digital_access_statistics",
    "find_employment_statistics",
    "find_unemployment_statistics",
    "find_industry_employment_statistics",
    "find_occupation_statistics",
    "find_wages_income_statistics",
    "find_labour_force_statistics",
    "find_gdp_national_accounts",
    "find_trade_import_export_statistics",
    "find_price_inflation_statistics",
    "find_business_demographics",
    "find_industry_sector_statistics",
    "find_tourism_statistics",
    "find_government_finance_statistics",
    "find_environmental_statistics",
    "find_agriculture_statistics",
    "find_energy_statistics",
    "find_transport_travel_statistics",
    "find_regional_area_statistics",
    "find_local_board_statistics",
    "find_health_region_district_statistics",
    "find_statistical_area_data",
    "compare_across_census_years",
    "compare_across_geographic_areas",
    "general_query",
]


def datasets():
    return DATASETS


def intents():
    return INTENTS
