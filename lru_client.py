import random
import grpc 

import lru_pb2_grpc
import lru_pb2
import google.protobuf

prev_reqs = []

def print_data(data):
    print(data.address,end=", ")
    print(data.data,end=", ")
    print(lru_pb2.Data.cache_miss_hit_evict.Name(data.status))

def close(channel):
    channel.close()

def run():
    with grpc.insecure_channel("localhost:6515") as channel:
        stub = lru_pb2_grpc.MemoryStub(channel)
        response = stub.read(lru_pb2.Read(address = 675))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 112))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 143))
        print_data(response)
        
        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 675))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 143))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 112))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)


        response = stub.read(lru_pb2.Read(address = 675))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)

        response = stub.read(lru_pb2.Read(address = 145))
        print_data(response)

        response = stub.image(google.protobuf.empty_pb2.Empty())
        for i in response.data:
            print(i)
        channel.unsubscribe(close)
        exit()


run()

