import time
import can

CAN_ID_LED_CMD   = 0x100
CAN_ID_VALUE_REQ = 0x101
CAN_ID_COUNTER   = 0x201
CAN_ID_ACK       = 0x210


##Listening for Specific Frames
def wait_for(bus, arbitration_id, timeout=1.0):
    """Return the first frame with the given ID, or None on timeout."""
    end = time.time() + timeout
    while time.time() < end:
        msg = bus.recv(timeout=end - time.time()) #Fetches incoming CAN frames from the Linux RX buffer.
        if msg is not None and msg.arbitration_id == arbitration_id:
            return msg
    return None


def send_led(bus, state):
    msg = can.Message(arbitration_id=CAN_ID_LED_CMD, data=[state], is_extended_id=False) #Constructs a standard 11-bit CAN frame
    bus.send(msg)
    return wait_for(bus, CAN_ID_ACK)


#Hardware Initialization
def main():
    #Opens the connection to the Pi
    bus = can.interface.Bus(channel="can0", interface="socketcan")
    try:
        # 1. Turn LED ON
        print("TX : commande LED ON")
        ack = send_led(bus, 0x01)
        print(f"RX : 0x210 ACK={ack.data[0]}" if ack else "RX : pas d'ACK")

        time.sleep(1)

        # 2. Turn LED OFF
        print("TX : commande LED OFF")
        ack = send_led(bus, 0x00)
        print(f"RX : 0x210 ACK={ack.data[0]}" if ack else "RX : pas d'ACK")

        # 3. Request Counter Value
        print("TX : demande compteur")
        bus.send(can.Message(arbitration_id=CAN_ID_VALUE_REQ, data=[], is_extended_id=False))
        resp = wait_for(bus, CAN_ID_COUNTER)
        # Receiving and Reconstructing the 16-Bit Integer
        if resp and len(resp.data) >= 2:
            print("RX : 0x201")
            value = (resp.data[0] << 8) | resp.data[1] #shifts the received high byte
            print(f"Valeur : {value}")
        else:
            print("RX : pas de réponse")
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()