from .base import CtapHidConnection, HidDescriptor
import socket

fake_descriptor = HidDescriptor("____", 0x1234, 0x1234, 64, 64, "Fake Device", "12345")

class FakeDeviceConnection(CtapHidConnection):
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.connect(('::1', 13231))
        
    def read_packet(self) -> bytes:
        data = self.sock.recv(64)
        
        if len(data) <= 0:
            raise Exception("The remote host sent back no data")
        
        if len(data) != 64:
            raise Exception("The remote host sent an incorrect amount of data")
        
        return data

    def write_packet(self, data: bytes) -> None:
        self.sock.send(data)

    def close(self) -> None:
        self.sock.close()



def make_list_descriptors(other_list_descriptors):
    def list_descriptors():
        descriptors = other_list_descriptors()
        descriptors.append(fake_descriptor)
        return descriptors

    return list_descriptors


def make_get_descriptor(other_get_descriptor):
    def get_descriptor(path):

        if path ==fake_descriptor.path:
            return fake_descriptor

        return other_get_descriptor(path)

    return get_descriptor


def make_open_connection(other_open_connection):
    def open_connection(descriptor):

        if descriptor == fake_descriptor:
            return FakeDeviceConnection(descriptor)

        return other_open_connection(descriptor)

    return open_connection
