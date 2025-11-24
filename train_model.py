import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, cohen_kappa_score
import pickle

# Download NLTK data
print("Downloading NLTK data...")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load the dataset
print("Loading dataset...")
data_path = 'archive/training_set_rel3.tsv'
try:
    df = pd.read_csv(data_path, sep='\t', encoding='ISO-8859-1')
except FileNotFoundError:
    print(f"Error: File not found at {data_path}")
    exit(1)

# Select relevant columns
df = df[['essay_id', 'essay_set', 'essay', 'domain1_score']]

# Clean text function
def clean_text(text):
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Apply cleaning
print("Preprocessing text...")
df['cleaned_essay'] = df['essay'].apply(clean_text)

# Initialize TF-IDF Vectorizer
print("Extracting features...")
vectorizer = TfidfVectorizer(max_features=5000)

# Fit and transform the essays
X = vectorizer.fit_transform(df['cleaned_essay']).toarray()
y = df['domain1_score']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize RandomForest Regressor
print("Training model (this may take a while)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)
print("Model trained successfully!")

# Predict on test set
y_pred = model.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Calculate Cohen's Kappa Score
y_pred_rounded = np.round(y_pred).astype(int)
kappa = cohen_kappa_score(y_test.astype(int), y_pred_rounded, weights='quadratic')
print(f"Quadratic Weighted Kappa: {kappa}")

# Save model and vectorizer
print("Saving model...")
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved to disk.")
