from docx import Document

from paths import REPO_ROOT


def extract_tables_from_docx(docx_file):
    # Load the Word document
    doc = Document(docx_file)

    # Array to store all tables
    tables_array = []

    # Iterate over each table in the document
    for table in doc.tables:
        # Create an array to store the current table's data
        table_data = []

        # Iterate over each row in the table
        for row in table.rows:
            row_data = []

            # Iterate over each cell in the row
            for cell in row.cells:
                row_data.append(cell.text.strip())

            # Add the row data to the table data
            table_data.append(row_data)

        # Add the current table data to the tables array
        tables_array.append(table_data)

    return tables_array


def test():
    # Specify your docx file path
    docx_file = REPO_ROOT / "timetable.docx"

    # Extract tables
    extracted_tables = extract_tables_from_docx(docx_file)

    # Print or process the extracted tables
    for table in extracted_tables:
        print(table)

    # convert every table to a csv file with table_X.csv
    # for i, table in enumerate(extracted_tables):
    #     with open(f"table_{i}.csv", "w") as f:
    #         for row in table:
    #             f.write(",".join(row) + "\n")
