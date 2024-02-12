import pandas as pd
import threading
from threading import Thread
from django.core.management.base import BaseCommand
from base.models import Company
from sqlalchemy import create_engine
from django.conf import settings


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def run_in_thread(self, chunk):
        engine = create_engine('sqlite:///db.sqlite3')
        chunk = chunk[chunk['name'].notnull()].iloc[:, 1:]
        chunk.to_sql(Company._meta.db_table, con=engine, if_exists='append', index=False)

    def handle(self, *args, **options):
        try:
            filename = options['filename']
            column_names = ["id", "name", "domain", "foundationYear", "industry", "companySize", "locality", "country", "linkedin", "currentEmployeeCount", "totalEmployeeCount"]
            df_chunks = pd.read_csv(filename, chunksize=1000, header=None, names=column_names)

            counter = 0
            for chunk in df_chunks:
                counter += 1
                print(counter)
                thread_pool = threading.Thread(target=self.run_in_thread, args=(chunk, ))
                thread_pool.start()
                thread_pool.join()

            self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        except Exception as e:
            print(e)