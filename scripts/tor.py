from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
browser = None

proxy_address = "127.0.0.1:8118"
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxy_address,
})

tor = '/usr/bin/tor-browser/Browser/firefox'
firefox_binary = FirefoxBinary(tor)

urls = (
    ('tor_browser_check', 'https://check.torproject.org/'),
    ('icanhazip', 'http://icanhazip.com'),
)
keys, _ = zip(*urls)
urls_map = dict(urls)

def get_browser(binary=None, proxy=None):
    global browser
    if not browser:
        browser = webdriver.Firefox(firefox_binary=binary, proxy=proxy)
    return browser

if __name__ == "__main__":
    browser = get_browser(binary=firefox_binary, proxy=proxy)
    for resource in keys:
        browser.get(urls_map.get(resource))