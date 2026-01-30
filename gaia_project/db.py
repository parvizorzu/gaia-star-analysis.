import duckdb

def execute_query(query_path):
    con = duckdb.connect('gaia_project/my.db', read_only=True)
    
    with open(query_path, 'r') as f:
        sql_script = f.read()
    
    df = con.execute(sql_script).df()
    con.close()
    return df
