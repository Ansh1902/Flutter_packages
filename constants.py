import os

PUB_DEV_WEBSITE = "https://pub.dev/packages?sort=like"

PACKAGE_TITLE_XPATH = '//div[@class="packages-header"]//h3[@class="packages-title"]/a'
PACKAGE_LIKES_XPATH = "//div[@class='packages-score packages-score-like']"
PACKAGE_PUB_POINTS_XPATH = "//div[@class='packages-score packages-score-health']"
PACKAGE_POPULARITIY_XPATH = "//div[@class='packages-score packages-score-popularity']"
PACKAGE_PUBLISHER_XPATH = "//aside/p[1]"
PACKAGE_DESCRIPTION_XPATH = "//div[@class='packages-description']/span"
PACKAGE_VERSION_XPATH = "//span[@class='packages-metadata-block'][1]/a[1]"
PACKAGE_VERSION_RELEASE_DATE_XPATH = "//p[@class='packages-metadata']//span[@class='packages-metadata-block'][1]//a[@class='-x-ago'][1]"
PACKAGE_PUBLISHER_SITE_XPATH = "//p[@class='packages-metadata']/span[2]/a"
PACKAGE_PROVIDED_LICENSE_XPATH = "//span[img[contains(@class, 'inline-icon-img')]]"
PACKAGE_SDK_XPATH = "//div[@class='-pub-tag-badge'][1]/a"
PACKAGE_PRE_RELEASE_XPATH = "//div[@class='detail-header-content-block']//div[@class='metadata']//span[contains(text(),'Prerelease:')]//a[1]"
PACKAGE_PLATFORM_XPATH = "//div[@class='-pub-tag-badge'][2]/a"
PACKAGE_DOCUMENTATION_LINK_XPATH = "//aside//h3[@class = 'title' and text() = 'Documentation']/following-sibling::p[1]//a"

PACKAGE_DEPENDENCIES_XPATH = "//aside//h3[@class='title' and text()='Dependencies']/following-sibling::p[1]//a"
PACKAGE_GITHUB_XPATH = "//aside//h3[@class='title pkg-infobox-metadata']/following-sibling::p[2]//a[contains(text(),'Repository')]"
NEXT_BUTTON_XPATH = '//a[@rel="next nofollow"]'
EXAMPLE_BUTTON_XPATH = "//ul[@class='detail-tabs-header']/li[3]"
DETAIL_TITLE_XPATH = "//h1[@class='title']"

WAIT_TIME = 3
LIKES_COUNT = 20
BASIC_CSV_FILE = "basic.csv"
BASIC_PROGRESS_FILE = "basic_progress.csv"
DETAILED_CSV_FILE = "detailed.csv"
ERROR_FILE = "error.csv"
SCRIPT_LOCATION = os.path.dirname(os.path.abspath(__file__))
DATA_LOCATION = SCRIPT_LOCATION + "/output"
os.makedirs(DATA_LOCATION, exist_ok=True)

CHROME_PATH = r'C:\Users\ANSH\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
CHROME_BINARY_LOCATION = r"c:\Program Files\Google\Chrome Beta\Application\chrome.exe"
OPTION_ARGUMENT_ONE = "--ignore-certificate-errors"
OPTION_ARGUMENT_TWO = "--ignore-ssl-errors"
OPTION_EXCLUDE = "excludeSwitches"
OPTION_LOGGING = "enable-logging"
