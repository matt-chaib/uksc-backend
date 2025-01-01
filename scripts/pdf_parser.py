from PyPDF2 import PdfReader
import re
import pandas as pd

raw_text = """
Consorfruit - Espax  direct produce supplies PLC  Ctra. Seròs s/n Soses SOSES 25181  Spain  342 
Continental Fine Foods - Bury  Cranswick Plc  Roach Bank Road, Pilsworth Industrial Estate, Bury, United Kingdom, 
BL9 8RQ  United Kingdom  767 
Continental Wine & Food  Continental Wine & Food Ltd  trafalgar winery leeds road Huddersfield HD2 1YY  United Kingdom  20 
Coopera Solutions (Agrosol Export)  Glinwell Marketing Ltd  Paraje Loma del Viento, El Ejido, Spain N/A N/A 4716  Spain  286 
Coopval - Cooperativa Agricola dos Fruticultores do Cadaval 
"""

# Define a function to parse the text
def parse_pdf_text(text):

    header = "transparency in the supply chain."
    if header in text:
        # Extract the portion after the header
        text = text.split(header, 1)[1].strip()
    else:
        print("Header not found!")
        return pd.DataFrame()  # Return empty DataFrame if header is missing


    # Regex pattern for structured parsing
    pattern = r"""
        (?P<site_name>.+?)\s{2,}                # Site name until the first hyphen
        (?P<company_name>.+?)\s{2,}           # Company name, separated by spaces
        (?P<site_address>.+?)\s{2,}           # Site address, separated by spaces
        (?P<country>[A-Za-z\s]+)\s{2,}        # Country name
        (?P<total_workers>\d+|N/A)            # Total workers (number or N/A)
    """
    # Use re.findall with the pattern
    matches = re.finditer(pattern, text, re.VERBOSE)

    # Create a list of parsed data
    data = []
    for match in matches:
        data.append(match.groupdict())
    
    # Return as a DataFrame for better handling
    return pd.DataFrame(data)

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


if __name__ == "__main__":
    # print(extract_text_from_pdf("./data/tesco_2024.pdf"))

    # Parse the raw text
    parsed_data = parse_pdf_text(extract_text_from_pdf("./data/tesco_2024.pdf"))
    # Display the parsed data
    print(parsed_data)
    # parsed_data
    parsed_data.to_csv("parsed_suppliers.csv", index=False)
