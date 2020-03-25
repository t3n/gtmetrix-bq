from datetime import datetime
from yaml import load, BaseLoader
from gtmetrix import GTmetrixInterface
from google.cloud import bigquery
from google.api_core.exceptions import NotFound


def bq_create_dataset(dataset):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset)

    try:
        bigquery_client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = bigquery_client.create_dataset(dataset)
        print('Dataset {} created.'.format(dataset.dataset_id))


def bq_create_table(dataset, table):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset)

    # Prepares a reference to the table
    table_ref = dataset_ref.table(table)

    try:
        bigquery_client.get_table(table_ref)
    except NotFound:
        schema = [
            bigquery.SchemaField('timestamp', 'DATETIME', mode='REQUIRED'),
            bigquery.SchemaField('url', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('adblock', 'BOOLEAN', mode='REQUIRED'),
            bigquery.SchemaField('onload_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('first_contentful_paint_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('page_elements', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('report_url', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('redirect_duration', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('first_paint_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('dom_content_loaded_duration', 'INTEGER'),
            bigquery.SchemaField('dom_content_loaded_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('dom_interactive_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('page_bytes', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('page_load_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('html_bytes', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('fully_loaded_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('html_load_time', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('rum_speed_index', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('yslow_score', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('pagespeed_score', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('backend_duration', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('onload_duration', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('connect_duration', 'INTEGER', mode='REQUIRED'),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        print('table {} created.'.format(table.table_id))


def bq_insert_rows(dataset, table, rows_to_insert):
    # Instantiates a client
    bigquery_client = bigquery.Client()

    # Prepares a reference to the dataset
    dataset_ref = bigquery_client.dataset(dataset)

    table_ref = dataset_ref.table(table)
    table = bigquery_client.get_table(table_ref)  # API call

    errors = bigquery_client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []


if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        config = load(stream, BaseLoader)

    dataset_id = config['bq']['dataset']
    table_id = config['bq']['table']
    bq_create_dataset(dataset_id)
    bq_create_table(dataset_id, table_id)
    gt = GTmetrixInterface()

    for url in config['urls']:
        for options in [{}, {'x-metrix-adblock': 1}]:
            test = gt.start_test(url, **options)
            results = test.fetch_results('results')['results']
            results['url'] = url
            results['timestamp'] = datetime.utcnow()

            if not bool(options):
                results['adblock'] = False
            else:
                results['adblock'] = True

            for k, v in results.items():
                if v is None:
                    results[k] = 0

            bq_insert_rows(dataset_id, table_id, [results])
