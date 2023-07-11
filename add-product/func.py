#
# oci-serverless-demo-python version 1.0.
# This function connects to the ATP database and performs the basic operations
# like Fetch/Create/Update/Delete for the products table

import os
import json
import requests
from parliament import Context
from urllib.parse import urlparse, parse_qs

os.environ['OCI_RESOURCE_PRINCIPAL_VERSION'] = "2.2"
ORDS_BASE_URL = os.getenv("ORDS_BASE_URL")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def ords_run_sql(ordsbaseurl, dbschema, dbpwd, sqlQuery):
    dbsqlurl = ordsbaseurl + dbschema + '/_/sql'
    headers = {"Content-Type": "application/sql"}
    auth=(dbschema, dbpwd)
    r = requests.post(dbsqlurl, auth=auth, headers=headers, data=sqlQuery)
    result = {}
    print("status code:", r.status_code, flush=True)
    r_json = json.loads(r.text)
    print("sql REST call response", r_json, flush=True)
#    if r.status_code == 200:
    try:
        for item in r_json["items"]:
            result["sql_statement"] = item["statementText"]
            if "errorDetails" in item:
                result["error"] = item["errorDetails"]
            elif "resultSet" in item:
                result["results"] = item["resultSet"]["items"]
            elif "response" in item:
                result["response"] = item["response"]
    except ValueError:
        print(r.text, flush=True)
        raise
#    else:
#        result["error"] = "Error while invoking the SQL Rest endpoint"
    return result

# get the sql query based on the operation extracted from the request URL parameters
def get_sql_query(queryString, dbUser):
    tableName = dbUser + ".products"
    product_name = queryString['name'][0]
    product_count = int(queryString['count'][0])
    sqlQuery = "insert into "+ tableName + " values ('" + product_name +"' , "+ str(product_count) + ")"
    return sqlQuery

def main(context: Context):
    request_url = context.request.full_path
    request_url_string = json.dumps(request_url)
    print(request_url_string)
    parsed_url = urlparse(request_url)
    query_string = parse_qs(parsed_url.query)

    ords_base_url = "https://gefe254a28f61fa-products.adb.us-ashburn-1.oraclecloudapps.com/ords/" # ORDS_BASE_URL

    # Read the db credential secrets from the OCI
    dbuser = "test_user" # DB_USER
    dbpwd = "Hamonica2023" # DB_PASSWORD
    sql_query_string = get_sql_query(query_string, dbuser)

    result = ords_run_sql(ords_base_url, dbuser, dbpwd, sql_query_string)

    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    return json.dumps(result), 200, headers
