# Automated Essay Scoring

A web application for automated essay scoring using machine learning. This application allows users to register, log in, and submit essays to receive an instant score based on a pre-trained model.

## Features

*   **User Authentication**: Secure user registration and login functionality.
*   **Automated Scoring**: Instant essay scoring using a Machine Learning model.
*   **Text Preprocessing**: Advanced text cleaning and processing using NLTK.
*   **User Dashboard**: Personalized view for logged-in users.

## Technologies Used

*   **Backend**: Flask (Python)
*   **Database**: MongoDB
*   **Machine Learning**: Scikit-learn, NLTK, Pandas, NumPy
*   **Frontend**: HTML/CSS (Templates)

## Prerequisites

Before running the application, ensure you have the following installed:

*   Python 3.x
*   MongoDB (running locally on default port 27017)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AUTOMATED-ESSAY-SCORING
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK data:**
    The application will attempt to download necessary NLTK data on first run, but you can also install them manually if needed.

## Usage

1.  **Train the Model:**
    If you haven't trained the model yet, run the training script:
    ```bash
    python train_model.py
    ```
    This will generate `model.pkl` and `vectorizer.pkl`.

2.  **Run the Application:**
    ```bash
    python app.py
    ```

3.  **Access the App:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

4.  **Register/Login:**
    Create a new account or log in to start scoring essays.

## Project Structure

*   `app.py`: Main Flask application file.
*   `train_model.py`: Script to train the machine learning model.
*   `requirements.txt`: List of Python dependencies.
*   `templates/`: HTML templates for the web interface.
*   `static/`: Static files (CSS, JS, images).
*   `model.pkl`: Serialized machine learning model.
*   `vectorizer.pkl`: Serialized text vectorizer.
