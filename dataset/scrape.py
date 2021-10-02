import uuid
import time
import json
import logging
import colorlog
import numpy as np
import pandas as pd
from urllib import request
# from os.path import exists

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException, StaleElementReferenceException, NoSuchElementException, InvalidArgumentException


def colorize(obj):
    return highlight(pformat(obj), PythonLexer(), Terminal256Formatter())

class TweetScraper:

    def __init__(self, dataset=None, loglevel=logging.DEBUG, expand=4):
        # Create a colorful logger for better debugging
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s: - %(funcName)20s():%(message)s'))
        self.logger = colorlog.getLogger('birdseye')
        self.logger.addHandler(handler)
        self.logger.setLevel(loglevel)

        # Create a new Safari window
        self.driver = webdriver.Safari()

        self.dataset = pd.read_excel(dataset) if dataset is not None else None
        self.expand = expand
        self.tweets = []


    def sleep_until_loaded(self):
        # Wait until the articles are loaded and available
        articles = self.driver.find_elements_by_xpath("//article")
        while len(articles) == 0:
            time.sleep(3)
            articles = self.driver.find_elements_by_xpath("//article")


    def sleep_between_interactions(self, loc=2, scale=2):
        sleep_time = np.clip(np.random.normal(loc, scale), 2, 5)
        self.logger.debug('Sleeping for %d seconds', sleep_time)
        time.sleep(sleep_time)


    def sleep_between_tweets(self, loc=20, scale=20):
        sleep_time = np.clip(np.random.normal(2, 2), 3, 60)
        time.sleep(sleep_time)


    def read_dataset(self, filename, start='0000-01-01 00:00:00', end='9999-12-31 23:59:59'):
        self.logger.info('Reading dataset from: %s' % filename)
        dataset = pd.read_csv(filename)
        dataset['url'] = dataset['text'].apply(lambda text: text[-23:])
        selection = (dataset['date'] <= end) & (dataset['date'] >= start)
        self.dataset = dataset[selection]
        self.logger.debug(self.dataset)
        self.dataset.to_excel('./data/initial.xlsx')


    def expland_replies(self, timeline):
        elements = timeline.find_elements_by_xpath("./div/div")
        self.logger.debug('Found %d elements in the timeline' % len(elements))
        for element in elements:
            try:
                # self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.logger.debug('Element text: %s' % repr(element.text))
                # if element.text == 'Show replies':
                #     element.click()
                #     self.sleep_between_interactions()
                if element.text == 'Show more replies':
                    element.find_element_by_xpath("./div").click()
                    self.sleep_between_interactions()
                elif element.text == 'More Tweets':
                    self.logger.info('Reached the end of replies. Stopping.')
                    break
            except StaleElementReferenceException:
                break
        
        elements = timeline.find_elements_by_xpath("./div/div")
        self.logger.debug('End of expansion. Now there are %d elements in the timeline' % len(elements))


    def parse_tweet_element(self, element, reply_to=None):
        tweet = {
            'uuid': str(uuid.uuid4()),
            'tweet_id': self.driver.current_url.rsplit('/', 1)[-1],
            'replies': [],
            'reply_to': reply_to['uuid'] if reply_to else None,
        }
        if reply_to is not None:
            reply_to['replies'].append(tweet['uuid'])

        try:
            author = element.find_element_by_xpath(".//article/div/div/div/div[2]")
        except NoSuchElementException:
            return False, False

        try:
            avatar = element.find_element_by_xpath(".//article//img[1]")
            tweet['avatar'] = avatar.get_attribute('src')
            
        except NoSuchElementException:
            return False, False
        
        tweet['user_handle'] = author.text.rsplit('@', 1)[-1]
        tweet['user_name'] = author.text.rsplit('@', 1)[0]

        contents = element.find_elements_by_xpath(".//article/div/div/div/div/div")

        self.logger.debug("Logging the content elements:")
        for content in contents:
            self.logger.debug(repr(content.text))
        if reply_to is not None:
            try:
                tweet['content'] = contents[3].text + '\n' + contents[4].text
            except IndexError:
                self.logger.debug('This tweet seems to be a reply to a reply. Skipping.')
                return False, False
        else:
            tweet['content'] = contents[3].text
        tweet['date'] = contents[-3].text
        tweet['engagement'] = contents[-2].text
            
        self.logger.info('Tweet: %s' % colorize(tweet))
        return tweet, False


    def find_timeline(self):
        return self.driver.find_element_by_xpath("//div[@aria-label='Timeline: Conversation']")


    def click_tweet(self, tweet):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(tweet, 5, 5)
        action.click()
        try:
            action.perform()
        except MoveTargetOutOfBoundsException:
            self.driver.execute_script('arguments[0].scrollIntoView();', tweet)
            action.perform()


    def step_into_reply(self, previous_url, element, reply_to=None):
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)
        # self.driver.execute_script('arguments[0].addEventListener("click", function (e) {e.stopPropagation();});', element)
        self.driver.execute_script("document.body.style['-webkit-user-select'] = 'none';")

        self.logger.info("Attempting to click a reply.")
        try:
            self.click_tweet(element)
        except MoveTargetOutOfBoundsException:
            self.logger.warning("Can't click this tweet. Skipping it.")
            return False, False
        
        self.sleep_between_interactions()
        self.sleep_until_loaded()

        self.logger.debug('Loaded page %s' % self.driver.current_url)

        newtab = False  # Whether the tweet opened in a new tab or a 
        for handle in self.driver.window_handles:
            if handle != self.maintab:
                self.driver.switch_to.window(handle)
                newtab = True
                break

        # Find the Timeline element
        try:
            timeline = self.driver.find_element_by_xpath("//div[@aria-label='Timeline: Conversation']")
        except Exception:
            if newtab:
                self.driver.close()
                self.driver.switch_to.window(self.maintab)
                return False, False
            else:
                self.logger.error("Error getting the timeline. We also aren't in a new tab. Abandoning this line of tweets.")
                return False, True
        
        self.logger.info('Successfully located the timeline.')
        post = timeline.find_element_by_xpath("./div/div[2]")

        tweet, abandon = self.parse_tweet_element(post, reply_to=reply_to)
        
        if newtab:
            self.driver.close()
            self.driver.switch_to.window(self.maintab)
        else:
            self.logger.warning('We have fell into the pit of no return. Abandoning this line of tweets now. End of the line.')
            return tweet, True

        return tweet, abandon


    def grab_tweets(self):
        # for _, row in self.dataset.iterrows():
        for _, row in self.dataset.iterrows():

            if row['url'] != 'https://twitter.com/cnnbrk/status/1337810503981264903':
                continue

            self.logger.info('Grabbing tweet from: %s' % row['url'])
            try:
                self.driver.get(row['url'])
            except InvalidArgumentException:
                self.logger.warning('%s is not a valid URL. Skipping.' % row['url'])
                continue
            self.maintab = self.driver.current_window_handle

            # Wait until the articles are loaded and available
            self.sleep_until_loaded()

            # Disable text selection to prevent clicks being accidentally interpreted as text selection.
            self.driver.execute_script("document.body.style['-webkit-user-select'] = 'none';")

            # Find the Timeline element
            timeline = self.find_timeline()
            self.logger.info('Successfully located the timeline.')

            # Expand the replies for some rounds.
            for i in range(self.expand):
                self.expland_replies(timeline)
                timeline = self.find_timeline()

            # Finally grab the expanded elements in the timeline
            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            self.sleep_between_interactions()
            timeline = self.find_timeline()
            elements = timeline.find_elements_by_xpath("./div/div")
            self.logger.info('Found %d elements in the timeline' % len(elements))

            self.logger.info('Parsing timeline elements...')

            main_tweet = None

            index = 0
            while index < len(elements):
                print(index, len(elements))
                timeline = self.driver.find_element_by_xpath("//div[@aria-label='Timeline: Conversation']")
                elements = timeline.find_elements_by_xpath("./div/div")
                element = elements[index]
                self.logger.debug("Element text: %s" % element.text)

                if element.text == 'This Tweet is from a suspended account. Learn more':
                    self.logger.warning('Tweet author suspended. Skipping.')
                    break

                index += 1

                self.driver.execute_script('arguments[0].scrollIntoView({block: "center"});', element)
                self.sleep_between_interactions()

                # Skip empty elements (likely horizontal lines between tweets)
                if element.text == '':
                    continue

                # If the current row username is in the element text, this element contains the main tweet.
                elif (element.text.startswith(row['user_name']) or '@' in element.text) and main_tweet is None:
                    main_tweet, abandon = self.parse_tweet_element(element)
                    if abandon:
                        self.logger.error('Error parsing the main tweet. Skipping this tweet.')
                        break
                    self.logger.info(
                        'Parsed tweet by @%s: %s' % 
                        (main_tweet['user_handle'], repr(main_tweet['content'][:40] + '...'))
                    )
                    self.add_parsed_tweet(main_tweet)

                # Otherwise, the tweet is a reply. By this time, we would have already had the main tweet.
                else:
                    # Skip deleted tweets and "show replies".
                    if  element.text == 'This Tweet was deleted by the Tweet author. Learn more' \
                        or element.text == 'Show replies':
                        self.logger.debug("Not a tweet. Skipping this element: %s" % repr(element.text))
                        continue
                    
                    # When we reach "Show more replies" or "More Tweets", this is the end of our scraping.
                    elif element.text == 'Show more replies' or element.text == 'More Tweets':
                        self.logger.debug("Reached the end of replies.")
                        break

                    tweet, abandon = self.step_into_reply(self.driver.current_url, element, reply_to=main_tweet)

                    if tweet is not False:
                        self.logger.info(
                            'Parsed tweet by @%s: %s' % 
                            (tweet['user_handle'], repr(tweet['content'][:40] + '...'))
                        )
                        self.add_parsed_tweet(tweet)

                    if abandon:
                        self.logger.error('Abandoning this tweet.')
                        break
                # images = piece.find_elements_by_xpath(".//div/div/div/div/div/div/div//img")
                # for image in images:
                #     source = image.get_attribute('src')
                #     self.logger.debug('Found image with src: %s' % source)
                #     if 'profile_images' in source:
                #         tweet['profile'] = image
            
        self.driver.quit()


    def add_parsed_tweet(self, tweet):
        extension = tweet['avatar'].rsplit('.', 1)[-1]
        tweet['avatar_extension'] = extension
        self.tweets.append(tweet)

        with open('./data/tweets/%s.json' % tweet['uuid'], 'w') as f:
            f.write(json.dumps(tweet));

        with request.urlopen(tweet['avatar']) as response:
            data = response.read()
            with open('./data/avatars/%s.%s' % (tweet['uuid'], extension), 'wb') as f:
                f.write(data);

if __name__ == '__main__':
    scraper = TweetScraper(dataset='./data/initial.xlsx')

    # Read dataset
    # scraper.read_dataset(
    #     './data/vaccination_all_tweets.csv', 
    #     start='2020-12-12 00:00:00', 
    #     end='2020-12-19 00:00:00'
    # )

    # Grab all tweets
    scraper.grab_tweets()

    # Print a dataframe
    scraped = pd.DataFrame(scraper.tweets)
    print(scraped)
    scraped.to_excel('./data/scraped.xlsx')
    
