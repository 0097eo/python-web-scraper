# BookScraper

A web scraper built with Python and Scrapy to extract details about books.

## Features

- Scrapes book titles, titles, prices, and descriptions.
- Export data to CSV, JSON, or other formats
- Respects robots.txt and implements polite crawling behavior

## Requirements

- Python 3.7+
- Scrapy 2.5+

## Installation

1. Clone this repository:
   ```
   git clone
   
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   
   ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   
   ```

## Usage

1. Configure your search parameters in `bookscraper.py`:
```
# Example configuration
keywords = "sci-fi"
price = "$ 45"
```

2. Run the spider
```
scrapy crawl bookscraper -o data.csv

```
3. Find your scraped data in data.csv (or the filename you specified).

## Customization

Modify bookspider.py to adjust the scraping logic or extract additional fields.
Edit settings.py to change Scrapy settings like user agent, download delay, etc.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License 
