
# Data Extraction and Storage DAG

This project includes an Apache Airflow DAG (Directed Acyclic Graph) that extracts daily data from the Tunç Botanik website and stores it in a PostgreSQL database.

## Features

- Daily Data Extraction**: Retrieves daily data from the Tunç Botanik website.
- PostgreSQL Integration**: Stores the extracted data in a PostgreSQL database.
- Automation with Airflow**: The DAG structure automates the data extraction process.

## Requirements

- Python 3
- PostgreSQL
- Apache Airflow
- Python packages: requests, BeautifulSoup, psycopg2

## Installation

1. Configure your PostgreSQL database.
2. Place the `main.py` file in your Airflow DAG folder.
3. Install the required Python packages:
   ```bash
   pip install requests beautifulsoup4 psycopg2
   ```
4. Start Airflow and enable the DAG.

## Usage

Once activated through the Airflow interface, the DAG will automatically run daily. The data will be stored in the designated PostgreSQL database.

## Contributing

If you wish to contribute to the project, please submit pull requests or report issues.

<img width="1505" alt="image" src="https://github.com/aozgokmen/plant/assets/74674469/13803f40-962a-4773-8cc0-92cc43d94c34">

