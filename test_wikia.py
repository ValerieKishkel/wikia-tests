#!/usr/bin/env python

import re

from nose.tools import assert_equal, assert_not_equal, assert_in, assert_true
from selenose.cases import SeleniumTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from wikia_page_objects import PageFactory, HomePage, VideoAddPage

__all__ = ['TestScenario1', 'TestScenario2']


class TestScenario1(SeleniumTestCase):

    def setUp(self):
        self.home_page = PageFactory.init(self.driver, HomePage)
        self.driver.get(self.home_page.url)

    def test_redirect_and_login(self):
        page = self.home_page

        # assert for a correct redirect
        assert_equal(self.driver.current_url,
                     'http://qm-homework.wikia.com/wiki/QM_HomeWork_Wikia')

        # assert for mouse over the login label
        assert_true(page.open_login_dropdown())

        # submit login info
        page.submit_login_info(*credentials)

        # assert to check if logged in
        assert_not_equal(page.ajax_login_anchor.get_attribute('title'),
                         u'Log in')

        # optionally check that user profile
        # url is properly generated after log in
        assert_equal(page.ajax_login_anchor.get_attribute('href'),
                     'http://qm-homework.wikia.com/wiki/User:%s' %
                     credentials[0])


class TestScenario2(SeleniumTestCase):

    def setUp(self):
        home_page = PageFactory.init(self.driver, HomePage)

        # navigate & log in
        self.driver.get(home_page.url)
        home_page.open_login_dropdown()
        home_page.submit_login_info(*credentials)
        self.home_page = home_page
        self.video_add_page = PageFactory.init(self.driver, VideoAddPage)

    def test_add_video(self):
        home_page = self.home_page
        video_add_page = self.video_add_page

        # click on contribute dropdown
        home_page.contribute_dropdown_nav.click()
        assert_in('active',
                  home_page.contribute_dropdown_nav.get_attribute('class'))

        add_video_menuitem_anchor = \
            WebDriverWait(self.driver, 10) \
            .until(EC.visibility_of(home_page.add_video_menuitem_anchor))
        add_video_menuitem_anchor.click()

        # selenium won't wait after a click
        # we will need to manually wait for a new page to load
        # one way to do that is by checking document.readyState
        WebDriverWait(self.driver, 10) \
            .until(lambda driver:
                   driver.execute_script('return document.readyState;') ==
                   'complete')

        # assert for a correct redirect
        assert_equal(self.driver.current_url[:len(video_add_page.url)],
                     video_add_page.url)

        # type url into form input
        video_add_page.video_add_url_input.send_keys(youtube_url)

        # click add
        video_add_page.add_submit.submit()

        # assert confirmation message
        assert_true(re.match('Video page .* was successfully added.',
                    video_add_page.confirm_msg_div.text) is not None)

        # grab file name, optionally can use above regex
        filename = video_add_page.confirm_msg_anchor.text.replace(' ', '_')

        # click on message link
        video_add_page.confirm_msg_anchor.click()

        # wait for page to load
        WebDriverWait(self.driver, 10) \
            .until(lambda driver:
                   driver.execute_script('return document.readyState;') ==
                   'complete')

        # check that filename matches current url
        assert_equal(self.driver.current_url,
                     'http://qm-homework.wikia.com/wiki/%s' % filename)

credentials = ('ValerieKish', 'testpass')
youtube_url = 'https://www.youtube.com/watch?v=_q-n8SjU_RI'
