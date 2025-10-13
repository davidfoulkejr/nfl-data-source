from get_each_week import main as get_each_week
from espn_data_processor import main as espn_data_processor
from csv_to_excel import main as csv_to_excel

def main():
    get_each_week()
    espn_data_processor()
    csv_to_excel()

if __name__ == "__main__":
    main()