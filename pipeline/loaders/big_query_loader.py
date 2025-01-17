from google.cloud import bigquery
import pandas as pd

class BigQueryLoader:
    """Loads transformed data into BigQuery"""
    def __init__(self, project_id, dataset_id, table_id):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    def load_data(self, data, schema):
        # Check if data is a DataFrame
        if isinstance(data, pd.DataFrame):
            # Load directly from DataFrame
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                schema=schema
            )
            job = self.client.load_table_from_dataframe(data, self.table_ref, job_config=job_config)
            job.result()
            print(f"Data successfully loaded into {self.table_ref}")

        else:
            # Fallback to JSON (original behavior)
            temp_table_ref = f"{self.table_ref}_staging"

            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                schema=schema
            )
            job = self.client.load_table_from_json(data, temp_table_ref, job_config)
            job.result()

            print(f"Data successfully staged at {temp_table_ref}")

            # Merge temp with BigQuery table
            merge_query = f"""
            MERGE `{self.table_ref}` t
            USING `{temp_table_ref}` s
            ON t.pk = s.pk
            WHEN MATCHED THEN
                UPDATE SET
                    t.id = s.id,
                    t.code = s.code,
                    t.name = s.name,
                    t.datetime_first = s.datetime_first,
                    t.datetime_last = s.datetime_last,
                    t.param_id = s.param_id,
                    t.param_name = s.param_name,
                    t.units = s.units,
                    t.display_name = s.display_name
            WHEN NOT MATCHED THEN
                INSERT (id, code, name, datetime_first, datetime_last, param_id, param_name, units, display_name)
                VALUES (s.id, s.code, s.name, s.datetime_first, s.datetime_last, s.param_id, s.param_name, s.units, s.display_name)
            """
            query_job = self.client.query(merge_query)
            query_job.result()

            # Clean up temp table
            self.client.delete_table(temp_table_ref, not_found_ok=True)