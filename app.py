from flask import Flask, request, jsonify, render_template
from google_sheets_updater import update_scores
import csv
import os

app = Flask(__name__)

STUDENT_NAMES = []

def load_student_data(csv_filename='student_data.csv'):
    """
    Loads a list of student names from student_data.csv (using the "Full Name" column).
    """
    names = []
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Full Name", "").strip()
                if name:
                    names.append(name)
    else:
        print(f"Warning: {csv_filename} not found. No student data loaded.")
    return names

def load_student_mapping(csv_filename='student_data.csv'):
    """
    Reads student_data.csv and returns a dictionary mapping student name (normalized)
    to their Google Sheet ID.
    Assumes the CSV has headers "Full Name" and "GoogleSheet ID".
    """
    mapping = {}
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Full Name", "").strip()  # use uppercase for matching
                sheet_id = row.get("Googlesheet ID", "").strip()
                if name and sheet_id:
                    mapping[name] = sheet_id
                print(mapping)
    else:
        print(f"Warning: {csv_filename} not found. No student mapping loaded.")
    return mapping

@app.before_request
def startup():
    # Load student names (for autocomplete) at startup
    global STUDENT_NAMES
    STUDENT_NAMES = load_student_data('student_data.csv')
    print("Loaded student names:", len(STUDENT_NAMES))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete')
def autocomplete():
    """
    Returns up to 10 names from STUDENT_NAMES that contain the query string (case-insensitive).
    """
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])

    # Use fuzzy matching via thefuzz
    from thefuzz import process
    matches = process.extract(query, STUDENT_NAMES, limit=10)
    result_names = [m[0] for m in matches if m[1] > 70]
    return jsonify(result_names)

@app.route('/update-scores', methods=['POST'])
def update():
    data = request.get_json()
    column_name = data.get('columnName', '').strip()
    results = data.get('results', {})
    # Expected results format: { "first": [...], "second": [...], "third": [...], "last": [...] }

    # Define scoring adjustments for each category
    adjustments = {
        "first": 1.0,
        "second": 0.5,
        "third": 0.2,
        "last": -0.5
    }

    # Build a dictionary of student scores (use uppercase for matching)
    student_scores = {}
    for category, names in results.items():
        for name in names:
            key = name.strip().upper()
            student_scores[key] = student_scores.get(key, 0) + adjustments.get(category, 0)

    if not column_name:
        return jsonify({"success": False, "error": "No column name specified."})
    if not student_scores:
        return jsonify({"success": False, "error": "No student scores provided."})

    # Load the student mapping from student_data.csv
    student_mapping = load_student_mapping('student_data.csv')
    if not student_mapping:
        return jsonify({"success": False, "error": "Student mapping not loaded from CSV."})

    # Group the student_scores by their GoogleSheet ID
    sheet_groups = {}  # key: sheet_id, value: dict of {student_name: score}
    missing_mapping = []  # student names not found in mapping
    for student, score in student_scores.items():
        sheet_id = student_mapping.get(student)
        if sheet_id:
            sheet_groups.setdefault(sheet_id, {})[student] = score
        else:
            missing_mapping.append(student)

    # Process each sheet group
    updated_students_set = set()
    for sheet_id, group_scores in sheet_groups.items():
        # Create the full URL from the sheet ID
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        # Use default sheet name "Data" (or change if needed)
        sheet_name = "Data"
        print(f"Processing sheet with ID {sheet_id}: {sheet_url}")
        update_scores(group_scores, sheet_url, sheet_name, column_name)
        updated_students_set.update(group_scores.keys())

    # Combine students not found in mapping and not updated
    not_updated = set(student_scores.keys()) - updated_students_set
    if not_updated:
        return jsonify({
            "success": False,
            "error": f"The following names were not updated (not found in their assigned sheet): {', '.join(not_updated)}"
        })
    elif missing_mapping:
        return jsonify({
            "success": False,
            "error": f"The following names have no assigned GoogleSheet ID in the CSV: {', '.join(missing_mapping)}"
        })
    else:
        return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
