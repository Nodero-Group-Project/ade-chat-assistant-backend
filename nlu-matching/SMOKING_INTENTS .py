SMOKING_INTENTS = [
    # --- Core smoking status ---
    "find_smoking_status_overview",       # regular smoker / ex-smoker / never smoked, general split
    "find_daily_smoking_rate",
    "find_smoking_prevalence_trends",     # change over time / historical trend

    # --- Demographic breakdowns ---
    "find_smoking_by_age",
    "find_smoking_by_sex",
    "find_smoking_by_ethnicity",
    "find_smoking_by_region",             # regional council / territorial authority
    "find_smoking_by_deprivation_index",  # NZDep / socioeconomic deprivation
    "find_smoking_by_occupation",
    "find_smoking_by_income",
    "find_smoking_by_education_level",

    # --- Specific population groups ---
    "find_youth_smoking_statistics",
    "find_smoking_during_pregnancy",
    "find_secondhand_smoke_exposure",

    # --- Fallback ---
    "general_smoking_query"
]