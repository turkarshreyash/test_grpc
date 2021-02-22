from  concurrent import futures
import string
import random

import grpc

import lru_pb2
import lru_pb2_grpc

def getFromDisk(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class node:
    def __init__(self):
        self.address = 0
        self.next = None
        self.prev = None
        self.data = ''

class Memory(lru_pb2_grpc.MemoryServicer):

    def __init__(self):
        self.head = None
        self.tail = None
        self.hash = dict()
        self.limit = 3

    def read(self, request, context):
        # implementation
        
        if request.address in self.hash:
            print("%d, HIT!"%(request.address))
            mNode = self.hash[request.address]
            if mNode != self.head:
                mNode.prev.next = mNode.next
                if mNode.next != None:
                    mNode.next.prev = mNode.prev
                else:
                    self.tail = mNode.prev
                mNode.next = self.head
                self.head.prev = mNode
                self.head = mNode
            return lru_pb2.Data(address = mNode.address, data = mNode.data, status = lru_pb2.Data.cache_miss_hit_evict.HIT)

        cache_miss = lru_pb2.Data.cache_miss_hit_evict.MISS
        if len(self.hash) >= self.limit:
            print("%d, EVICT!"%(request.address))
            self.hash.pop(self.tail.address)
            print(self.tail.data)
            self.tail = self.tail.prev
            self.tail.next = None
        
            cache_miss = lru_pb2.Data.cache_miss_hit_evict.EVICT
        else:
            print("%d, MISS!"%(request.address))

        
        mNode = node()
        mNode.address = request.address
        mNode.data = getFromDisk()
        mNode.next = self.head
        self.hash[mNode.address] = mNode
        if self.head != None:
            self.head.prev = mNode
        else:
            self.tail = mNode
        self.head = mNode
        return lru_pb2.Data(address = request.address, data = mNode.data, status = cache_miss)




    def image(self,request,context):

        mImage = lru_pb2.MemImageData()
        itr = self.head
        while itr != None:
            mImage.data.append(itr.data)
            itr = itr.next
        return mImage


def lruServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    lru_pb2_grpc.add_MemoryServicer_to_server(Memory(),server)
    server.add_insecure_port("[::]:6515")
    server.start()
    while True:
        pass
    server.stop(0)



if __name__ == "__main__":
    lruServer()
