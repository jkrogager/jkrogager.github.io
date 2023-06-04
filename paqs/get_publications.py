import json
import requests
from urllib.parse import urlencode
import os

# Function to fetch publications
def fetch_publications():
    base_url = "https://api.adsabs.harvard.edu/v1/search/query?"
    # api_key = "VO3ngz5JQrilUP0oNcndEylcoFL4Lv1Te2Ein6zF"
    api_key = os.environ.get("ADS_API_TOKEN")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    query = {
        "q": "full:PAQS+year:2021-",
        "fq": "database:astronomy",
        "fl": "title,author,abstract,year,pub,volume,page,bibcode,doi"
    }

    encoded_query = '&'.join([f"{key}={value}" for key, value in query.items()])
    # Send request to ADS API
    response = requests.get(f"{base_url}{encoded_query}", headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        publications = data["response"]["docs"]
        with open('result.json', 'w') as output:
            json.dump(publications, output, indent=4)
        return publications
    else:
        print("Failed to fetch publications.")
        return []


# Save JSON to a well-formatted text file
def save_to_file(publications):
    with open("publications.txt", "w") as file:
        json.dump(publications, file, indent=4)


# Generate HTML file with publications
def generate_html(publications):
    with open("publications.html", "w") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n")
        file.write("<head>\n")
        file.write("  <title>Publications related to PAQS</title>\n")
        file.write("  <link rel=\"stylesheet\" href=\"paqs.css\" />\n")
        file.write("  <link rel=\"icon\" href=\"images/4gpaqs.ico\">\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("""
    <header>
        <a id="header" href="index.html">Home</a>
        <div class="dropdown">
            <button class="dropbtn">Survey Details</button>
            <div class="dropdown-content">
              <a href="dlas.html">Intervening Absorbers</a>
              <a href="bals.html">Broad Absorption Line Quasars</a>
              <a href="facility.html">4MOST on the VISTA telescope</a>
              <a href="targets.html">Target selection</a>
            </div>
          </div> 
        <a id="header" href="publications.html">Publications</a>
        <a id="header" href="#contact">Contact</a>
    </header>""")
        file.write("  <h1>PAQS Publications</h1>\n")
        file.write("  <p class=\"centered\">Publications related to the Purely Astrometric Quasar Survey (PAQS)</p>\n")
        file.write("  <div class=\"publications\">\n")

        for publication in publications:
            title = publication.get("title", ["N/A"])[0]
            authors = ", ".join(publication.get("author", ["N/A"]))
            abstract = publication.get("abstract", "N/A")
            year = publication.get("year", "N/A")
            journal = publication.get("pub", "N/A")
            vol = publication.get("volume", "N/A")
            page = publication.get("page", ["N/A"])[0]
            doi = publication.get("doi", "N/A")
            bibcode = publication.get("bibcode", ["N/A"])
            url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract"
            reference = f"<i>{journal}</i> {vol}, {page} ({year})  <a href='{url}'>{bibcode}</a>"

            file.write(f"    <h3 id=\"title\">{title}</h3>\n")
            file.write(f"    <p id=\"ref\">{reference}</p>\n")
            file.write(f"    <p id=\"authors\"><strong>Authors:</strong> {authors}</p>\n")
            file.write(f"    <p id=\"abstract\"><strong>Abstract:</strong> {abstract}</p>\n")
            file.write("    <hr>\n")

        file.write("  </div>\n")
        file.write("""
    <div id="contact" class="centered">
        <h2>Contact</h2>
        <p>You can get in touch with the survey PI at the following address:<br>
        <span class="blockspam" aria-hidden="true">PLEASE GO AWAY!</span> <span style="color:#4c77ee"><!-- 234987 < >fsdglkj -->jens-kristian.krogager<!-- lasldih -->@<!-- we8734nasælk -->univ-lyon1.<!-- toasjsdkjh -->fr</span>
        </p>
    </div>
    """)
        
        file.write("</body>\n")
        file.write("</html>\n")

# Fetch publications and generate HTML file
publications = fetch_publications()
generate_html(publications)

