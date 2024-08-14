from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import fire
from selenium.webdriver.chrome.service import Service
import constants
import csv
import re
import os
import time


class MainExecuter:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_experimental_option(
            constants.OPTION_EXCLUDE, [constants.OPTION_LOGGING]
        )
        options.binary_location = constants.CHROME_BINARY_LOCATION
        chrome_options= Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
        service=Service(constants.CHROME_PATH),
        options=chrome_options
)
        self.driver.maximize_window()
        self.driver.get(constants.PUB_DEV_WEBSITE)
        # self.final_dict = defaultdict(list)
        self.result_dict = defaultdict(list)

    def get_item_from_xpath(self, xpath):
        item = self.driver.find_element(by=By.XPATH, value=xpath)
        return item

    def get_elements_from_xpath(self, xpath):
        item = self.driver.find_elements(by=By.XPATH, value=xpath)
        return item
    
    def get_elements_or_null(self,xpath):
        try:
            elements = self.get_elements_from_xpath(xpath)
            if elements:
                return elements
            else:
                return "NULL"
        except:
            return "NULL"

    def get_text(self, xpath):
        items = self.get_elements_from_xpath(xpath)
        return ",".join(element.text for element in items)

    def get_digit(self, word):
        item = (
            word.replace("\nLIKES", " ")
            .replace(" ", "")
            .replace("\nPUBPOINTS", " ")
            .replace("\nPOPULARITY", " ")
        )
        return item
    
    def update_progress(self, processed_urls, file_name):
        df = pd.DataFrame(processed_urls, columns=["url"])
        df.to_csv(file_name, index=False)

    def load_progress(self, file_name):
        if os.path.isfile(file_name):
            df = pd.read_csv(file_name)
            return set(df["url"].to_list())
        return set()
    
    def reset_progress(self, file_path):
        """Reset the progress file by deleting it."""
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Progress file {file_path} has been reset.")
        else:
            print(f"Progress file {file_path} does not exist to reset.")

    def get_basic_info(self, force_download):
        print("getting package details")
        min_likes = True
        processed_urls = self.load_progress(constants.BASIC_PROGRESS_FILE)

        # Load existing data from basic.csv if it exists and not forcing download
        if os.path.isfile(os.path.join(constants.DATA_LOCATION, constants.BASIC_CSV_FILE)) and not force_download:
            existing_df = pd.read_csv(os.path.join(constants.DATA_LOCATION, constants.BASIC_CSV_FILE))
            self.final_dict = {
                "title": existing_df["title"].tolist(),
                "title_link": existing_df["title_link"].tolist(),
                "likes": existing_df["likes"].tolist(),
                "pub_points": existing_df["pub_points"].tolist(),
                "popularity": existing_df["popularity"].tolist(),
                "description": existing_df["description"].tolist(),
                "latest_version": existing_df["latest_version"].tolist(),
                "latest_version_release_date": existing_df["latest_version_release_date"].tolist(),
                "provided_license": existing_df["provided_license"].tolist()
                
            }
            
            # Calculate the number of pages to skip
            num_rows = len(existing_df)
            num_pages = (num_rows // 10) + 1  # Assuming each page has 10 packages
            self.current_page = num_pages
        else:
            self.final_dict = defaultdict(list)
            self.current_page = 1

        while min_likes:
            print(f"Finding package - Page {self.current_page}")
            time.sleep(constants.WAIT_TIME)
            
            # Navigate to the page
            if self.current_page > 1:
                try:
                    page_url = f"{constants.PUB_DEV_WEBSITE}&page={self.current_page}"
                    self.driver.get(page_url)
                except Exception as e:
                    print(f"Failed to navigate to page {self.current_page}: {e}")
                    break

            package_title = self.get_elements_or_null(constants.PACKAGE_TITLE_XPATH)
            package_likes = self.get_elements_or_null(constants.PACKAGE_LIKES_XPATH)
            package_pub_points = self.get_elements_or_null(constants.PACKAGE_PUB_POINTS_XPATH)
            package_popularitys = self.get_elements_or_null(constants.PACKAGE_POPULARITIY_XPATH)
            package_description = self.get_elements_or_null(constants.PACKAGE_DESCRIPTION_XPATH)
            package_version = self.get_elements_or_null(constants.PACKAGE_VERSION_XPATH)
            package_version_release_date = self.get_elements_or_null(constants.PACKAGE_VERSION_RELEASE_DATE_XPATH)
            package_organisation = self.get_elements_from_xpath(constants.PACKAGE_PROVIDED_LICENSE_XPATH)
            

            first_url = package_title[0].get_attribute("href")
            if first_url in processed_urls:
                print(f"Skipping page (first URL already processed): {first_url}")
                try:
                    button = self.get_item_from_xpath(constants.NEXT_BUTTON_XPATH)
                    self.driver.get(button.get_attribute("href"))
                    self.current_page += 1
                    continue
                except Exception as e:
                    print(f"Failed to navigate to next page: {e}")
                    break

            for j in range(len(package_likes)):
                url = package_title[j].get_attribute("href")
                if url in processed_urls:
                    continue
                if not int(self.get_digit(package_likes[j].text)) > constants.LIKES_COUNT:
                    min_likes = False
                    break
                time.sleep(constants.WAIT_TIME)
                self.final_dict["title"] += [i.get_attribute("textContent") if i!="NULL" else "NULL" for i in package_title]
                self.final_dict["title_link"] += [i.get_attribute("href") for i in package_title]
                self.final_dict["likes"] += [self.get_digit(i.text) for i in package_likes]
                self.final_dict["pub_points"] += [self.get_digit(i.text) for i in package_pub_points]
                self.final_dict["popularity"] += [self.get_digit(i.text) for i in package_popularitys]
                self.final_dict["description"] += [i.text for i in package_description]
                self.final_dict["latest_version"] += [i.get_attribute("textContent") for i in package_version]
                self.final_dict["latest_version_release_date"] += [i.get_attribute("title") for i in package_version_release_date]
                self.final_dict["provided_license"] += [i.text for i in package_organisation]
               
                    
                processed_urls.add(url)
                self.update_progress(processed_urls, constants.BASIC_PROGRESS_FILE)
                df = pd.DataFrame.from_dict(self.final_dict, orient="index")
                df = df.transpose()
                df.fillna("", inplace=True)
                df.to_csv(os.path.join(constants.DATA_LOCATION + "/" + constants.BASIC_CSV_FILE), index=False)
                break

            if not min_likes:
                break
            else:
                button = self.get_item_from_xpath(constants.NEXT_BUTTON_XPATH)
                self.driver.get(button.get_attribute("href"))
                self.current_page += 1

        print("basic.csv has been downloaded and saved in output folder.")


    def get_detailed_info(self, force_download):
        # Load basic information
        df_package = pd.read_csv(os.path.join(constants.DATA_LOCATION, constants.BASIC_CSV_FILE))
        df_url = df_package["title_link"].tolist()
        df_title = df_package["title"].tolist()

        # Load existing detailed data if it exists
        detailed_csv_path = os.path.join(constants.DATA_LOCATION, constants.DETAILED_CSV_FILE)
        if os.path.isfile(detailed_csv_path):
            df_package_detail = pd.read_csv(detailed_csv_path)
            existing_urls = set(df_package_detail["title_link"].tolist())
        else:
            df_package_detail = pd.DataFrame(columns=["title_link", "title", "is_beta_version", "sdk", "platform", "documentation_link", "verified_publisher", "dependencies", "github_link"])
            existing_urls = set()

        # Initialize result_dict for new scraping
        self.result_dict = {
            "title_link": [],
            "title": [],
            "is_beta_version":[],
            "sdk": [],
            "platform": [],
            "documentation_link":[],
            "verified_publisher":[],
            "dependencies": [],
            "github_link": [],
        }

        # Start scraping
        for i in tqdm(range(len(df_url)), "Scraping Detailed Packages: "):
            try:
                url = df_url[i]
                if url in existing_urls:
                    print(f"Skipping already processed URL: {url}")
                    continue  # Skip URLs already processed

                print(f"Scraping {url}")
                self.driver.get(url)
                time.sleep(constants.WAIT_TIME)
                
                # Extract detailed information
                package_title = self.get_elements_from_xpath(constants.DETAIL_TITLE_XPATH)
                try:
                    package_prerelease_version=self.get_item_from_xpath(constants.PACKAGE_PRE_RELEASE_XPATH)
                except:
                    package_prerelease_version = "NULL"
                

                package_sdk = self.get_elements_from_xpath(constants.PACKAGE_SDK_XPATH)
                package_platform = self.get_elements_from_xpath(constants.PACKAGE_PLATFORM_XPATH)
                package_api_reference = self.get_elements_from_xpath(constants.PACKAGE_DOCUMENTATION_LINK_XPATH)
                package_dependencies = self.get_elements_from_xpath(constants.PACKAGE_DEPENDENCIES_XPATH)
                package_publisher = self.get_elements_or_null(constants.PACKAGE_PUBLISHER_XPATH)
                package_github_link = self.get_elements_from_xpath(constants.PACKAGE_GITHUB_XPATH)
                self.result_dict["title_link"].append(url)
                self.result_dict["title"] += [package_title[0].text if package_title else ""]
                self.result_dict["is_beta_version"] += [package_prerelease_version.text if package_prerelease_version is not "NULL" else "NULL"]
                self.result_dict["sdk"] += [", ".join(i.text for i in package_sdk)]
                self.result_dict["platform"] += [", ".join(i.text for i in package_platform)]
                self.result_dict["verified_publisher"] += [i.text for i in package_publisher]
                self.result_dict["dependencies"] += [",".join(i.text for i in package_dependencies)]
                self.result_dict["github_link"] += [i.get_attribute("href") if package_github_link else "NULL" for i in package_github_link]
                
                self.result_dict["documentation_link"] += [",".join(i.get_attribute("href") for i in package_api_reference)]
                # Save results to detailed.csv
                max_len = max(len(lst) for lst in self.result_dict.values())
                for key in self.result_dict:
                # Extend lists to the maximum length with empty strings
                    self.result_dict[key] += ["" for _ in range(max_len - len(self.result_dict[key]))]
                df_new = pd.DataFrame.from_dict(self.result_dict)
                df_new.fillna("", inplace=True)
                
                # Append new data to the existing DataFrame
                df_package_detail = pd.concat([df_package_detail, df_new]).drop_duplicates(subset=["package_url"], keep="last")
                
                # Save updated data incrementally
                df_package_detail.to_csv(detailed_csv_path, index=False)
            except Exception as e:
                
            # Log the URL and error to error.csv
                with open(constants.ERROR_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([url])
                print(f"Error processing URL {url}: {e}")
                continue
        self.driver.close()
        print("detailed.csv has been downloaded and saved in the output folder.")


    def scrap_packages(self, force_download=False):
        self.get_basic_info(force_download)
        self.get_detailed_info(force_download)


if __name__ == "__main__":
    fire.Fire(MainExecuter)
    
