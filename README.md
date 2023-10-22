
# ReconSphere - OSINT Subdomain Enumeration Tool

ReconSphere is an open-source intelligence (OSINT) tool for subdomain enumeration. It fetches subdomains from various sources and provides information such as IP addresses and status codes for each subdomain. It also supports brute-force subdomain enumeration.

## Features

- Fetch subdomains from multiple sources.
- Resolve and display IP addresses for subdomains.
- Display HTTP status codes for subdomains.
- Brute-force subdomain enumeration.
- Option to save results to an output file.

## Usage

To use ReconSphere, you can follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/Paresh-Maheshwari/ReconSphere
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
    python ReconSphere.py <target_domain> [-o <output_file>] [other options]

      <target_domain>: The target domain for subdomain enumeration.
      -o <output_file>: (Optional) Specify an output file to save the results.
      -h or --help: (Optional) Display help message and exit.

    Osint Enumeration Options:
      -osint or --osint: (Optional) Run OSINT subdomain enumeration.
      -s or --status-code: (Optional) Display HTTP status codes for subdomains.
      -ip or --ip: (Optional) Display IP addresses for subdomains.

    Brute-force Enumeration Options:
     -bf or --bruteforce: (Optional) Run subdomain brute-force enumeration.
     -w <wordlist>: (Optional) Specify the path to the wordlist file for brute-force enumeration.

      
    ```
## Examples
### OSINT Subdomain Enumeration 
1. Enumerate subdomains for a domain without displaying IP addresses or status codes:

```
python ReconSphere.py -d example.com --osint 
```

2. Enumerate subdomains, display status codes, and save results to an output file:

```
python ReconSphere.py -d example.com -osint -o output.txt -s
```


3. Enumerate subdomains, display status codes, ip address and save results to an output file:

```
python ReconSphere.py -d example.com  -s -ip
```

### Brute-force Subdomain Enumeration

1. Run brute-force subdomain enumeration using a wordlist file:
    
```
python ReconSphere.py -d example.com -w wordlist.txt -bf
```

## Results
ReconSphere will fetch subdomains and provide a table with the following information:

![image](https://github.com/Paresh-Maheshwari/ReconSphere/assets/70533309/ab529880-fb6d-48a5-a791-22af7c446cad)



## Contributors
 [@Paresh-Maheshwari](https://www.github.com/Paresh-Maheshwari)


## Contact
For questions or issues, please open an issue on GitHub.


Make sure to replace `<target_domain>` with the actual domain name and customize the contributor and contact sections with relevant information. You can also provide a link to the GitHub repository where the code is hosted.
