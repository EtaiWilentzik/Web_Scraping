import os
import smtplib
from pathlib import Path
from email.message import EmailMessage
import ssl
import csv

import io

import xlsxwriter

def create_csv_from_list(data, file_name="data.csv"):
    print(data)
    with open(file_name, 'w', newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        fields = ["title", "company_name", "link", "requirements", "posted_date"]
        writer.writerow(fields)
        for row in data:
            writer.writerow(
                [row["title"], row["company_name"], row["company_link"], row["requirements"], row["posted_date"]])

    print("_________________")



def create_excel_from_list2(data, file_name="data.xlsx"):
    try:
        # Create a new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        # Define bold format for the header.
        header_format = workbook.add_format({'bold': True, 'font_size': 20,'color': 'red'})
        cell_format = workbook.add_format({'font_size': 20, 'text_wrap': True})

        # Add the header row.
        fields = ["title", "company_name", "link", "requirements", "posted_date"]
        for col_num, field in enumerate(fields):
            worksheet.write(0, col_num, field, header_format )

        # Write data to the worksheet.
        for row_num, row in enumerate(data, 1):
            worksheet.write(row_num, 0, row["title"], cell_format)
            worksheet.write(row_num, 1, row["company_name"], cell_format)
            worksheet.write(row_num, 2, row["company_link"], cell_format)
            worksheet.write(row_num, 3, row["requirements"], cell_format)
            worksheet.write(row_num, 4, row["posted_date"], cell_format)

        # Adjust column widths to fit content.
        worksheet.set_column(0, 4, 20)
        workbook.close()
        print(f"Excel file '{file_name}' created successfully with formatting!")
    except Exception as e:
        print(f"An error occurred: {e}")
def send_email(send_to, body, files=[], send_from='etaiwil2000@gmail.com',password='', port=465, smpt_server="smtp.gmail.com",
               subject="משרות חדשות רלוונטיות", ):
    password = os.getenv('EMAIL_PASSWORD')  # used App passwords from google to generate a password
    # https://support.google.com/mail/thread/205453566/how-to-generate-an-app-password?hl=en
    em = EmailMessage()
    em['Subject'] = subject
    em['From'] = send_from
    em['To'] = send_to
    em.set_content(body)
    context = ssl.create_default_context()
    for file in files:
        try:
            file_path = Path(file)
            # print(file_path)
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = file_path.name
                file_type = file_path.suffix

            # Add the file to the email as an attachment
            em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        except Exception as e:
            print(f"Failed to attach {file}: {e}")
            return

    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(send_from, password)
        server.send_message(em)
        server.quit()

# send_email("etaiwil2000@gmail.com", body="this is etai email", files=["data.csv"])
