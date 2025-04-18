import logging
from consumers.submission_consumer import start_submission_consumer

def main():
    print("ETL entry-point")
    start_submission_consumer()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
