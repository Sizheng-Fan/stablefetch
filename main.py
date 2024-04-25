import json
from selenium.webdriver.chrome.options import Options
import schedule
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import time


def init_driver():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def read_last_record(site):
    try:
        with open(f'{site}_last_link.txt', 'r') as file:
            last_link = file.read().strip()
            return last_link
    except FileNotFoundError:
        return None


def save_data(site, data, last_link):

    directory = os.path.dirname(site)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f'{site}_data.txt'

    with open(filename, 'a+', encoding='utf-8') as file:
        data_strings = [json.dumps(item, ensure_ascii=False) for item in data]  # ensure_ascii=False 允许字符串中显示实际的中文字符
        file.write('\n'.join(data_strings) + '\n')

    if last_link:
        last_link_filename = f'{site}_last_link.txt'
        with open(last_link_filename, 'w', encoding='utf-8') as file:
            file.write(last_link)


def fetch_jinse(driver):
    print("Current Fetching Jinse")
    url = "https://www.jinse.com/lives"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".js-lives__item")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('jinse')
    last_title = None
    reached_last_record = False
    scroll_count = 0
    start_index = 0

    results = []

    while scroll_count < 10 and not reached_last_record:
        print("Scroll Count:", scroll_count)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-lives__item")))
        time.sleep(10)
        articles = driver.find_elements(By.CSS_SELECTOR, ".js-lives__item")

        if last_title:
            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, "a.title").text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            title = article.find_element(By.CSS_SELECTOR, "a.title").text
            print(title)
            link = article.find_element(By.CSS_SELECTOR, "a.title").get_attribute('href')

            if link == last_link:
                reached_last_record = True
                break
            # if "比特币" in title:
            if "稳定币" in title or "stablecoin" in title:
                results.append({'title': title, 'link': link})

            last_title = title

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1

    # Save new results if any
    if results:
        save_data("./info/jinse", results, results[-1]['link'])

    # Debug information to see how many scrolls were performed and if last record was reached
    print("jinse Results:", results)
    print(f"Scrolled jinse {scroll_count} times; Reached last record: {reached_last_record}")


def fetch_odaily(driver):
    print("Current Fetching Odaily")
    url = "https://www.odaily.news/newsflash"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "._10Kq18pH")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('odaily')
    last_title = None
    results = []
    current_clicks = 0
    reached_last_record = False
    start_index = 0

    while current_clicks < 10 and not reached_last_record:
        print("Current Click:", current_clicks)
        # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "._10Kq18pH")))
        time.sleep(10)
        articles = driver.find_elements(By.CSS_SELECTOR, "._10Kq18pH")

        if last_title:
            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, ".hZVqeSqH").text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            title = article.find_element(By.CSS_SELECTOR, ".hZVqeSqH").text
            print(title)
            link = article.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            time_stamp = article.find_element(By.CSS_SELECTOR, "._1hNP0tDU").text

            if link == last_link:
                reached_last_record = True
                break

            # if "比特币" in title:
            if "稳定币" in title or "stablecoin" in title:

                results.append({
                    'time': time_stamp,
                    'title': title,
                    'link': link,
                })
            last_title = title

        try:

            more_button = driver.find_element(By.CSS_SELECTOR, "._2wlGZCh1 .sxH7phty")
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            more_button.click()
            current_clicks += 1
        except NoSuchElementException:
            break

    if results:
        save_data('./info/odaily', results, results[-1]['link'])

    print("Odaily Results:", results)
    print(f"Scrolled Odaily {current_clicks} times; Reached last record: {reached_last_record}")


def fetch_chaincatcher(driver):
    print("Current Fetching Chaincatcher")
    url = "https://www.chaincatcher.com/news"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".v-timeline-item")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('chaincatcher')
    results = []
    last_title = 0
    scroll_count = 0
    reached_last_record = False
    start_index = 0

    while scroll_count < 10 and not reached_last_record:
        print("Scroll Count:", scroll_count)
        # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".v-timeline-item")))
        time.sleep(10)
        articles = driver.find_elements(By.CSS_SELECTOR, ".v-timeline-item")

        if last_title:
            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, ".timeline_title .text").text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            title = article.find_element(By.CSS_SELECTOR, ".timeline_title .text").text
            print(title)
            link = article.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            time_stamp = article.find_element(By.CSS_SELECTOR, ".dateTime").text
            if link == last_link:
                reached_last_record = True
                break
            if "稳定币" in title or "stablecoin" in title:
            # if "BTC" in title or "比特币" in title:
                results.append({'time': time_stamp,
                                'title': title,
                                'link': link})
                print(results)

            last_title = title

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        scroll_count += 1

    if results:
        save_data('./info/chaincatcher', results, results[-1]['link'])
    print("Chaincatcher Results:", results)
    print(f"Scrolled Chaincatcher {scroll_count} times; Reached last record: {reached_last_record}")


def fetch_theblockbeats(driver):
    print("Current Fetching theblockbeats")
    url = "https://www.theblockbeats.info/newsflash"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.news-flash-item-top")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('theblockbeats')
    results = []
    current_clicks = 0
    last_title = 0
    reached_last_record = False
    start_index = 0

    while current_clicks < 10 and not reached_last_record:
        print("Current Click:", current_clicks)
        # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.news-flash-item-top")))
        time.sleep(10)
        articles = driver.find_elements(By.CSS_SELECTOR, "div.news-flash-item-top")

        if last_title:
            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, ".news-flash-title-text").text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            time_stamp = article.find_element(By.CSS_SELECTOR, ".news-flash-title").text.strip()
            title = article.find_element(By.CSS_SELECTOR, ".news-flash-title-text").text.strip()
            print(title)
            link = article.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

            if link == last_link:
                reached_last_record = True

            # if "BTC" in title or "比特币" in title:
            if "稳定币" in title or "stablecoin" in title:
                results.append({
                    'title': title,
                    'time': time_stamp,
                    'link': link
                })
            last_title = title
        try:
            more_button = driver.find_element(By.CSS_SELECTOR, "div.articleList_more")
            # driver.execute_script("arguments[0].click();", more_button)
            more_button.click()
            time.sleep(1)
            current_clicks += 1
        except NoSuchElementException:
            break

    if results:
        save_data('./info/theblockbeats', results, results[-1]['link'])
    print("theblockbeats Results:", results)
    print(f"Scrolled theblockbeats {current_clicks} times; Reached last record: {reached_last_record}")


def fetch_techflowpost(driver):
    print("Current Fetching techflowpost")
    url = "https://www.techflowpost.com/newsletter/index.html"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "dl")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('techflowpost_last_title')
    results = []
    last_title = None
    current_clicks = 0
    reached_last_record = False
    start_index = 0

    while current_clicks < 2 and not reached_last_record:
        print("Current Click:", current_clicks)
        # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "dl")))
        time.sleep(10)
        articles = driver.find_elements(By.CSS_SELECTOR, 'dl')

        if last_title:
            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, 'dd a').text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            date = article.find_element(By.CSS_SELECTOR, 'dt').text
            title = article.find_element(By.CSS_SELECTOR, 'dd a').text
            print(title)
            link = article.find_element(By.CSS_SELECTOR, 'dd a').get_attribute('href')

            if link == last_link:
                reached_last_record = True

            if "稳定币" in title or "Stablecoin" in title:
                results.append({
                    'title': title,
                    'date': date,
                    'link': link
                })
            last_title = title

        try:
            more_button = driver.find_element(By.CSS_SELECTOR, 'a.linmore')
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(10)
            current_clicks += 1
        except NoSuchElementException:
            break

    if results:
        save_data('./info/techflowpost', results, results[-1]['link'])

    print("techflowpost Results:", results)
    print(f"Scrolled techflowpost {current_clicks} times; Reached last record: {reached_last_record}")


def fetch_foresightnews(driver):
    print("Current Fetching foresightnews")
    url = "https://foresightnews.pro/news"
    driver.get(url)
    # wait = WebDriverWait(driver, 10)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".el-timeline-item")))
    except TimeoutException:
        print("Page did not load in time. Stopping further execution.")
        return

    last_link = read_last_record('foresightnews_last_link')
    last_title = None
    results = []
    scroll_count = 0
    reached_last_record = False
    start_index = 0
    max_count = 10

    while scroll_count < max_count and not reached_last_record:
        print("Scroll Count:", scroll_count)
        # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".news-item")))
        articles = driver.find_elements(By.CSS_SELECTOR, ".el-timeline-item")

        if last_title:

            for index, article in enumerate(articles):
                title = article.find_element(By.CSS_SELECTOR, ".news_body_title").text
                if title == last_title:
                    start_index = index + 1
                    break

        for article in articles[start_index:]:
            title_element = article.find_element(By.CSS_SELECTOR, ".news_body_title")
            title = title_element.text
            print(title)
            link = title_element.get_attribute('href')

            date_element = article.find_element(By.CSS_SELECTOR, ".el-timeline-item__timestamp.is-top")
            date = date_element.text.strip()

            if link == last_link:
                reached_last_record = True
                break

            if "稳定币" in title or "Stablecoin" in title:
            # if "比特币" in title:
                results.append({'date': date, 'title': title, 'link': link})
            last_title = title

        if not reached_last_record:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            scroll_count += 1

    if results:
        save_data('./info/foresightnews', results, results[-1]['link'])

    print("foresightnews Results:", results)
    print(f"Scrolled foresightnews {scroll_count} times; Reached last record: {reached_last_record}")


def crawl_sites():
    driver = init_driver()
    try:
        fetch_jinse(driver)
        fetch_odaily(driver)
        fetch_chaincatcher(driver)
        fetch_theblockbeats(driver)
        fetch_techflowpost(driver)
        fetch_foresightnews(driver)
    finally:
        driver.quit()


def main():
    os.chdir(os.getcwd())
    crawl_sites()
    # schedule.every(1).minutes.do(crawl_sites)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()
