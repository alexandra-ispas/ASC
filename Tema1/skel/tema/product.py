"""
This module offers the available Products.

Computer Systems Architecture Course
Assignment 1
March 2022
"""

from dataclasses import dataclass


@dataclass(init=True, repr=True, order=False, frozen=True)
class Product:
    """
    Class that represents a product.
    """
    name: str
    price: int

    def get_name(self):
        """
        Returns the name of a 'Product' object
        """
        return self.name


@dataclass(init=True, repr=True, order=False, frozen=True)
class Tea(Product):
    """
    Tea products
    """
    type: str


@dataclass(init=True, repr=True, order=False, frozen=True)
class Coffee(Product):
    """
    Coffee products
    """
    acidity: str
    roast_level: str
