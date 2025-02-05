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

    if (company == "Tesco"):
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
            fitz.Rect(50, 0, 290, 1200),
            fitz.Rect(292, 0, 432, 1000),
            fitz.Rect(434, 0, 660, 1000),
            fitz.Rect(662, 0, 725, 1000),
            fitz.Rect(727, 0, 782, 1000)
        ]
        total_text = ""
        
        for page_num, page in enumerate(doc):
            addresses = []
            total_text += reader.pages[page_num].extract_text()  # Extract text from each page

            for index, bbox in enumerate(bboxes):

                if (page_num == 0):
                    bbox.y0 = 300
                    bbox.y1  = 545
                else:
                    bbox.y0 = 15
                    bbox.y1  = 537

                if page_num == 1:
                    # Highlight the bbox
                    highlight = page.add_rect_annot(bbox)
                    highlight.set_colors({"stroke": (1, 0, 0), "fill": (1, 1, 0)})  # Red stroke, yellow fill
                    highlight.update()

                    # Save the modified PDF without incremental saving
                    output_path = "highlighted_output" + str(index) + ".pdf"
                    doc.save(output_path)
                    print(f"Highlighted PDF saved to {output_path}")

                # Extract text within the bbox
                text_in_bbox = page.get_text("blocks", clip=bbox)

                # Print the extracted text blocks
                for block in text_in_bbox:
                    block_text = block[4]  # Text content of the block
                    print("New block")
                    print(block_text)
                    # If you want to further extract lines from the block, you can split by line breaks:
                    line = block_text
                    print("lines")
               
                    line = line.strip()
                    if (index == 0):
                            names.append(line)
                    if (index == 1):
                        None
                            # addresses.append(line)
                            # addresses_all.append(line)
                    if (index == 2):
                            addresses.append(line)
                            addresses_all.append(line)
                            # sectors.append(None)
                            # sectors.append(line)
                    if (index == 3):
                            countries.append(line)
                    if (index == 4):
                            workers.append(line)

        # workers.insert(0, "workers")
        # addresses_all.insert(301, "Cranswick Plc") # If using company names

        addresses_all[294] = str.replace(addresses_all[294], """Lot A01-A12, Zone A, Phong Dien Industrial Zone Phong Dien Town, 
        Phong Dien District Phong Dien 530000""", "")
        addresses_all.insert(294, """Lot A01-A12, Zone A, Phong Dien Industrial Zone Phong Dien Town, 
Phong Dien District Phong Dien 530000""")

        addresses_all[846] = str.replace(addresses_all[846], """NO.133 SHUANGYUAN ROAD,CHENGYANG 
DISTRICT,QINGDAO,CHINA/NO.27-1,Tianshan 3rd Road, Daxin 
Street,Jimo District, Qingdao, China  Qingdao 266109""", "")
        addresses_all.insert(846, """NO.133 SHUANGYUAN ROAD,CHENGYANG 
DISTRICT,QINGDAO,CHINA/NO.27-1,Tianshan 3rd Road, Daxin 
Street,Jimo District, Qingdao, China  Qingdao 266109""")
        
        addresses_all[923] = str.replace(addresses_all[923], """CTRA. CUEVAS DEL ALMANZORA-AGUILAS KM.11 CUEVAS DEL ALMANZORA Cuevas de Almanzora 4610""", "")
        addresses_all.insert(924, """CTRA. CUEVAS DEL ALMANZORA-AGUILAS KM.11 CUEVAS DEL 
ALMANZORA Cuevas de Almanzora 4610""")
        
        addresses_all[952] = str.replace(addresses_all[952], """No.1358 & No. 1428 Jiahang Rd, Xuhang Town, Jiading District  
Shanghai 201808""", "")
        addresses_all.insert(953, """No.1358 & No. 1428 Jiahang Rd, Xuhang Town, Jiading District  
Shanghai 201808""") 

        data = {
            "supplier": names,
            "address": addresses_all,
            # "sector": sectors,
            "workers": workers,
            "country": countries
        }
        # Determine the number of rows (assuming all lists have the same length)
        num_rows = len(names)

        # Loop through each row and print the values
        for i in range(min(num_rows, 976)):  # Ensure only first 10 rows are printed
            print(f"Row {i+1}:")
            for key in data:
                print(f"{key.capitalize()}: {data[key][i]}")
            print()  # Blank line for better readability
        
        print(len(names))
        print(len(addresses_all))
        print(len(sectors))
        print(len(workers))
        print(len(countries))

        data_subset = {key: value[0:1137] for key, value in data.items()}
        for key, value in data_subset.items():
            print(f"Length of {key}: {len(value)}")
        df = pd.DataFrame(data_subset)

        df["sectors"] = None

        df = df.iloc[1:].reset_index(drop=True)

        return df

    else:
        """Extracts text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
def extract_asda_csv(row):
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
    return df_filtered



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
        if (row["company"] == "Asda"):
            df = extract_asda_csv(row)
        else:
            df = extract_text_from_pdf(row["filename"], row["company"])
            df['year'] = row["year"]
            df["source_business"] = row["company"]
            df['sector'] = None
        total_data = pd.concat([total_data, df])
        filename = row["company"] + ".csv"
        df.to_csv(filename, index=False)
    
    country_dictionary = {
        "Türkiye": "Turkey",
        "Cyprus (South)": "Cyprus",
        """Republic of                     +
        | Ireland""": "Ireland",
        "United States": "USA",
        "Scotland": "United Kingdom"
    }

    total_data['country'] = total_data['country'].apply(lambda x: country_dictionary.get(x, x))

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