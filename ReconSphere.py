
import dns.resolver
import requests
import re
import argparse
import concurrent.futures
import time
import contextlib
import sys
from tqdm import tqdm
from colorama import Fore, Style

# Function to print colored text
def colored_print(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

# ASCII art with colored text and your name
banner = f"""
{Fore.RED}██████  {Fore.GREEN}██████  ██████  {Fore.YELLOW}████████ {Fore.CYAN}███    ██ {Fore.MAGENTA}███████ {Fore.BLUE}██████  ██   ██ ███████ {Fore.RED}██████  {Fore.GREEN}███████ 
{Fore.RED}██   ██ {Fore.GREEN}██      ██      {Fore.YELLOW}██    ██ {Fore.CYAN}████   ██ {Fore.MAGENTA}██      {Fore.BLUE}██   ██ ██   ██ ██      {Fore.RED}██   ██ {Fore.GREEN}██      
{Fore.RED}██████  {Fore.GREEN}█████   ██      {Fore.YELLOW}██    ██ {Fore.CYAN}██ ██  ██ {Fore.MAGENTA}███████ {Fore.BLUE}██████  ███████ █████   {Fore.RED}██████  {Fore.GREEN}█████   
{Fore.RED}██   ██ {Fore.GREEN}██      ██      {Fore.YELLOW}██    ██ {Fore.CYAN}██  ██ ██ {Fore.MAGENTA}     ██ {Fore.BLUE}██      ██   ██ ██      {Fore.RED}██   ██ {Fore.GREEN}██
{Fore.RED}██   ██ {Fore.GREEN}███████ ██████  {Fore.YELLOW}████████ {Fore.CYAN}██   ████ {Fore.MAGENTA}███████ {Fore.BLUE}██      ██   ██ ███████ {Fore.RED}██   ██ {Fore.GREEN}███████ 
            

"""

# Print the colored ASCII art
print(banner)



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
    print(
        f"{Fore.GREEN}ReconSphere - Fetching subdomains. Please wait...{Style.RESET_ALL}"
    )

    subdomains = fetch_subdomains_from_sources(domain)

    # Initialize a dictionary to keep track of status code counts
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
        header = f"\n|{'No.':<4}|{'Subdomain':<40}|{'Status Code':<10}         |{'IP Address':<20}"
    elif display_status_code:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|Status Code|"
    elif display_ip:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|IP Address|"
    else:
        header = f"\n|{'No.':<4}  |{'Subdomain':<40}|"

    # Print the header with green text
    # Print the header with green text
    print(Fore.GREEN + header + Style.RESET_ALL)

    for subdomain in subdomains:
        index += 1

        output_line = f"|{index:<4}  {subdomain:<40}"

        if display_status_code:
            status_code = check_subdomain_status(subdomain)
            # Display status code in red if it's an error
            if status_code == 'Error':
                output_line += f"{Fore.RED}{status_code:<20}{Style.RESET_ALL}"
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
    print(
        f"{Fore.GREEN}Time elapsed: {time_elapsed:.2f} seconds{Style.RESET_ALL}"
        + "\n"
    )
    print("-" * 60)
    print(
        f"{Fore.GREEN}Total subdomains found: {len(subdomains)}{Style.RESET_ALL}"
        + "\n"
    )

    if display_status_code:
        # Print the status code counts with color
        print(f"{Fore.CYAN}Status Code Counts:{Style.RESET_ALL}")
        for code, count in status_counts.items():
            print(f"{Fore.CYAN}{code:<10}{count}{Style.RESET_ALL}")


    if output_file:
        result_line = "\n".join(subdomains)
        with open(output_file, 'a') as f:
            f.write(f'{result_line}\n')




# List to store found subdomains
found_subdomains = []

# Function to check if a subdomain exists in either HTTP or HTTPS
def check_subdomain(target_domain, subdomain):
    protocols = ["http", "https"]
    for protocol in protocols:
        url = f"{protocol}://{subdomain}.{target_domain}"
        with contextlib.suppress(requests.exceptions.RequestException):
            response = requests.get(url)
            if response.status_code == 200:
                found_subdomains.append(f"{subdomain}.{target_domain}")
                sys.stdout.write("\r{}    ".format("\n".join(found_subdomains)))
                sys.stdout.flush()
                if protocol == "http":
                    break  # If HTTP is successful, no need to check HTTPS

def brute_force_subdomains(target_domain, wordlist_file, output_file):
    common_subdomains = []

    try:
        with open(wordlist_file, "r") as file:
            common_subdomains = [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        print(f"Error: Wordlist file '{wordlist_file}' not found.")
        return

    total_words = len(common_subdomains)

    # Use multithreading for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_subdomain, target_domain, subdomain) for subdomain in common_subdomains]

        with tqdm(total=total_words, position=0, desc="Bruteforcing") as pbar:
            for _ in concurrent.futures.as_completed(futures):
                pbar.update(1)

    # Save found subdomains to the specified output file
    with open(output_file, "w") as output_file:
        for subdomain in found_subdomains:
            output_file.write(subdomain + "\n")





if __name__ == "__main__":
    print(
        f"{Fore.RED}ReconSphere - OSINT Subdomain Enumeration Tool{Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}Author: @Paresh-Maheshwari{Style.RESET_ALL}")
    print(Fore.CYAN + "GitHub: https://github.com/Paresh-Maheshwari\n" + Style.RESET_ALL)

    parser = argparse.ArgumentParser(description="ReconSphere - OSINT Subdomain Enumeration Tool")
    parser.add_argument("-d", "--domain", type=str, help="The target domain for subdomain enumeration")
    parser.add_argument("-o", "--output-file", type=str, help="Output file for subdomains")
    parser.add_argument("-s", "--status-code", action="store_true", help="Display status codes")
    parser.add_argument("-ip", "--ip", action="store_true", help="Display IP addresses")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file")
    parser.add_argument("-osint", action="store_true", help="Run OSINT subdomain enumeration")
    parser.add_argument("-bf", "--bruteforce", action="store_true", help="Run subdomain brute-force enumeration")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(
            f"{Fore.RED}Unrecognized arguments: {', '.join(unknown)}{Style.RESET_ALL}"
        )
    elif args.osint:
        osint(args.domain, args.output_file, args.status_code, args.ip)
    elif args.bruteforce:
        if args.wordlist is None:
            print(
                f"{Fore.RED}Please provide a wordlist using the -w option for brute-force enumeration.{Style.RESET_ALL}"
            )
        else:
            brute_force_subdomains(args.domain, args.wordlist, args.output_file)
    else:
        # Display available commands when no arguments are provided
        print(
            f"{Fore.YELLOW}Usage: python ReconSphere.py -d <target_domain> [other options]{Style.RESET_ALL}"
        )
        print(f"{Fore.YELLOW}Available Commands:{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}     -osint: Run OSINT subdomain enumeration{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}     -bf/--bruteforce: Run subdomain brute-force enumeration{Style.RESET_ALL}"
        )
        print("\nUse -h or --help for more information on specific commands.")
