from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import argparse
import sys
from urllib.parse import urlparse 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

os.system('clear')

parser = argparse.ArgumentParser()
parser.add_argument("--update", help="update the script to the latest version", action="store_true")
args = parser.parse_args()

if args.update:
    print('Code not done yet.')
    continuation = input('Run the script as it is? (Yes/No) ')
    if continuation.upper() == 'NO':
        sys.exit()

print("This script is a SEO tool that analyzes a given website and extracts important SEO elements such as headings, paragraphs, and images. It saves these elements in separate text    and also downloads all the images found on the website. The script also gives a count of the number of each element found on the website, making it easy to see which areas of the website need improvement in terms of SEO. This tool can be used by marketers and webmasters to optimize their website's visibility and ranking on search engines.") 
print('\n Developer: Hater\n')

url = input("Site URL: (Including protocol) ").strip()

try:
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        site_domain = url[8:]
        index = site_domain.find('/')
        site_domain = site_domain[:index]
        if not os.path.exists(site_domain):
            os.makedirs(site_domain)
            
        # Headings Level 1 and 2
        h1_elements = soup.find_all('h1')

        h2_elements = soup.find_all('h2')

        with open('{}/headings1.txt'.format(site_domain), 'w') as f1, open('{}/headings2.txt'.format(site_domain), 'w') as f2:
            f1.write('--== Headings Level 1 ==--\n')
            f2.write('--== Headings Level 2 ==--\n')

            if h1_elements != []:
                for h1 in h1_elements:
                    f1.write(h1.text + '\n')
            else:
                f1.write('No Level 1 Headings on this website\n')

            if h2_elements != []:
                for h2 in h2_elements:
                    f2.write(h2.text + '\n')
            else:
                f2.write('No Level 2 Headings on this website\n')
        
        # Paragraphs
        p_elements = soup.find_all('p')

        with open('{}/paragraph.txt'.format(site_domain), 'w') as p:
            p.write('--== Paragraphs Level 1 ==--\n')
            if p_elements != []:
                for element in p_elements:
                    p.write(element.text + '\n')
            else: 
                p.write('No Level 1 Paragraphs on this website\n')
        
        # Images
        images_copied = 0
        images_errors = 0
        img_elements = soup.find_all('img')
        try:
            for i, img_element in enumerate(img_elements):
                img_url = img_element.get('src')
                urllib.request.urlretrieve(img_url, '{}/image{}.jpg'.format(site_domain,i))
                i += 1
                images_copied += 1
        except ValueError:
            images_errors += 1
        except TypeError:
            images_errors += 1

        # Divs
        divs_copied = 0
        div_elements = soup.find_all('div')
        with open('{}/divs.txt'.format(site_domain), 'w') as d:
            d.write('--== Divs ==--\n')
            if div_elements != []:
                for div in div_elements:
                    d.write(div.text + '\n')
                    divs_copied += 1
            else: 
                d.write('No divs on this website\n')

        # print the results
        print("\n\n--== RESULTS ==--")
        print("Headings Level 1: {}".format(len(h1_elements)))
        print("Headings Level 2: {}".format(len(h2_elements)))
        print("Paragraphs: {}".format(len(p_elements)))
        print("Divs: {}".format(divs_copied))
        print("Images Found: {}".format(len(img_elements)))
        print("Images Copied: {}".format(images_copied))
        print("Errors: {}".format(images_errors))
        print('Files have been saved into folder {}'.format(site_domain[:index]))
    else:
        print(f'Failed to retrieve index.html. Website returned status code {r.status_code}')

except requests.exceptions.RequestException as e:
    print(f'An error occurred while making the HTTP request: {e}')