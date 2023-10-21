
import dns.resolver
import requests
import re
import argparse
import concurrent.futures
import time

from colorama import Fore, Style

# Function to print colored text
def colored_print(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

# ASCII art with colored text and your name
ascii_art = f"""
{Fore.RED}██████  {Fore.GREEN}██████  ██████  {Fore.YELLOW}████████ {Fore.CYAN}███    ██ {Fore.MAGENTA}███████ {Fore.BLUE}██████  ██   ██ ███████ {Fore.RED}██████  {Fore.GREEN}███████ 
{Fore.RED}██   ██ {Fore.GREEN}██      ██      {Fore.YELLOW}██    ██ {Fore.CYAN}████   ██ {Fore.MAGENTA}██      {Fore.BLUE}██   ██ ██   ██ ██      {Fore.RED}██   ██ {Fore.GREEN}██      
{Fore.RED}██████  {Fore.GREEN}█████   ██      {Fore.YELLOW}██    ██ {Fore.CYAN}██ ██  ██ {Fore.MAGENTA}███████ {Fore.BLUE}██████  ███████ █████   {Fore.RED}██████  {Fore.GREEN}█████   
{Fore.RED}██   ██ {Fore.GREEN}██      ██      {Fore.YELLOW}██    ██ {Fore.CYAN}██  ██ ██ {Fore.MAGENTA}     ██ {Fore.BLUE}██      ██   ██ ██      {Fore.RED}██   ██ {Fore.GREEN}██
{Fore.RED}██   ██ {Fore.GREEN}███████ ██████  {Fore.YELLOW}████████ {Fore.CYAN}██   ████ {Fore.MAGENTA}███████ {Fore.BLUE}██      ██   ██ ███████ {Fore.RED}██   ██ {Fore.GREEN}███████ 
            

"""

# Print the colored ASCII art
print(ascii_art)


# ANSI escape codes for text color
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
CYAN = '\033[96m'
# Function to resolve IP addresses for subdomains
def resolve_subdomain_ips(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        return [str(rdata) for rdata in answers]
    except dns.resolver.NXDOMAIN:
        return ["Not Found"]
    except dns.resolver.Timeout:
        return ["Timeout"]
    except dns.resolver.NoAnswer:
        return ["Not Found"]
    except Exception as e:
        return [str(e)]

# Function to fetch subdomains from various sources
def fetch_subdomains_from_sources(domain):
    # URLs to fetch subdomains from various sources
    urls = [
        f"https://rapiddns.io/s/{domain}/#result",
        f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=text&fl=original&collapse=urlkey",
        f"https://crt.sh/?q=%.{domain}",
        f"https://crt.sh/?q=%.%.{domain}",
        f"https://crt.sh/?q=%.%.%.{domain}",
        f"https://crt.sh/?q=%.%.%.%.{domain}",
        f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns",
        f"https://api.hackertarget.com/hostsearch/?q={domain}",
        f"https://urlscan.io/api/v1/search/?q={domain}",
        f"https://jldc.me/anubis/subdomains/{domain}",
        f"https://www.google.com/search?q=site%3A{domain}&num=100",
    #    f"https://www.bing.com/search?q=site%3A{domain}&count=50"
    ]

    subdomains = set()

    def fetch_subdomains_from_url(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                matches = re.findall(r'([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])\.' + re.escape(domain), response.text)
                full_subdomains = [f"{match}.{domain}" for match in matches]
                subdomains.update(full_subdomains)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_subdomains_from_url, urls))

# Now you have the results of the executions

    return subdomains

# Main function for OSINT
def osint(domain, output_file=None, display_status_code=False, display_ip=False):
    start_time = time.time()
    print("ReconSphere - Fetching subdomains. Please wait...\n")

    subdomains = fetch_subdomains_from_sources(domain)
    

    subdomain_status = {}
    status_counts = {}

    def check_subdomain_status(subdomain):
    
        url = f"http://{subdomain}"
        try:
            response = requests.head(url)
            final_url = response.url
            status_code = response.status_code
            if final_url.startswith("https"):
                url = final_url  # Use the HTTPS URL if available
        except requests.exceptions.RequestException:
            status_code = "Error"

        if status_code in status_counts:
            status_counts[status_code] += 1
        else:
            status_counts[status_code] = 1

        return status_code
        
    # Initialize a variable to keep track of the index
    index = 0


    if display_status_code and display_ip:
        header = f"\n|{'No.':<4} |{'Subdomain':<40}||{'Status Code':<10}|            |{'IP Address':<20}|"
    elif display_status_code:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|{'Status Code'}|"
    elif display_ip:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|{'IP Address'}|"
    else:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|"

    # Print the header with green text
    print(GREEN + header + RESET)

    for subdomain in subdomains:
        index += 1

        output_line = f"|{index:<4}  {subdomain:<40}"
        
        if display_status_code:
            status_code = check_subdomain_status(subdomain)
            # Display status code in red if it's an error
            if status_code == 'Error':
                output_line += RED + f"{status_code:<20}" + RESET
            else:
                output_line += f"{status_code:<20}"
        if display_ip:
            ips = resolve_subdomain_ips(subdomain)
            output_line += f"|{''.join(ips):<20}"
        # Print the output line
        print(output_line)


        
    

    end_time = time.time()
    time_elapsed = end_time - start_time

    # Print the time elapsed and total subdomains found with color
    print(f"\n{GREEN}Time elapsed: {time_elapsed:.2f} seconds{RESET}\n")
    print("-" * 60)
    print(f"{GREEN}Total subdomains found: {len(subdomains)}{RESET}\n")

    if display_status_code:
        # Print the status code counts with color
        print(f"{CYAN}Status Code Counts:{RESET}")
        for code, count in status_counts.items():
            print(f"{CYAN}{code:<10}{count}{RESET}")


    if output_file:
        result_line = "\n".join(subdomains)
        with open(output_file, 'a') as f:
            f.write(f'{result_line}\n')

if __name__ == "__main__":
    print("ReconSphere - OSINT Subdomain Enumeration Tool")
    print("Author: @Paresh-Maheshwari")
    print("GitHub: https://github.com/Paresh-Maheshwari\n")

    parser = argparse.ArgumentParser(description="ReconSphere - OSINT Subdomain Enumeration Tool")
    parser.add_argument("domain", type=str, help="The target domain for subdomain enumeration")
    parser.add_argument("-o", "--output-file", type=str, help="Output file for subdomains")
    parser.add_argument("-s", "--status-code", action="store_true", help="Display status codes")
    parser.add_argument("-ip", "--ip", action="store_true", help="Display IP addresses")
    args = parser.parse_args()

    

    osint(args.domain, args.output_file, args.status_code, args.ip)
