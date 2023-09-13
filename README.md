# SEING: Search Engine Is Not Global

SEING, which stands for Search Engine Is Not Global, is an advanced search engine developed as a graduation project. Unlike traditional search engines, SEING specializes in searching Egyptian web content, providing a more focused and personalized experience for users seeking information relevant to Egypt. This README.md file offers comprehensive documentation on SEING, including its features, installation instructions, usage guidelines, and customization options.
Table of Contents

- Features
- Requirements
- Installation
- Getting Started
- Usage
  - Basic Search
  - Advanced Search
  - Crawling System
  - Page Rank Algorithm
  - Integration with Google and Bing
- Customization
- Contributing
- License

## Features

SEING offers a range of features designed to enhance the search experience for Egyptian web users:

- Egyptian Web Content: SEING exclusively indexes Egyptian web pages, ensuring search results are tailored to local needs.
- Full-Text Search: Powered by Elasticsearch, SEING provides fast and accurate full-text search capabilities.
- Crawling System: SEING includes a crawling system that allows users to submit Egyptian websites for indexing.
- Page Rank Algorithm: A Page Rank algorithm is integrated to rank search results based on authority and relevance.
- Integration with Google and Bing: SEING seamlessly integrates with Google and Bing, enabling users to toggle between searching only Egyptian websites or the broader web.

## Requirements

Before using SEING, ensure your system meets the following requirements:

- Python 3.7 or higher.
- Flask: Install it using pip install Flask.
- SQLAlchemy: Install it using pip install SQLAlchemy.
- Elasticsearch: An Elasticsearch server is required. Follow the official installation guide to set up Elasticsearch.
- Python packages listed in shell.nix file: Convert it into requirements.txt, Then install them using pip install -r requirements.txt.

## Installation

1. Clone the SEING repository to your local machine:

```bash
git clone https://github.com/yourusername/seing.git
```

2. Navigate to the project directory:

```bash
cd seing
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install the required Python packages:

```bash
pip install -r requirements.txt
```

6. Getting Started

Configure SEING by editing the search.py file by adding APIs. Ensure that the Elasticsearch server address and other settings are correctly set.

7. Start the SEING server:
```bash
python __main__.py
```
SEING is now running and accessible at http://localhost:5000. You can access the API and the web interface.

## Usage

### Basic Search

Use the SEING web interface to perform basic searches. Enter your query in the search bar and click "Search."
Advanced Search

For more advanced queries, use the API:

    Search: Send a GET request to http://localhost:5000/api/search?q=your_query to search for a query.

    Crawling: Use the API to submit URLs for crawling. See the Crawling System section for details.

    Customization: Modify the API routes and controllers to customize the behavior of SEING to suit your needs.

### Crawling System

SEING includes a web crawling system that allows users to index Egyptian web pages. To crawl a website from `http://localhost:5000/dbsocket`

The crawler will start indexing the specified website and add the pages to the search engine's index.
Page Rank Algorithm

SEING incorporates a Page Rank algorithm to rank search results. The Page Rank scores are calculated based on the links between pages. Higher Page Rank scores indicate more authoritative pages.
Integration with Google and Bing

SEING features seamless integration with Google and Bing. Users can toggle between searching only Egyptian websites and searching the broader web. This feature enhances the user experience by providing access to global information while maintaining a focus on Egyptian content.

## Customization

SEING is highly customizable to suit your specific requirements. You can:

    Modify the crawling system to index specific Egyptian websites or web pages.
    Customize the ranking algorithm to fine-tune search result rankings.
    Add additional filters or facets to the search results.
    Enhance the web interface with additional features or a different design.

## Contributing

We welcome contributions to SEING. If you would like to contribute, please follow our contribution guidelines.
License

SEING is licensed under the MIT License. See the LICENSE file for details.

Thank you for using SEING! If you have any questions or encounter issues, please feel free to open an issue on our GitHub repository or reach out to us for support. SEING is designed to provide a specialized and enhanced search experience for users seeking Egyptian web content. We hope it proves to be a valuable tool for your information retrieval needs.
