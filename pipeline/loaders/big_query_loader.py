from google.cloud import bigquery

class BigQueryLoader:
    """Loads transformed data into BigQuery"""
    def __init__(self, project_id, dataset_id, table_id):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    def load_data(self, df, schema):
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            schema=schema)
        job = self.client.load_table_from_dataframe(df, self.table_ref, job_config)

        job.result()
        print(f"Data successfully load to {self.table_ref}")