from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

def extract_keywords(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract keywords from meta tags
    meta_keywords = soup.find('meta', {'name': 'keywords'})
    keywords = meta_keywords.get('content') if meta_keywords else ''

    # Extract keywords from headings (h1, h2)
    heading_keywords = [heading.text.strip() for heading in soup.find_all(['h1', 'h2'])]

    # Extract keywords from paragraphs (p)
    paragraph_keywords = [paragraph.text.strip() for paragraph in soup.find_all('p')]

    # Extract keywords from anchor text (a)
    anchor_keywords = [anchor.text.strip() for anchor in soup.find_all('a')]

    # Combine all extracted keywords
    all_keywords = [keyword.strip() for keyword in [keywords] + heading_keywords + paragraph_keywords + anchor_keywords if keyword.strip()]
    
    return all_keywords

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        html_content = get_html_content(url)
        
        if html_content:
            keywords = extract_keywords(html_content)
            return jsonify({"url": url, "keywords": keywords})
        else:
            return jsonify({"error": "Failed to fetch content. Check the URL and try again."}), 500

    return jsonify({"message": "Working"})

if __name__ == "__main__":
    app.run(debug=True)
