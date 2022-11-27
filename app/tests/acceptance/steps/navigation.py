from behave import *
from selenium import webdriver

use_step_matcher('re')

@given('I am on the homepage')
def step_impl(context):
    browser = webdriver.Chrome('C:/Users/Goldb/OneDrive/Desktop')
    browser.get('http://127.0.0.1:5000')
    
    
    