from dotenv import dotenv_values
import sqlalchemy 
import pandas as pd 
import psycopg2

#Future Setup: 
#sql_config = get_sql_config() 
#schema = 'cgn_analytics_24_1'
#engine = get_engine()
#sql_query = f'select * from {schema}.flights limit 5;'

# get the configuration key value pairs 
def get_sql_config():
    ''' Function loads credentials from .env file and returns a dictionary containing the data needed for sqlalchemy.create_engine() '''
    needed_keys = ['host', 'port', 'database','user','password']
    dotenv_dict = dotenv_values(".env")
    sql_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}

    return sql_config 


def get_api():
    config = dotenv_values(".env") 
    weather_api = config.get("weather_api") 
    meteostat_api = config.get("meteostat_api")

    if weather_api is None:
        raise ValueError("weather_api not found in the .env file")
    
    if meteostat_api is None:
        raise ValueError("meteostat_api not found in the .env file")
    
    return meteostat_api, weather_api 


def get_engine():
    sql_config = get_sql_config() 
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=sql_config) # use dictionary with config details)
    return engine  


def get_data(sql_query):
    '''Connect to the PostgreSQL database server, run query, and return data'''
    sql_config = get_sql_config() # Get the connection configuration dictionary using the get_sql_config function
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database', # Create a connection engine to the PostgreSQL server
                        connect_args=sql_config) # use dictionary with config details
    with engine.begin() as conn: # Open a connection session using 'with', execute the query, and return the results
        results = conn.execute(sql_query) 
        return results.fetchall() 
    

# def get_dataframe(sql_query):
#     ''' Connect to the PostgreSQL database server, run query, and return data as a pandas dataframe '''
#     sql_config = get_sql_config()  # Get the connection configuration dictionary using the get_sql_config function
#     engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',   # Create a connection engine to the PostgreSQL server
#                                       connect_args=sql_config) # use dictionary with config details
#     return  pd.read_sql_query(sql=sql_query, con=engine) # Use pandas read_sql_query to execute the query and return the results as a dataframe 


def get_dataframe(sql_query):
    sql_config = get_sql_config()  # Assuming get_sql_config() returns a dictionary with connection details
    # Constructing the database URL 
    db_url = f"postgresql://{sql_config['user']}:{sql_config['password']}@{sql_config['host']}:{sql_config['port']}/{sql_config['database']}"
    engine = sqlalchemy.create_engine(db_url)
    return pd.read_sql_query(sql=sql_query, con=engine)


def push_to_sql(df, table_name, engine=None, schema=None): 
    if engine!=None:
        try:
            df.to_sql(name=table_name,
                      con=engine,
                      if_exists='replace',
                      schema=schema,
                      index=False,
                      chunksize=5000,
                      method='multi')
            return f"The {table_name} table was imported successfully."  # Return a status message
        except (Exception, psycopg2.DatabaseError) as error:
            return f"An error occurred: {error}"  # Return an error message
    else:
        return "No engine provided."

