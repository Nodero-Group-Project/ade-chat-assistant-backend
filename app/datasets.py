DATASETS = [
    {
        "id": "CEN23_HAD_020",
        "name": "Cigarette smoking behaviour, ethnicity, age, and gender",
        "description": "Cigarette smoking behaviour by ethnicity, age, gender, location, and census year for 2013, 2018, and 2023.",
    },
    {
        "id": "CEN23_HOU_001",
        "name": "Access to basic amenities, household income, and tenure",
        "description": "Household amenities, household income, and tenure by location for 2018 and 2023.",
    },
    {
        "id": "CEN23_FHH_017",
        "name": "Access to telecommunication systems, ethnicity, age, and gender",
        "description": "Access to telecommunication systems by ethnicity, age, gender, location, and census year for 2013, 2018, and 2023.",
    },
    {
        "id": "CEN23_EDU_003",
        "name": "Highest qualification, industry, and gender",
        "description": "Highest qualification and industry by gender, location, and census year for 2013, 2018, and 2023.",
    },
    {
        "id": "CEN23_HAD_014",
        "name": "Activity limitations, travel to education, and age",
        "description": "Activity limitations and travel to education by age, location, and census year for 2018 and 2023.",
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
    "find_crime_justice_statistics",
    "find_health_statistics",
    "find_smoking_alcohol_drug_statistics",
    "find_disability_statistics",
    "find_housing_statistics",
    "find_household_family_statistics",
    "find_wellbeing_statistics",
    "find_religion_statistics",
    "find_language_statistics",
    "find_employment_statistics",
    "find_unemployment_statistics",
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
    "find_regional_area_statistics",
    "general_query",
]


def datasets():
    return DATASETS


def intents():
    return INTENTS
