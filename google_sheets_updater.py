import gspread
from oauth2client.service_account import ServiceAccountCredentials
from thefuzz import process

# Authenticate Google Sheets API using your credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def open_sheet(spreadsheet_url, sheet_name):
    spreadsheet = client.open_by_url(spreadsheet_url)
    return spreadsheet.worksheet(sheet_name)

def find_best_match(student_name, sheet_names):
    best_match, score = process.extractOne(student_name, sheet_names)
    return best_match.strip().title() if (best_match and score > 70) else None

def update_scores(student_scores, spreadsheet_url, sheet_name, column_name):
    sheet = open_sheet(spreadsheet_url, sheet_name)
    headers = sheet.row_values(1)
    # Assume student names are in Column E
    sheet_students = [name.strip().title() for name in sheet.col_values(5)]
    print(sheet_students)

    try:
        col_index = headers.index(column_name) + 1
    except ValueError:
        print(f"Error: Column '{column_name}' not found in Google Sheet.")
        return

    for student, score in student_scores.items():
        best_match = find_best_match(student, sheet_students)
        if best_match:
            cell_row = None
            for row_number, name in enumerate(sheet_students, start=1):
                if best_match == name:
                    cell_row = row_number
                    break
            if cell_row:
                sheet.update_cell(cell_row, col_index, score)
                print(f"Updated {best_match} with {score} in {column_name}")

if __name__ == "__main__":
    # Example usage:
    student_scores = {'JOHANNA ABARETA': 1.0, 'PAUL CEDRIC ACOSTA': 0.5, 'MAQUILYN ALEJANDRO': 0.2, 'MARIE ANTONETTE AMPO': -0.5}
    update_scores(student_scores, "https://docs.google.com/spreadsheets/d/1XZLxzVdqj937fw7CerpVSOfvpy3M2LkEINVwK8W9MmA/edit", "Data", "Quiz20250326")