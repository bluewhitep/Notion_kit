####################################################################################
# MIT License
#
# Copyright (c) 2023 bluewhitep
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################
import logging

from notion_client import Client, AsyncClient
from notion_client.helpers import get_id

from .gadget import Gadget
from .api import Page, Database, User, Block
    
class kit:
    @staticmethod
    def get_id(url:str) ->str:
        """
        Get id from notion url

        Parameter
            url:            (str)       - Notion url
        """
        return get_id(url)
    
    @classmethod
    def method(cls) -> None:
        cls.Gadget:Gadget = Gadget()
        cls.Page:Page = Page(cls.client, id=None)         
        cls.Database:Database = Database(cls.client, id=None)
        cls.User:User = User(cls.client, id=None)
        cls.Block = Block(cls.client, id=None)
    
    @classmethod
    def Client(cls, token:str, log_level:int=logging.WARNING) ->Client:
        """
        Set client from notion_client

        Parameter
            token:          (str)       - Notion token
            log_level:      (int)       - Log level
        """
        cls.token = token
        cls.log_level = log_level
        cls.client = Client(auth=token, log_level=log_level)
        
        cls.method()
        return  cls.client
        
    @classmethod
    def Async_client(cls, token:str, log_level:int=logging.WARNING) ->AsyncClient:
        cls.token = token
        cls.log_level = log_level
        cls.client = AsyncClient(auth=token, log_level=log_level)
        
        cls.method()
        return  cls.client