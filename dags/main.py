
import requests
from bs4 import BeautifulSoup
import psycopg2
import datetime
import configparser
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook

# DAG definition
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'catchup' : False
}

# Functions
def get_soup(base_url, headers):
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def get_category_urls(url, headers):
    soup = get_soup(url, headers)
    category_ul = soup.find("ul", {"class": "mobile-step-1"})
    return [a_tag.get('href') for a_tag in category_ul.find_all('a', href=True) if a_tag['href'].startswith('http')]

def get_products(url, headers):
    soup = get_soup(url, headers)
    category_name = soup.find("h1", class_="modtitle").get_text(strip=True)
    products = soup.find_all("div", {"class": "right-block"})
    return [{"Category": category_name, "Title": product.find("div", {"class": "t-baslikk"}).find("a").get_text(strip=True),
             "Price": product.find("div", {"class": "price"}).get_text(strip=True),
             "Supplier": product.find("div", {"class": "price"}).find_next_sibling("span").find("a").get_text(strip=True)}
            for product in products]

def insert_data_to_db(data, postgres_conn_id='postgres_conn'):
    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    print(hook.get_uri())
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    for product in data:
        cursor.execute("""
            INSERT INTO plant.products (category, title, price, supplier) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title, supplier) 
            DO UPDATE SET 
                category = EXCLUDED.category,
                price = EXCLUDED.price;
            """, (product['Category'], product['Title'], product['Price'], product['Supplier']))
    conn.commit()
    cursor.close()
    conn.close()

dag = DAG('my_scraping_dag', default_args=default_args, schedule_interval=None)

def main(**kwargs):
    """Main function to orchestrate tasks."""
    base_url = Variable.get('base_url')
    headers = {
        'User-Agent': Variable.get('user_agent'),
        'Accept-Language': Variable.get('accept_language'),
    }
    category_urls = get_category_urls(base_url, headers)
    all_products = []
    for category_url in category_urls:
        page = 1
        while True:
            full_url = f"{category_url}?pg={page}&s=1&o=0&ps=12"
            print(full_url) 
            products = get_products(full_url, headers)
            if not products:
                break  
            all_products.extend(products)
            page += 1

main_task = PythonOperator(
    task_id='main_task',
    python_callable=main,
    provide_context=True,
    dag=dag,
)

main_task