
# ReconSphere - OSINT Subdomain Enumeration Tool

ReconSphere is an open-source intelligence (OSINT) tool for subdomain enumeration. It fetches subdomains from various sources and provides information such as IP addresses and status codes for each subdomain.

## Features

- Fetch subdomains from multiple sources.
- Resolve and display IP addresses for subdomains.
- Display HTTP status codes for subdomains.
- Option to save results to an output file.

## Usage

To use ReconSphere, you can follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/ReconSphere.git
   ```
2. Navigate to the project directory:

    ```
    cd ReconSphere
    ```
3. Install the required Python packages:

    ```    
    pip install -r requirements.txt
    ```

4. Run ReconSphere with the desired options. You can provide the target domain and specify additional options.

    ``` 
    python ReconSphere.py <target_domain> [-o <output_file>] [-s] [-ip]

    <target_domain>: The target domain for subdomain enumeration.
    
    -o <output_file>: (Optional) Specify an output file to save the results.
    
    -s or --status-code: (Optional) Display HTTP status codes for subdomains.
    
    -ip or --ip: (Optional) Display IP addresses for subdomains.
    ```
## Examples
Enumerate subdomains for a domain without displaying IP addresses or status codes:


```
python ReconSphere.py example.com
```
Enumerate subdomains, display status codes, and save results to an output file:

```
python ReconSphere.py example.com -o output.txt -s
```

## Results
ReconSphere will fetch subdomains and provide a table with the following information:






## Contributors
 [@Paresh-Maheshwari](https://www.github.com/Paresh-Maheshwari)


## Contact
For questions or issues, please open an issue on GitHub.


Make sure to replace `<target_domain>` with the actual domain name and customize the contributor and contact sections with relevant information. You can also provide a link to the GitHub repository where the code is hosted.
