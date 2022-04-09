"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        # iterating through carts
        for cart in self.carts:
            # registering cart
            cart_id = self.marketplace.new_cart()

            # iterating through current cart operations
            for operation in cart:
                op_no = operation['quantity']
                iters = 0
                # performing the specified operations
                while iters < op_no:
                    if operation['type'] == 'add':
                        # if something needs to be added
                        ret = self.marketplace.add_to_cart(cart_id, operation['product'])
                    else:
                        # if something needs to be removed
                        ret = self.marketplace.remove_from_cart(cart_id, operation['product'])

                    if ret or ret is None:
                        iters += 1
                    else:
                        # if the previous operation failed
                        time.sleep(self.retry_wait_time)

            # placing order at the marketplace
            self.marketplace.place_order(cart_id)
