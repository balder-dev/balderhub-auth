import balder

from tests.lib.scenario_features.base_dut_manager_feature import BaseDutManagerFeature
from tests.lib.utils import my_action
from tests.lib.utils.dut_simulator import DUTSimulator
from tests.lib.utils.my_resource import MyResource
from tests.lib.utils.my_data_item_resource import MyDataItemResource
from tests.lib.utils.data_items.book_data_item import BookDataItem
from tests.lib.utils.data_items.author_data_item import AuthorDataItem
from tests.lib.utils.data_items.book_category_data_item import BookCategoryDataItem


AUTHOR_1 = AuthorDataItem(id=1, first_name='Jane', last_name='Austen')
AUTHOR_2 = AuthorDataItem(id=2, first_name='George', last_name='Orwell')
AUTHOR_3 = AuthorDataItem(id=3, first_name='Mark', last_name='Twain')

CATEGORY_1 = BookCategoryDataItem(id=1, name='Fiction')
CATEGORY_2 = BookCategoryDataItem(id=2, name='Science')

BOOK_1 = BookDataItem(id=1, title='Pride and Prejudice', author=AUTHOR_1, category=CATEGORY_1)
BOOK_2 = BookDataItem(id=2, title='1984', author=AUTHOR_2, category=CATEGORY_1)
BOOK_3 = BookDataItem(id=3, title='Adventures of Huckleberry Finn', author=AUTHOR_3, category=CATEGORY_2)


class DataItemDutManagerFeature(BaseDutManagerFeature):

    def define_dut_environment(self, dut_simulator: DUTSimulator):
        # public resource (no auth needed)
        dut_simulator.add_public_resource(MyResource('catalog'), actions=[my_action.RETRIEVE])

        # authenticated resources for books (unresolved, data-item-based)
        books_resource = MyDataItemResource('books', BookDataItem)
        for book in [BOOK_1, BOOK_2, BOOK_3]:
            resolved = books_resource.get_resolved_resource(MyDataItemResource.Parameter(data_item=book))
            dut_simulator.add_authenticated_resource(
                resolved, actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE])

        # authenticated resources for authors (unresolved, data-item-based)
        authors_resource = MyDataItemResource('authors', AuthorDataItem)
        for author in [AUTHOR_1, AUTHOR_2, AUTHOR_3]:
            resolved = authors_resource.get_resolved_resource(MyDataItemResource.Parameter(data_item=author))
            dut_simulator.add_authenticated_resource(
                resolved, actions=[my_action.RETRIEVE, my_action.UPDATE])

        # testuser has permission for books 1 and 2 (RETRIEVE, UPDATE) but not book 3
        for book in [BOOK_1, BOOK_2]:
            resolved = books_resource.get_resolved_resource(MyDataItemResource.Parameter(data_item=book))
            dut_simulator.grant_permission('testuser', resolved, my_action.RETRIEVE)
            dut_simulator.grant_permission('testuser', resolved, my_action.UPDATE)

        # testuser has permission for authors 1 and 2 (RETRIEVE) but not author 3
        for author in [AUTHOR_1, AUTHOR_2]:
            resolved = authors_resource.get_resolved_resource(MyDataItemResource.Parameter(data_item=author))
            dut_simulator.grant_permission('testuser', resolved, my_action.RETRIEVE)
