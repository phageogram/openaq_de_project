from google.cloud import bigquery

def define_schema(table_id):
    if table_id == "countries":
        return [
            bigquery.SchemaField("id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("datetime_first", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("datetime_last", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("param_id", "INT64", mode="REQUIRED"),
            bigquery.SchemaField("param_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("units", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("display_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("pk", "STRING", mode="REQUIRED")
        ]
    else:
        raise ValueError(f"No schema defined for table: {table_id}")