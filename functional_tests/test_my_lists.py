from django.contrib.auth import get_user_model

from .list_page import ListPage
from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user

        self.create_pre_authenticated_session('edith@example.com')
        
        # She goes to the home page and starts a list
        # self.browser.get(self.live_server_url)
        list_page = (ListPage(self).add_list_item('Reticulate splines')
                                   .add_list_item('Immanentize eschaton'))
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.

        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there, named according to its
        # first list item
        
        self.wait_for(lambda: self.browser.find_element_by_link_text(list_page.list_name))
        
        self.browser.find_element_by_link_text(list_page.list_name).click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url,
                      first_list_url)
        )
        
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decideds to start another list, just to see
        self.browser.get(self.live_server_url)
        self.list_page2 = ListPage(self).add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text(self.list_page2.list_name))
        
        self.browser.find_element_by_link_text(self.list_page2.list_name).click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url,
                      second_list_url)
        )

        # She logs out.  The "My Lists" option disappears
        
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
                      self.browser.find_elements_by_link_text('My lists'),
                      [] )
        )
