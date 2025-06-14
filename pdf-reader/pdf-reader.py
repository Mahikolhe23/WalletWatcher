import pdfplumber
import pandas as pd
from copy import deepcopy

def get_pdf_data(pdf_path):
    pdf = pdfplumber.open(pdf_path)

    result = []
    current_client_name = None
    current_site_name = None
    current_location_name = None

    for page in pdf.pages:
        tables = page.extract_tables()
        if not tables:
            continue

        for table in tables:
            for row in table:                
                line = [l for l in row if l is not None]
                if not any(line):
                    continue

                # 1. Detect new client
                client_match = next((l for l in line if l.startswith("Client:")), None)
                if client_match:
                    current_client_name = client_match.split("Client:")[1].strip()
                    # Create/find client
                    client_entry = next((c for c in result if c["client"] == current_client_name), None)
                    if not client_entry:
                        client_entry = {"client": current_client_name, "sites": []}
                        result.append(client_entry)
                    continue

                # 2. Detect new site
                site_match = next((l for l in line if l.startswith("Site:")), None)
                if site_match:
                    current_site_name = site_match.split("Site:")[1].strip()
                    # Create/find site in current client
                    site_entry = next((s for s in client_entry["sites"] if s["site"] == current_site_name), None)
                    if not site_entry:
                        site_entry = {"site": current_site_name, "locations": []}
                        client_entry["sites"].append(site_entry)
                    continue

                # 3. Detect new location
                location_match = next((l for l in line if l.startswith("Location:")), None)
                if location_match:
                    current_location_name = location_match.split("Location:")[1].strip()
                    # Create/find location in current site
                    location_entry = next((l for l in site_entry["locations"] if l["location"] == current_location_name), None)
                    if not location_entry:
                        location_entry = {"location": current_location_name, "assets": []}
                        site_entry["locations"].append(location_entry)
                    continue

                # 4. Skip header row
                if any("Asset ID" in l for l in line):
                    continue



                # 5. Parse asset line (if it starts with numeric Asset ID)
                if str(line[0]).isnumeric:
                    asset = {
                        "Asset ID": line[0],
                        "Description": line[1],
                        "User": line[2],
                        "Test Instrument": line[3],
                        "Date": line[4],
                        "Retest Period": line[5],
                        "Next Test": line[6],
                        "Result": line[7]
                    }

                    # Ensure location_entry is available
                    if current_client_name and current_site_name and current_location_name:
                        # Refresh parent references (in case structure changed mid-page)
                        client_entry = next((c for c in result if c["client"] == current_client_name), None)
                        site_entry = next((s for s in client_entry["sites"] if s["site"] == current_site_name), None)
                        location_entry = next((l for l in site_entry["locations"] if l["location"] == current_location_name), None)
                        location_entry["assets"].append(asset)

    return result

def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem

def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pd.DataFrame(flatten_json(data_in))

def pdf_to_csv():
    pdf_file_path = '/Users/mahendrakolhe/Downloads/3-06-26 Tenterfield REPORT NM.pdf'
    csv_file_path = './pdf-extractor/output_hierarchical.csv'

    json_data = get_pdf_data(pdf_file_path)

    df_data = json_to_dataframe(json_data)

    df = pd.DataFrame(df_data)
    df.columns = ['client','site','location','Asset ID','Description','User','Test InstrSeaward','Date','Retest Period','Next Test','Result']
    df.to_csv(csv_file_path, index=False)


def get_report():
    pdf_to_csv()
    csv_file_path = './pdf-extractor/output_hierarchical.csv'
    

get_report()    



