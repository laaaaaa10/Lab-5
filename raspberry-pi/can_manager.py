import time
import can


class CanManager:
    def __init__(self, channel="can0", interface="socketcan"):
        self.channel = channel
        self.interface = interface
        self.bus = None

    #Opening and Closing the Socket
    def open(self):
        self.bus = can.interface.Bus(channel=self.channel, interface=self.interface)
    
    #Sending Data
    def send(self, arbitration_id, data=()):
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=list(data),
            is_extended_id=False,
        )
        self.bus.send(msg)

    def receive(self, timeout=1.0):
        """Return (id, data) for the next frame, or None on timeout."""
        msg = self.bus.recv(timeout=timeout)
        if msg is None:
            return None
        return msg.arbitration_id, bytes(msg.data)

    def receive_id(self, arbitration_id, timeout=1.0):
        """Wait for a frame with this ID. Return its data bytes, or None."""
        end = time.time() + timeout
        while True:
            remaining = end - time.time()
            if remaining <= 0:
                return None
            frame = self.receive(timeout=remaining) # Repeatedly called until a frame matching the target arbitration_id arrives (or the timeout runs out).
            if frame is not None and frame[0] == arbitration_id:
                return frame[1]

    
    #Opening and Closing the Socket
    def close(self):
        if self.bus is not None:
            self.bus.shutdown()
            self.bus = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()