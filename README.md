Quizlet Live Score Recorder
The Quizlet Live Score Recorder is a web application built with Flask that allows educators to record and update student scores from Quizlet Live games directly into Google Sheets. The app supports multiple Google Sheets by mapping each student to their assigned Google Sheet ID using a CSV file (student_data.csv). It also features an autocomplete function for quick and accurate student name entry.

Features
Score Recording: Record scores for different prize categories (First, Second, Third, and Last) with custom weightings.

Google Sheets Integration: Automatically updates the specified column in Google Sheets using the Google Sheets API.

Student Mapping: Uses a CSV file to map student names to their specific Google Sheet IDs.

Autocomplete: Provides an autocomplete feature (powered by fuzzy matching) for student name entry.

Responsive Design: Uses Bootstrap for a clean, modern, and education-friendly interface.

Project Structure
graphql
Copy
quizlet_quiz_recorder/
├── app.py                   # Main Flask application file
├── google_sheets_updater.py # Module for Google Sheets API integration and score updates
├── templates/
│   └── index.html           # Frontend HTML template with Bootstrap styling
├── student_data.csv         # CSV file containing student names and their GoogleSheet IDs
├── credentials.json         # Google API credentials (keep this file secure)
└── README.md                # This README file
Installation
Clone the Repository:

bash
Copy
git clone <repository-url>
cd quizlet_quiz_recorder
Create and Activate a Virtual Environment (Recommended):

On Windows:

bash
Copy
python -m venv venv
venv\Scripts\activate
On macOS/Linux:

bash
Copy
python -m venv venv
source venv/bin/activate
Install Dependencies:

Ensure you have a requirements.txt file containing:

nginx
Copy
Flask
gspread
oauth2client
thefuzz
Then run:

bash
Copy
pip install -r requirements.txt
If you don't have a requirements.txt file, install the dependencies manually:

bash
Copy
pip install Flask gspread oauth2client thefuzz
Add Your Google API Credentials:

Place your credentials.json file in the project root. This file is necessary for authenticating with the Google Sheets API.

Configuration
Student Data CSV:
The student_data.csv file must include at least two columns:

Full Name – The student's full name.

GoogleSheet ID – The ID of the Google Sheet where the student's data is stored.

Google Sheets Requirements:
Each Google Sheet should have:

A worksheet named "Data" (or another name if you change the default in the code).

A header row (Row 1) that includes the column name (e.g., Quiz20250325) that you wish to update.

Student names (from Row 2 onward) in Column E.

Column Name:
When running the app, you must specify the exact header (column name) you want to update in your Google Sheets.

Usage
Run the Flask Application:

bash
Copy
python app.py
Access the Application:
Open your web browser and navigate to http://127.0.0.1:5000.

Record Scores:

Enter the column/header name (e.g., Quiz20250325) in the designated input.

For each prize category (First, Second, Third, Last), use the autocomplete feature to select the student name, then click the plus (+) button to add them.

Once all entries are complete, click the "Execute" button.

Update Process:
The application will:

Use the student_data.csv file to map each student's name to their corresponding Google Sheet ID.

Build a full Google Sheet URL for each student and update the specified column if the student's name is found.

Alert you if any student names were not updated (e.g., not found in their assigned sheet).

Troubleshooting
Google Sheets Not Updating:
Verify that the column header you enter matches exactly with the header in your Google Sheet and that student names in the sheet match (or are fuzzy-close to) the names provided.

CSV Files Not Found:
Ensure that both student_data.csv and credentials.json are in the project root.

Authentication Issues:
Check that your credentials.json file is valid and that your service account has permission to edit the Google Sheets.

License
GNU General Public License v3.0

Acknowledgments
Flask

gspread

oauth2client

TheFuzz

Bootstrap

