from PyPDF2 import PdfReader
import pdfplumber
import fitz

import re
import pandas as pd

get_pattern = {
    "Tesco": r"""
        (?P<site_name>.+?)\s{2,}                # Site name until the first hyphen
        (?P<company_name>.+?)\s{2,}           # Company name, separated by spaces
        (?P<site_address>.+?)\s{2,}           # Site address, separated by spaces
        (?P<country>[A-Za-z\s]+)\s{2,}        # Country name
        (?P<total_workers>\d+|N/A)            # Total workers (number or N/A)
    """,
    "Sainsburys": r""""""
}

country_list = [
    "United Kingdom", "United States", "China", "Germany", "India", "Japan", "France", "Italy", "Brazil",
    "Canada", "Australia", "South Korea", "Spain", "Mexico", "Netherlands", "Russia", "Sweden", "Switzerland",
    "Belgium", "Singapore", "South Africa", "Austria", "Poland", "Turkey", "Norway", "Saudi Arabia", "Argentina",
    "United Arab Emirates", "Thailand", "Malaysia", "Israel", "Chile", "Nigeria", "Indonesia", "Denmark",
    "Finland", "Ireland", "Vietnam", "Egypt", "Chile", "Pakistan", "Romania", "Czech Republic", "Greece", 
    "New Zealand", "Portugal", "Hungary", "Israel", "Egypt", "South Africa", "Malaysia", "Philippines",
    "Colombia", "Peru", "Bangladesh", "Vietnam", "Nigeria", "Algeria", "Ukraine", "Poland", "Egypt", "Kazakhstan",
    "Morocco", "Jordan", "Iraq", "Kuwait", "Qatar", "Oman", "Kenya", "Ethiopia", "Zimbabwe", "Uzbekistan", 
    "Azerbaijan", "Belarus", "Sri Lanka", "Bulgaria", "Croatia", "Slovakia", "Slovenia", "Lithuania", "Latvia",
    "Estonia", "Macedonia", "Bosnia", "Montenegro", "Serbia", "Kosovo", "Albania", "Kosovo", "Armenia", 
    "Georgia", "Tanzania", "Uganda", "Angola", "Zambia", "Nepal", "Cambodia", "Laos", "Myanmar", "Mongolia",
    "Malawi", "Botswana", "Togo", "Benin", "Gabon", "Mauritius", "Seychelles", "Malta", "San Marino", "Monaco", "Scotland", "Wales"
]

# Define a function to parse the text
def parse_pdf_text(text, year, company):

    header = "transparency in the supply chain."
    if header in text:
        # Extract the portion after the header
        text = text.split(header, 1)[1].strip()
    else:
        print("Header not found!")
        return pd.DataFrame()  # Return empty DataFrame if header is missing


    # Regex pattern for structured parsing
    pattern = get_pattern[company]

    # Use re.findall with the pattern
    matches = re.finditer(pattern, text, re.VERBOSE)

    # Create a list of parsed data
    data = []
    for match in matches:
        data.append(match.groupdict())
    
    df =  pd.DataFrame(data)
    
    df['year'] = year
    
    # Return as a DataFrame for better handling
    return df

def find_country_in_address(address, total_text):
    # Sample cutoff address to search for
    for country in country_list:
        if (country in address):
            return country
    
    # Search for the cutoff address in the text
    if address in total_text:
        # Find all country names in the text that come after the cutoff address
        after_cutoff = address + total_text.split(address, 1)[1][:100]  # Get everything after the cutoff address

        # Check for any country name in the remaining text
        for country in country_list:
            if country in after_cutoff:
                return country
    else:
        return None

def extract_text_from_pdf(file_path, company):
    if (company == "Sainsburys"):
        reader = PdfReader(file_path)
        names = []
        addresses = []
        sectors = []
        workers = []
        countries = []

        doc = fitz.open(file_path)

        # Access the first page (0-indexed)
        page = doc[0]  # Change index for other pages if needed

        # Define the bounding box (bbox)
        bboxes = [
            fitz.Rect(52, 0, 95, 1200),
            fitz.Rect(99, 0, 193, 1000),
            fitz.Rect(195, 0, 261, 1000),
            fitz.Rect(262, 0, 305, 1000)
        ]

        for page_num, page in enumerate(doc):
            total_text = reader.pages[page_num].extract_text()  # Extract text from each page

            for index, bbox in enumerate(bboxes):
                # Extract text within the bbox
                text_in_bbox = page.get_text("blocks", clip=bbox)

                # Print the extracted text blocks
                for block in text_in_bbox:
                    block_text = block[4]  # Text content of the block

                    # If you want to further extract lines from the block, you can split by line breaks:
                    lines = block_text.split("\n")  # Split block text into individual lines
                    for line in lines:
                        line = line.strip()
                        if (index == 0):
                            if (line != ''):
                                names.append(line)
                        if (index == 1):
                            if (line != ''):
                                addresses.append(line)
                        if (index == 2):
                            if (line != ''):
                                sectors.append(line)
                        if (index == 3):
                            if (re.match(r'(\d+)', line)):
                                workers.append(int(line))


        for address_line in addresses:
            country = find_country_in_address(address_line, total_text)
            countries.append(country)
        print(len(names))
        print(len(addresses))
        print(len(sectors))
        print(len(workers))
        print(len(countries))
        workers.insert(0, "workers")

        data = {
            "Name": names,
            "Address": addresses,
            "Sector": sectors,
            "Workers": workers,
            "Country": countries
        }

        df = pd.DataFrame(data)
        df.to_csv("sainsburys.csv", index=False)
        return df

    else:
        """Extracts text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


if __name__ == "__main__":
    # print(extract_text_from_pdf("./data/tesco_2024.pdf"))

    data_definition = [
        # {
        #     "company": "Tesco",
        #     "filename": "./data/tesco_2024.pdf",
        #     "year": "2024"
        # },
         {
            "company": "Sainsburys",
            "filename": "./data/sainsburys_2024_food.pdf",
            "year": "2024"
        }
    ]

    for row in data_definition:
        match row["company"]:
            case "Tesco":
                parsed_data = parse_pdf_text(extract_text_from_pdf(row["filename"], row["company"]), row["year"], row["company"])

            case "Sainsburys":
                extract_text_from_pdf(row["filename"], row["company"])
                parsed_data = pd.DataFrame()
            case _:
                parsed_data = pd.DataFrame()

    # Parse the raw text
    # Display the parsed data
    print(parsed_data)
    # parsed_data
    # parsed_data.to_csv("parsed_suppliers.csv", index=False)
