import os

import pandas as pd
import threading
from threading import Thread
from django.core.management.base import BaseCommand
from base.models import Company
from sqlalchemy import create_engine
from django.conf import settings

# load environment variables
from dotenv import load_dotenv
path_to_env_file = './.env'
load_dotenv(path_to_env_file)

class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def run_in_thread(self, chunk, engine):
        chunk = chunk[chunk['name'].notnull()].iloc[:, 1:]
        chunk.to_sql(Company._meta.db_table, con=engine, if_exists='append', index=False)

    def handle(self, *args, **options):
        try:
            user = os.getenv('DBUSER')
            password = os.getenv('DBPASSWORD')
            database_name = os.getenv('DBNAME')
            database_url = f'postgresql://{user}:{password}@localhost:5432/{database_name}'
            engine = create_engine(database_url, echo=False)

            filename = options['filename']
            column_names = ["id", "name", "domain", "foundationYear", "industry", "companySize", "locality", "country", "linkedin", "currentEmployeeCount", "totalEmployeeCount"]
            df_chunks = pd.read_csv(filename, chunksize=5000, header=None, names=column_names)

            counter = 0
            for chunk in df_chunks:
                counter += 1
                print(counter)
                chunk['locality'].fillna('', inplace=True)

                split_names = chunk['locality'].str.split(',', expand=True)

                chunk['city'] = split_names[0]
                chunk['state'] = split_names[1]

                # Drop the original column
                chunk.drop('locality', axis=1, inplace=True)

                chunk = chunk.reindex(columns=["id", "name", "domain", "foundationYear", "industry", "companySize", "city", "state", "country", "linkedin", "currentEmployeeCount", "totalEmployeeCount"])
                chunk = chunk.iloc[1:]

                thread_pool = threading.Thread(target=self.run_in_thread, args=(chunk, engine))
                thread_pool.start()
                thread_pool.join()

            self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        except Exception as e:
            print(e)