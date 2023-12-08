import os
import requests
import pandas as pd

class CyclingDataDownloader:
    def __init__(self, base_url, base_directory, file_list_path):
        self.base_url = base_url
        self.base_directory = base_directory
        self.file_list_path = file_list_path

    def download_file(self, url, folder, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), 'wb') as f:
                f.write(response.content)

    def download_files(self):
        with open(self.file_list_path, 'r') as file:
            filenames = [line.strip() for line in file]

        for filename in filenames:
            year = filename[-8:-4]

            # Create directory for the year
            year_dir = os.path.join(self.base_directory, year)
            os.makedirs(year_dir, exist_ok=True)

            file_url = self.base_url + filename
            print(f"Downloading {filename}...")
            self.download_file(file_url, year_dir, filename)

    def combine_csv_files(self):
        year_dirs = [dir for dir in os.listdir(self.base_directory)
                     if os.path.isdir(os.path.join(self.base_directory, dir))]

        for year_dir in year_dirs:
            combined_df = pd.DataFrame()
            current_dir = os.path.join(self.base_directory, year_dir)

            for file in os.listdir(current_dir):
                if file.endswith('.csv'):
                    file_path = os.path.join(current_dir, file)
                    df = pd.read_csv(file_path)
                    combined_df = pd.concat([combined_df, df])

            combined_df.to_csv(os.path.join(current_dir, f'all_data_{year_dir}.csv'), index=False)

# Usage
base_url = "https://cycling.data.tfl.gov.uk/usage-stats/"
base_directory = "/cycling_analysis/data_scraping"
file_list_path = '/files.txt'

downloader = CyclingDataDownloader(base_url, base_directory, file_list_path)
downloader.download_files()
downloader.combine_csv_files()
