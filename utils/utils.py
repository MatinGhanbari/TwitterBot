import calendar
import re
import time
from random import Random
from faker import Faker
from colorama import Fore
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common import keys

fake = Faker()
random = Random(Random().random())


def findAllRegexMatches(regex, source):
    match_list = []
    while True:
        match = re.search(regex, source)
        if match:
            match_list.append(match.group(1))
            source = source[match.end():]
        else:
            return match_list


def stringToFloat(string):
    string = string.replace(",", "")
    if 'K' in string:
        return float(string.replace("K", "")) * 1000
    elif 'M' in string:
        return float(string.replace("M", "")) * 1000000
    return float(string)


def stringToInt(string):
    return round(stringToFloat(string))


def systemLog(message, cTime=None, saveToLog=False, printToConsole=True, color=Fore.WHITE):
    if cTime is None:
        cTime = time.strftime("%Y/%m/%d %H:%M:%S")
    out = f"# [{cTime}] Message: {message}"
    if printToConsole:
        print(color + out)
    if saveToLog:
        file = open('core/log', 'a+')
        print(out, file=file)


def takeABreath(minimum=0.1, maximum=2):
    rand = round(Random(random.random()).uniform(a=minimum, b=maximum), 2)
    systemLog(f"Bot will breath {rand} seconds!", printToConsole=False, saveToLog=False)
    time.sleep(rand)


def miniSleep():
    rand = round(random.random() * 0.1, 5)
    time.sleep(rand)


def sendKeys(element, content):
    for c in content:
        element.send_keys(c)
        takeABreath(minimum=0.08, maximum=0.27)


def fill(element, content, element_name: str = None) -> bool:
    try:
        if element_name is None:
            element_name = element.id
        if element is not None:
            element.clear()
            takeABreath(maximum=1)
            sendKeys(element, content)
            takeABreath(maximum=3)
            element.send_keys(keys.Keys.RETURN)
            systemLog(message=f"{element_name} FIELD! ✅", color=Fore.GREEN)
            takeABreath()
            return True
    except Exception as e:
        systemLog(message=f"{element_name} CAN'T FIELD!", color=Fore.RED)
    return False


def click(driver, element, element_name: str = None) -> bool:
    if element_name is None:
        element_name = element.id
    if element is not None:
        try:
            element.click()
            systemLog(message=f"{element_name} CLICKED! ✅", color=Fore.GREEN)
            takeABreath()
            return True
        except Exception as e:
            try:
                driver.execute_script("arguments[0].click();", element)
                systemLog(message=f"{element_name} CLICKED! ✅", color=Fore.GREEN)
                takeABreath()
                return True
            except Exception as e:
                systemLog(message=f"{element_name} CAN'T CLICKED!", color=Fore.RED)
                return False
    return False


def getLikeButtonXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[3]/div/div"
    return path


def getLikesCountXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[3]/div/div/div[2]/span/span/span"
    return path


def getCommentButtonXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[1]/div/div"
    return path


def getCommentCountXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[1]/div/div/div[2]/span/span/span"
    return path


def getCommentFieldXPath():
    path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[3]/div/div/div[2]/div/div/div/div/div[2]/div[' \
           '1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div'
    return path


def getSendCommentButtonXPath():
    path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div/div[3]/div/div'
    return path


def getShareButtonXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[4]/div/div"
    return path


def getShareDirectMessageButtonXPath():
    path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[1]'
    return path


def getShareBookmarkButtonXPath():
    path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[2]'
    return path


def getShareCopyLinkButtonXPath():
    path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[3]'
    return path


def getRetweetButtonXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[2]/div/div"
    return path


def getRetweetCountXPath(tweetArticle):
    ID = tweetArticle.split()[16]
    path = f"//*[@id=\"{ID}\"]/div[2]/div/div/div[2]/span/span/span"
    return path


def getRetweetRetweetButtonXPath():
    path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div'
    return path


def getRetweetQuoteButtonXPath():
    path = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/a'
    return path


def getRetweetQuoteTextFieldXPath():
    path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[3]/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div'
    return path


def getTweetTextXPath(tweetArticle):
    ID = tweetArticle.split()[10]
    path = f"//*[@id=\"{ID}\"]/span"
    return path


def getTweetTextXPath1(tweetArticle):
    ID = tweetArticle.split()[10]
    path = f"//*[@id=\"{ID}\"]/span[1]"
    return path


def getTweetTextXPath2(tweetArticle):
    ID = tweetArticle.split()[10]
    path = f"//*[@id=\"{ID}\"]/span[2]"
    return path


def getTweetSenderNameXPath(tweetArticle):
    ID = tweetArticle.split()[4]
    path = f"//*[@id=\"{ID}\"]/div[1]/div/a/div/div[1]/span/span"
    return path


def getTweetSenderUsernameXPath(tweetArticle):
    ID = tweetArticle.split()[4]
    path = f"//*[@id=\"{ID}\"]/div[2]/div/div/a/div/span"
    return path


def getTweetSendTimeXPath(tweetArticle):
    ID = tweetArticle.split()[4]
    path = f"//*[@id=\"{ID}\"]/div[2]/div/div[3]/a/time"
    return path


def saveScreenShot(driver, screenShotName=None) -> None:
    if screenShotName is None:
        screenShotName = f'screenshot {time.strftime("%Y-%m-%d %H-%M-%S")}'
    driver.save_screenshot(f"core/screenshots/{screenShotName}.png")


def generateNewName() -> str:
    return fake.name()


def generateNewPass() -> str:
    return fake.password()


def getRandomFavorites() -> str:
    favoriteList = ["Fashion & beauty", "Outdoors", "Arts & culture", "Animation & comics", "Business and finance",
                    "Food", "Travel", "Entertainment", "Music", "Gaming", "Careers", "Family & relationships",
                    "Fitness", "Sports", "Technology", "Science"]
    return favoriteList[random.randint(a=0, b=len(favoriteList))]


def generateMonth() -> str:
    return calendar.month_name[int(fake.month())]


def generateDay() -> str:
    return str(int(fake.day_of_month()))


def generateYear() -> str:
    return fake.year()

# fakes: ['_factories', '_factory_map', '_locales', '_map_provider_method', '_select_factory',
# '_select_factory_choice', '_select_factory_distribution', '_unique_proxy', '_weights', 'aba', 'add_provider',
# 'address', 'administrative_unit', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email',
# 'ascii_free_email', 'ascii_safe_email', 'bank_country', 'bban', 'binary', 'boolean', 'bothify', 'bs',
# 'building_number', 'cache_pattern', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix',
# 'color', 'color_name', 'company', 'company_email', 'company_suffix', 'coordinate', 'country',
# 'country_calling_code', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number',
# 'credit_card_provider', 'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_code',
# 'cryptocurrency_name', 'csv', 'currency', 'currency_code', 'currency_name', 'currency_symbol', 'current_country',
# 'current_country_code', 'date', 'date_between', 'date_between_dates', 'date_object', 'date_of_birth',
# 'date_this_century', 'date_this_decade', 'date_this_month', 'date_this_year', 'date_time', 'date_time_ad',
# 'date_time_between', 'date_time_between_dates', 'date_time_this_century', 'date_time_this_decade',
# 'date_time_this_month', 'date_time_this_year', 'day_of_month', 'day_of_week', 'del_arguments', 'dga',
# 'domain_name', 'domain_word', 'dsv', 'ean', 'ean13', 'ean8', 'ein', 'email', 'factories', 'file_extension',
# 'file_name', 'file_path', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'first_name_nonbinary',
# 'fixed_width', 'format', 'free_email', 'free_email_domain', 'future_date', 'future_datetime', 'generator_attrs',
# 'get_arguments', 'get_formatter', 'get_providers', 'hex_color', 'hexify', 'hostname', 'http_method', 'iana_id',
# 'iban', 'image', 'image_url', 'internet_explorer', 'invalid_ssn', 'ios_platform_token', 'ipv4',
# 'ipv4_network_class', 'ipv4_private', 'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'items', 'itin', 'job',
# 'json', 'language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male', 'last_name_nonbinary',
# 'latitude', 'latlng', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor', 'local_latlng',
# 'locale', 'locales', 'localized_ean', 'localized_ean13', 'localized_ean8', 'location_on_land', 'longitude',
# 'mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship',
# 'military_state', 'mime_type', 'month', 'month_name', 'msisdn', 'name', 'name_female', 'name_male',
# 'name_nonbinary', 'nic_handle', 'nic_handles', 'null_boolean', 'numerify', 'opera', 'paragraph', 'paragraphs',
# 'parse', 'password', 'past_date', 'past_datetime', 'phone_number', 'port_number', 'postalcode',
# 'postalcode_in_state', 'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female',
# 'prefix_male', 'prefix_nonbinary', 'pricetag', 'profile', 'provider', 'providers', 'psv', 'pybool', 'pydecimal',
# 'pydict', 'pyfloat', 'pyint', 'pyiterable', 'pylist', 'pyset', 'pystr', 'pystr_format', 'pystruct', 'pytimezone',
# 'pytuple', 'random', 'random_choices', 'random_digit', 'random_digit_not_null', 'random_digit_not_null_or_empty',
# 'random_digit_or_empty', 'random_element', 'random_elements', 'random_int', 'random_letter', 'random_letters',
# 'random_lowercase_letter', 'random_number', 'random_sample', 'random_uppercase_letter', 'randomize_nb_elements',
# 'rgb_color', 'rgb_css_color', 'ripe_id', 'safari', 'safe_color_name', 'safe_domain_name', 'safe_email',
# 'safe_hex_color', 'secondary_address', 'seed', 'seed_instance', 'seed_locale', 'sentence', 'sentences',
# 'set_arguments', 'set_formatter', 'sha1', 'sha256', 'simple_profile', 'slug', 'ssn', 'state', 'state_abbr',
# 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'suffix_nonbinary',
# 'swift', 'swift11', 'swift8', 'tar', 'text', 'texts', 'time', 'time_delta', 'time_object', 'time_series',
# 'timezone', 'tld', 'tsv', 'unique', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri',
# 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4', 'weights',
# 'windows_platform_token', 'word', 'words', 'year', 'zip', 'zipcode', 'zipcode_in_state', 'zipcode_plus4']
