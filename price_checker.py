import requests
from bs4 import BeautifulSoup

def get_etn_price():
    """
    Fetches the price for a bus ticket from Monterrey to Mexico City from the ETN website.
    """
    url = "https://etn.com.mx/english/monterrey-bus-travel.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with the route information
        # The table is not clearly marked, so I'll find the FAQ header and then the table after it.
        faq_header = soup.find('h2', string='Frequently Asked Questions (FAQ)')
        if not faq_header:
            # Fallback: The page structure might have changed. Let's look for the specific text.
            # I will search for the row containing the route directly.
            all_text = soup.get_text()
            if "Monterrey Central a la Ciudad de México Central Norte" in all_text:
                # This is a bit of a hack, but if the table is gone, I can still find the price.
                # I will find the price in the text.
                import re
                match = re.search(r"Monterrey Central a la Ciudad de México Central Norte\s*(\$\d{1,3}(,\d{3})*(\.\d{2})?)\s*MXN", all_text)
                if match:
                    price = match.group(1)
                    return f"The price for a bus ticket from Monterrey to Mexico City on ETN is: {price} MXN"
            return "Price table or route information not found on the page."


        table = faq_header.find_next('table')
        if not table:
             # Let's try searching for the table in the whole document again, just in case the header finding failed.
            table = soup.find('table')
            if not table:
                return "Price table not found on the page."


        # Find the correct row in the table
        rows = table.find_all('tr')
        for row in rows:
            # The structure is a bit odd, with the route name and price in the same cell sometimes.
            # I will look for the text in the whole row.
            row_text = row.get_text()
            if "Monterrey Central a la Ciudad de México Central Norte" in row_text:
                # The price is in the same row. I'll extract it.
                # I'll look for the price in the format $XXX.XX MXN
                import re
                match = re.search(r"(\$\d{1,3}(,\d{3})*(\.\d{2})?)\s*MXN", row_text)
                if match:
                    price = match.group(1)
                    return f"The price for a bus ticket from Monterrey to Mexico City on ETN is: {price} MXN"

        return "Route from Monterrey to Mexico City not found in the table."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print(get_etn_price())
