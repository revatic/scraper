# Zaubacorp Scraper

This is a Python web scraper designed to extract company information from the Zaubacorp website and store it in a MongoDB database.

## Requirements

Before running the scraper, make sure you have the following installed:

- Python 3.8
install required libraries from requiremnt.txt
  
  ```pip install -r requirements.txt```
## Usage

1. Clone the repository to your local machine.
2. Install the required libraries as mentioned above.
3. Open a terminal or command prompt and navigate to the project directory.
4. Run the `scraper.py` script using the following command:


The scraper will start fetching data from the Zaubacorp website, and the progress will be logged in the `scraper.log` file.

## Configuration

- The base URL for scraping is set as `BASE_URL = "https://www.zaubacorp.com/company-list-company.html"`.
- The MongoDB connection URI is set as `MONGO_URI = "mongodb://localhost:27017/"`. Make sure MongoDB is running on your system.
- The database name and collection name can be modified using `DATABASE_NAME` and `COLLECTION_NAME` variables in the `scraper.py` file.

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, feel free to create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

