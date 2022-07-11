from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .list_page import ListPage


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'
        ))

        #self.assertEqual(list_page, None)

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully

        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item

        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        
        self.get_item_input_box().send_keys('Make tea')
        
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        list_page = ListPage(self).add_list_item('Buy wellies')

        list_page.wait_for_row_in_list_table('Buy wellies', 1)

        # She accidentally tries to enter a duplicate item
        list_page.get_item_input_box().send_keys('Buy wellies')

        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            list_page.get_error_element().text,
                "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        list_page = ListPage(self).add_list_item('Banter too thick')

        list_page.get_item_input_box().send_keys('Banter too thick')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(  
            list_page.get_error_element().is_displayed()  
        ))

        # She starts typing in the input box to clear the error
        list_page.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            list_page.get_error_element().is_displayed()  
        ))

    def test_error_messages_are_cleared_on_any_key_press(self):
        # Edith starts a list and causes a validation error:
        list_page = ListPage(self).add_list_item('test any keypress clears error')

        list_page.wait_for_row_in_list_table('test any keypress clears error', 1)
        list_page.get_item_input_box().send_keys('test any keypress clears error')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            list_page.get_error_element().is_displayed()
        ))
        
        # She clicks into the input element which clears the error
        list_page.get_item_input_box().click()

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            list_page.get_error_element().is_displayed()
        ))

