from google.cloud import bigquery

def bq_magic (project_name, query):
  client = bigquery.Client(project=project_name)
  df = client.query(f'''{query}''').to_dataframe()
  df_to_csv = df.to_csv('df.csv')
  df_reread = pd.read_csv('df.csv')
  return df_reread