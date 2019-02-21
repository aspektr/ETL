from source import Source
from sink import Sink
from producer import Producer
from injector import Injector
import argparse
from parallel_ingesting import run_in_parallel

parser = argparse.ArgumentParser(description='<= Simple data transfer => ')
parser.add_argument('--version', action='version', version='%(ETL)s 0.1')
parser.add_argument('--from', metavar='FROM', required=True, dest='from_source',
                      help='source name from config file')
parser.add_argument('--to', metavar='TO', required=True, dest='to_sink',
                    help='sink name from config file')

if __name__ == '__main__':

    # batch data from command promt
    # args = parser.parse_args()
    # payload = Source(args.from_source).pull_data()
    # Sink(args.to_sink).push_data(payload)

    # batch data loading with pandas
    #payload = Source('test_source2').pull_data()
    #Sink('temp_table').push_data(payload)

    # row by row loading with info about speed
    #producer = Producer('test_source2')
    #injector = Injector('temp_table')
    #injector.ingest_from(producer)

    # run in parallel
    producer = Producer('test_source2')
    run_in_parallel(producer)

