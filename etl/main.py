from workers import url_worker, video_worker
from utils import kafka_mock_producer

def main():
    print("ETL entry-point")
    url_worker.main()
    # video_worker.main()
    # kafka_mock_producer.main()

if __name__ == "__main__":
    main()
