from PyPDF2 import PdfReader
import pdfplumber
import fitz

import re
import pandas as pd

import django
import os
import sys
sys.path.append('/home/mogs/Desktop/webdev_projects/uksupplychain/uksc_backend/uksc_backend_django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uksc_backend_django.settings')
django.setup()

from base.models import Supplier 

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

    header = """  Total 
Workers"""
    if header in text:
        # Extract the portion after the header
        text = text.split(header, 1)[1].strip()
    else:
        print("Header not found!")
        return pd.DataFrame()  # Return empty DataFrame if header is missing


    # Magic.
    text = text.replace(" Poland", "  Poland", 1)

    # Regex pattern for structured parsing
    pattern = get_pattern[company]

    # Use re.findall with the pattern
    matches = list(re.finditer(pattern, text, re.VERBOSE))  # Convert iterator to a list
    
    # Create a list of parsed data
    data = []
    for match in matches:
        data.append(match.groupdict())

    print(text[:300])
    df =  pd.DataFrame(data)
        
    # Return as a DataFrame for better handling
    return df

def find_country_in_address(address, total_text):
    # Sample cutoff address to search for
    for country in country_list:
        if (country in address):
            return country
    
    # Search for the cutoff address in the text
    first_10_chars = address[:10]
    if first_10_chars in total_text:
        # Find all country names in the text that come after the cutoff address
        after_cutoff = first_10_chars + total_text.split(first_10_chars, 1)[1][:150]  # Get everything after the cutoff address

        # Check for any country name in the remaining text
        for country in country_list:
            if country in after_cutoff:
                return country
    else:
        print(first_10_chars)
        print(address)
        return None

def extract_text_from_pdf(file_path, company):
    if (company == "Sainsburys"):
        reader = PdfReader(file_path)
        names = []
        addresses_all = []
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
        total_text = ""
        for page_num, page in enumerate(doc):
            addresses = []
            total_text += reader.pages[page_num].extract_text()  # Extract text from each page

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
                                addresses_all.append(line)
                        if (index == 2):
                            if (line != ''):
                                sectors.append(line)
                        if (index == 3):
                            if (re.match(r'(\d+)', line)):
                                workers.append(int(line))


        for address_line in addresses_all:
            country = find_country_in_address(address_line, total_text)
            countries.append(country)
        print(len(names))
        print(len(addresses_all))
        print(len(sectors))
        print(len(workers))
        print(len(countries))
        workers.insert(0, "workers")

        data = {
            "supplier": names,
            "address": addresses_all,
            "sector": sectors,
            "workers": workers,
            "country": countries
        }

        df = pd.DataFrame(data)

        df = df.iloc[1:].reset_index(drop=True)

        return df

    else:
        """Extracts text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


if __name__ == "__main__":

    data_definition = [
        {
            "company": "Tesco",
            "filename": "/home/mogs/Desktop/webdev_projects/uksupplychain/uksc_backend/uksc_backend_django/data/tesco_2024.pdf",
            "year": "2024"
        },
         {
            "company": "Sainsburys",
            "filename": "/home/mogs/Desktop/webdev_projects/uksupplychain/uksc_backend/uksc_backend_django/data/sainsburys_2024_food.pdf",
            "year": "2024"
        },
          {
            "company": "Asda",
            "filename": "/home/mogs/Desktop/webdev_projects/uksupplychain/uksc_backend/uksc_backend_django/data/asda_2024.csv",
            "year": "2024"
        }
    ]

    total_data = pd.DataFrame()

    # supplier, address, country, workers, sector
    for row in data_definition:
        match row["company"]:
            case "Tesco":
                df = parse_pdf_text(extract_text_from_pdf(row["filename"], row["company"]), row["year"], row["company"])
                df['year'] = row["year"]
                df["source_business"] = row["company"]
                df['sector'] = None
                df = df.rename(columns={'company_name': 'supplier', 'site_address': 'address', 'total_workers': 'workers'})
                print(df.columns)
                df = df.drop(['site_name'], axis=1)
                total_data = pd.concat([total_data, df])
                df.to_csv("tescos.csv", index=False)
            case "Sainsburys":
                df = extract_text_from_pdf(row["filename"], row["company"])
                df['year'] = row["year"]
                df["source_business"] = row["company"]
                # df = df.rename(columns={'country_name': 'country', 'name': 'supplier'})
                total_data =  pd.concat([total_data, df])
                df.to_csv("sainsburys.csv", index=False)
            case "Asda":
                df = pd.read_csv(row["filename"])
                df_filtered = df.filter(items=["name", "address", "country_name"])
                pattern = r"Asda \(Asda OSH facility list 2024 \(January - June 2024\)\)$"
                df_filtered["workers"] = None
                df_filtered["sector"] = None
               # Iterate over the rows
                for index, dat in df.iterrows():
                    print(dat)
                    if re.search(pattern, dat["contributor (list)"]):
                        # Extract the last digits from "number_of_workers"
                        if (dat["number_of_workers"] and not pd.isna(dat["number_of_workers"])):
                            last_digits = re.search(r"[\d-]+$", dat["number_of_workers"])
                            if last_digits:
                                df_filtered.at[index, "workers"] = last_digits.group()

                        # Extract the last set of characters not including "|"
                        if (dat["sector"]):
                            last_sector = re.search(r"[^|]+$", dat["sector"])
                            if last_sector:
                                df_filtered.at[index, "sector"] = last_sector.group().strip()

                # Print or save the filtered DataFrame
                print(df_filtered)
                df_filtered['year'] = row["year"]
                df_filtered["source_business"] = row["company"]
                df_filtered = df_filtered.rename(columns={'name': 'supplier', 'country_name': 'country'})
                total_data = pd.concat([total_data, df_filtered])
                df_filtered.to_csv("asda.csv", index=False)
            case _:
                parsed_data = pd.DataFrame()
    
    total_data.to_csv("total_data.csv", index=False)
    for _, row in total_data.iterrows():
        Supplier.objects.create(
            supplier=row['supplier'],
            address=row['address'],
            country=row['country'],
            workers=row['workers'],
            sector=row['sector'],
            year=row['year'],
            source_business=row['source_business']
        )