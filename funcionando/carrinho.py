import json
from datetime import datetime


class Carrinho:

    def __init__(self):
        self.itens = []
        self.abandonos = []
        self.fechado = False
    
    