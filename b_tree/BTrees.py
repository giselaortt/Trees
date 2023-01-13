from copy import deepcopy
from multipledispatch import dispatch
import collections
from array import array
from typing import Type
from skip_list import SkipList


class Node():
    precision = 0.00001

    def __init__( self, key:int, parentNode:'Node' = None, children:list = None, max_len:int = 10 ):
        self.keys = SkipList( )
        self.keys.insert( key )
        self.numberOfChildren = 0
        self.parent = parentNode
        if( children is not None ):
            #deep copy is important!
            self.children = list(children)
            for child in children:
                child.parent = self
        else:
            self.children = None
        self.max_len = max_len


    def isLeaf( self ) -> bool:
        return ( self.children is None )


    @dispatch( object )
    def __eq__( self, other:'Node' ):
        return (self.keys == other.keys)


    def __repr__( self ):
        return "["+ ", ".join([str(value) for value in self.keys])+"]"


    def hasExceded( self ):
        return ( len(self.keys) >= self.max_len )


    @dispatch( (int,float) )
    def __contains__( self, value:int ):
        return ( value in self.keys )


    def insert( self, key:int ) -> None:
       self.keys.insert(key)


    def removeChild( self, child:'None' ) -> None:
        if( self.children is None ):
            return
        for i in range( len(self.children) ):
            if( self.children[i] is child ):
                del self.children[i]
                return


    def split( self ):
        pass


    def insertNode( self, node:'Node' )->None:
        pass


class BTree():

    def __init__( self ):
        self.root = None


    def __contains__( self, key:int ) -> bool:
        return ( self.search( key ) is not None )


    def __repr__( self ):
        if( self.root is None ):
            return "< >"
        #ans = "<"+ " ".join([str(node) for node in self.pre_order()])+">"
        ans = "<"+ " ".join([str(self.pre_order())])+">"
        return ans


    def pre_order( self ) -> list:
        if(self.root is None):
            return []
        answer = []
        BTree._pre_order(self.root, answer)
        return answer


    @staticmethod
    def _pre_order( node:Type[Node], answer:list ) -> list:
        pass
    #    answer.append(node)
    #    if( node.children is None ):
    #        return
    #    for child in node.children:
    #        BTree._pre_order( child, answer )


    def isEmpty( self ):
        return ( self.root is None )


    def search( self, key:int ) -> Node:
        if( self.isEmpty() ):
            return None
        node = BTree._search( key, self.root )
        if(key in node):
            return node
        return None


    def _findNodeToInsert( self, key:int ) -> Type[Node]:
        node = BTree._search( key, self.root )
        if( key in node ):
            raise Exception("Operation not allowed.")
        return node


    @staticmethod
    def _search( key:int, node:Type[Node] ) -> Type[Node]:
        if( type(node) is not Node ):
            raise TypeError('expected type Node')
        if( key in node or node.isLeaf() ):
            return node
        """
        if( key < node.keys[0] ):
            return BTree._search( key, node.children[0] )
        if( node.isThreeNode() and key > node.keys[1] ):
            return BTree._search( key, node.children[2] )
        return BTree._search( key, node.children[1] )
        """


    def insert( self, key:int ) -> None:
        if( self.root is None ):
            self.root = Node( key )
            return
        node = self._findNodeToInsert( key )
        node.insert(key)
        self.bubbleUp(node)


    def bubbleUp( self, node:Type[Node] ) -> None:
        while(node.hasExceded()):
            node.split()
            if(node.parent is not None):
                node.parent.removeChild( node )
                node.parent.insertNode( node )
                node = node.parent


    def remove( self, key ):
        pass

