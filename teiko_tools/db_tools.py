from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

USERNAME="leeleavitt"
PASSWORD="test"
HOST="localhost"
DATABASE="teiko_db"

def schema_standup(
        username: str, 
        password: str, 
        host: str = "localhost", 
        database: str = "teiko_db",
        schema_file: str = "schema.sql") -> None:
    """
    Creates the database schema for the Teiko database.
    
    Args:
        username (str): The username for the database.
        password (str): The password for the database.
        host (str): The host for the database. Defaults to "localhost".
        database (str): The name of the database. Defaults to "teiko_db".
        
    Returns:
        None
    """
    
    # Create the engine
    engine = create_engine(f'postgresql://{username}:{password}@{host}/{database}')

    # Read the schema from the .sql file
    
    with open(schema_file, 'r') as file:
            schema_sql = file.read()

    with engine.begin() as connection:
        statements = schema_sql.split(';')
        for statement in statements:
            print(statement)
            if statement.strip():
                try:
                    connection.execute(text(statement))
                except SQLAlchemyError as e:
                    print(f"An error occurred: {e}")
    print("Schema loaded successfully.")


def db_loader(file_name: str = "cell-count.csv"):
     
    cell_df = pd.read_csv(file_name)
    
    engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}')


    projects = cell_df[['project']]
    projects.columns = ['project_name']
    projects = projects.drop_duplicates()
    projects.to_sql('projects', engine, if_exists='append', schema = "research_data", index=False)
    
    treatments = cell_df[['treatment']].drop_duplicates()
    treatments.columns = ['treatment_name']
    treatments.to_sql('treatments', engine, if_exists='append', schema = "research_data", index=False)

    # load back to 
    projects = pd.read_sql_table('projects', engine, schema='research_data')
    treatments = pd.read_sql_table('treatments', engine, schema='research_data')

    # this add the uniueq ID's to the cell_df
    cell_df = cell_df.merge(projects, how='left', left_on='project', right_on='project_name')
    cell_df = cell_df.merge(treatments, how='left', left_on='treatment', right_on='treatment_name')

    # load the subjects
    subjects = cell_df[['project_id', 'subject', 'condition', 'age', 'sex']].drop_duplicates()
    subjects.columns = ['project_id', 'subject_name', 'condition', 'age', 'sex']  # Ensure column names match the SQL table
    subjects.to_sql('subjects', engine, schema='research_data', if_exists='append', index=False)
