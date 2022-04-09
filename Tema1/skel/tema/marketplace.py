"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from threading import currentThread, Lock
import unittest
import logging
from logging.handlers import RotatingFileHandler
import time

logging.basicConfig(
        handlers=[RotatingFileHandler('marketplace.log', maxBytes=100000, backupCount=15)],
        level=logging.INFO & logging.ERROR,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

logging.Formatter.converter = time.gmtime   # converted to gmtime

class ProductsInfo:
    """
    Class that contains all the deteils about the products in the implementation.
    It uses dictionaries to make accessing the product or the producer easier.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor
        """
        self.products_no = []  # no. of items of each producer
        self.products = []  # list with all products from all producers
        self.product_and_producer = {}  # stores (product, producer) information
        self.queue_size_per_producer = queue_size_per_producer  # max no. of items per producer
        logging.info('ProductsInfo constructor called with parameter: queue_size_per_producer = %d', queue_size_per_producer)

    def check_producer(self, producer):
        """
        Check if the current producer has already reached the maximum number
        of items published
        """
        return_value = False
        if self.products_no[producer] >= self.queue_size_per_producer:
            logging.error('Producer %s reached the maximum number of public items', producer)
        else:
            return_value = True
        logging.info('Check producer %d and got result %s', producer, return_value)
        return return_value

    def get_next_id(self):
        """
        Gets the next available id for a producer
        """
        next_id = len(self.products_no)
        logging.info('Got the next available ID for a producer and the result is %d', next_id)
        return next_id

class CartsInfo:
    """
    Class that contains all the details about the carts in the implementation.
    It uses dictionaries to make accessing the carts easier.
    """
    def __init__(self):
        """
        Constructor
        """
        logging.info('CartsInfo constructor called')
        self.carts = {}  # (cart_id, list of products)
        self.__carts_no = 0  # the total number of carts

    def get_next_id(self):
        """
        Method used for getting the next available id for a chart
        """
        next_id = self.__carts_no
        self.__carts_no += 1 # a new cart is added
        self.carts[next_id] = [] # the cart is empty
        logging.info('Got the next available ID for a cart and the result is %d', next_id)
        return next_id

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        logging.info('Marketplace constructor called with parameter %d', queue_size_per_producer)
        self.carts_info = CartsInfo()
        self.products_info = ProductsInfo(queue_size_per_producer)

        self.producer_lock = Lock()  # lock used when creating a producer
        self.consumer_lock = Lock()  # lock used when creating a consumer
        self.cart_lock = Lock()  # lock used for updating a cart

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # synchronizing the producers
        with self.producer_lock:
            producer_id = self.products_info.get_next_id()
            self.products_info.products_no.append(0)
        logging.info('Registred a new producer with id %d', producer_id)
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        result = False
        # check if the producer can add anything else
        if  self.products_info.check_producer(producer_id):
            # increase the number of products for this producer
            self.products_info.products_no[producer_id] += 1
            # add an entry for this producer with the correspoing product id
            self.products_info.product_and_producer[product] = producer_id

            # add product to the list of products
            self.products_info.products.append(product)
            result = True
        logging.info('Published the product %s provided by the producer %d', product, producer_id)
        return result

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.consumer_lock:
            # get the next available id for the new chart
            cart_id = self.carts_info.get_next_id()
        logging.info('Created a new cart with id %d', cart_id)
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.cart_lock:
            # check if the product exists
            if product not in self.products_info.products:
                logging.error('The product %s does not exist and cannot be added to the cart %d', product.get_name(), cart_id)
                return False

            # if the product exists, it is removed from the store
            producer_id = self.products_info.product_and_producer[product]
            # firstly, from the internal list of the producer
            self.products_info.products_no[producer_id] -= 1

            # the from the list containg all the products
            self.products_info.products.remove(product)

            # lastly, it is added to the cart
            self.carts_info.carts[cart_id].append(product)
            logging.info('The product %s is added to the cart %d', product.get_name(), cart_id)
            return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # guard
        # check if the product is in the current cart
        if product not in self.carts_info.carts[cart_id]:
            logging.error('The product %s is not in the cart %d and cannot be removed', product.get_name(), cart_id)
            return False
        # get the id of the producer
        producer_id = self.products_info.product_and_producer[product]

        # removing product from cart
        self.carts_info.carts[cart_id].remove(product)

        # appending product to the list with all the products
        self.products_info.products.append(product)

        # increase the number of available products for the producer
        self.products_info.products_no[producer_id] += 1
        logging.info('The product %s is removed from the cart %d', product.get_name(), cart_id)
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # th products in the current cart
        products = self.carts_info.carts.pop(cart_id, None)

        # printing products
        for product in products:
            print(f'{currentThread().getName()} bought {product}')

        logging.info('The order corresponding to the cart %d was placed', cart_id)
        return products

class TestMarketplace(unittest.TestCase):

    def setUp(self):
        self.marketplace = Marketplace(4)

    def test_register_producer(self):
        self.assertEqual(self.marketplace.register_producer(), 0)
        self.assertEqual(self.marketplace.register_producer(), 1)
        self.assertEqual(self.marketplace.register_producer(), 2)
