def get_parkdat(SELECTED_PARK):
	# pip install psycopg2-binary
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import pandas as pd
    username = 'masteruser'
    password = 'yosemite'
    host = 'insightinstance.ce8p69rfxkwn.us-east-2.rds.amazonaws.com'
    port = 5432
    db_name = 'nps_database'

    engine = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, 
                                                            password, 
                                                            host, 
                                                            port, 
                                                            db_name))
    if not database_exists(engine.url):
        create_database(engine.url)
    
    con = None
    con = psycopg2.connect(database = db_name, user = username, host=host, password=password)
    
    all_query = """
    SELECT * FROM np_data_table;
    """
    park_query = 'SELECT * FROM np_data_table WHERE "ParkName"'+"='"+SELECTED_PARK+"';"
    
    NP_SUBSET = pd.read_sql_query(park_query,con)
    
    return NP_SUBSET