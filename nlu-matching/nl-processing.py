"""
1. preprocess the raw user query
2. parse the user query:
intent, entities, and dimensions implied.
3. Action/response generation
"""
import re
import nltk
from nltk.corpus import stopwords

raw_user_input = "What is the average household income in Auckland for 2023?"

# to all lowercase
lower_raw_user_input = raw_user_input.lower()

# remove punctuation
cleaned_user_input = re.sub(r'[^\w\s]', '', lower_raw_user_input)

# remove white space
cleaned_user_input = cleaned_user_input.strip()

# removing stop words

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
words = cleaned_user_input.split()
filtered_words = [word for word in words if word not in stop_words]
print(" ".join(filtered_words))