"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        # get the corresponding id for thie producer
        self.producer_id = marketplace.register_producer()

    def run(self):
        while True:
            # publish all the products for this producer
            for (product, qty, _) in self.products:
                i = 0
                while i < qty:
                    # checking if the operation was successful
                    if self.marketplace.publish(self.producer_id, product):
                        i += 1
                    # if not, sleep and try again
                    time.sleep(self.republish_wait_time)
                        