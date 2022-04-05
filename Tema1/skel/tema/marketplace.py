"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import currentThread, Lock

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
        self.queue_size_per_producer = queue_size_per_producer
        #locks
        self.prod_lock = Lock()
        self.cons_lock = Lock()
        self.carts_lock = Lock()
        self.producers_no = 0
        self.products = {}       # {producer_id, [product0, product1, ..]}
        self.bought = {}        # {product, producer_id}
        self.carts = {}         # {cart_id, [products]}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.prod_lock:
            _id = self.producers_no + 1
        self.products[_id] = []
        return _id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        #guard
        _id = int(producer_id)
        if len(self.products[_id]) >= self.queue_size_per_producer:
            return False
        self.products[_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        _id = len(self.carts)
        with self.cons_lock:
            self.carts[_id] = []
        return _id

    def get_producer_id(self, product):
        for (ids, p) in self.products:
            if product in p:
                return ids
        return -1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.
        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.carts_lock:
            if product not in self.products.values():
                return False
            _id = self.get_producer_id(product)
            self.bought[product] = _id
            self.products = {key:val for key, val in self.products.items() if val != product}
        self.carts[cart_id].append(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.carts[cart_id].remove(product)
        producer_id = self.bought[product]
        self.products[producer_id].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        products = self.carts.pop(cart_id, None)
        for product in products:
            print(f'{currentThread().getName()} bought {product}')
        return 
