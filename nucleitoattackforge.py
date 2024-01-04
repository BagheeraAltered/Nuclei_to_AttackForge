import csv
import json
import requests

# Function to read and process the CWE library CSV file
def process_cwe_library(file_path):
    cwe_details = {}
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cwe_id = row['CWE-ID']
            cwe_details[cwe_id] = row
    return cwe_details

# Process the CWE library file
cwe_library_path = 'cwelibrary.csv'  # Replace with the actual path to the cwelibrary.csv file
cwe_details = process_cwe_library(cwe_library_path)

def construct_vulnerability(finding, cwe_details):
    template_name = finding["template-path"].split('/')[-1] if '/' in finding["template-path"] else finding["template-path"]
    cwe_id_raw = finding.get("info", {}).get("classification", {}).get("cwe-id", ["CHANGELATER"])[0]
    cwe_id = cwe_id_raw.replace("cwe-", "")  # Adjust for format in cwelibrary.csv
    cwe_info = cwe_details.get(cwe_id, None)

    # Extracting the curl-command field
    curl_command = finding.get('curl-command', 'Not Available')
 
    # Create vulnerability dictionary, using 'CHANGELATER' if specific cwe_info not available
    vulnerability = {
        "affected_asset": finding["host"],
        "vulnerability_title": finding["info"]["name"],
        "vulnerability_priority": "Medium",
        "vulnerability_severity": 5,  # Map this value appropriately
        "vulnerability_likelihood_of_exploitation": 5,  # Adjust this value as necessary
        "vulnerability_description": cwe_info["Description"] if cwe_info else "CHANGELATER",
        "vulnerability_attack_scenario": cwe_info["Extended Description"] if cwe_info else "CHANGELATER",
        "vulnerability_remediation_recommendation": "UPDATE",
        "vulnerability_proof_of_concept":  curl_command,
        "vulnerability_tags": [cwe_id] if cwe_id != "CHANGELATER" else ["CHANGELATER"],
        "vulnerability_visible": True,
    }
    print(f"Constructed Vulnerability: {vulnerability}")
    return vulnerability

# Prompt the user for AttackForge credentials
project_id = input("Enter the AttackForge Project ID: ")
auth_token = input("Enter the AttackForge API Bearer Token: ")

# Load the Nuclei output
with open('formatted_output.json', 'r') as file:
    nuclei_output = json.load(file)

# Construct the payload for the AttackForge API
vulnerabilities = []
for finding in nuclei_output:  # Loop over all findings
    vuln = construct_vulnerability(finding, cwe_details)
    if vuln:
        vulnerabilities.append(vuln)

payload = {
    "import_to_library": "Imported Vulnerabilities",
    "vulnerabilities": vulnerabilities
}

# AttackForge API endpoint
url = f'https://UPDATETHIS.attackforge.io/api/projects/{project_id}/vulnerabilities/import'
headers = {
    'Authorization': auth_token,
    'Content-Type': 'application/json',
    'Connection': 'close'
}

# Send the POST request without the proxies
response = requests.post(url, headers=headers, json=payload, verify=False)
print(response.status_code, response.reason)

# Check if the request was successful
if response.status_code == 200:
    print("Vulnerabilities imported successfully.")
    print(response.text)
else:
    print(f"Failed to import vulnerabilities. Response: {response.status_code} - {response.text}")

