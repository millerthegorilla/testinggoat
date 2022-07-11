from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ListPage(object):

    def __init__(self, test):
        self._list_name = ""
        self.test = test
        if self.test.browser.current_url != self.test.live_server_url:
            self.test.browser.get(self.test.live_server_url)

    @property
    def list_name(self):
        return self._list_name

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')
    
    def get_error_element(self):
        return self.test.browser.find_element_by_css_selector('.has-error')
 
    @FunctionalTest.wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        try:
            self.wait_for_row_in_list_table(item_text, new_item_no) 
            if self.list_name == "":
                self._list_name = item_text
        except Exception as e:
            raise(e)
        return self

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

    def get_share_with_list(self):
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)

        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
                           email,
                           [item.text for item in self.get_shared_with_list()]
        ))
