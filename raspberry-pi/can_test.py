import time
from can_manager import CanManager

CAN_ID_LED_CMD   = 0x100
CAN_ID_VALUE_REQ = 0x101
CAN_ID_COUNTER   = 0x201
CAN_ID_ACK       = 0x210


def send_led(can_mgr, state):
    can_mgr.send(CAN_ID_LED_CMD, [state])
    ##Listening for Specific Frames
    return can_mgr.receive_id(CAN_ID_ACK)


#Hardware Initialization
def main():
    #Opens the connection to the Pi (the with-block opens and closes can0 for us)
    with CanManager("can0") as can_mgr:
        # 1. Turn LED ON
        print("TX : commande LED ON")
        ack = send_led(can_mgr, 0x01)
        print(f"RX : 0x210 ACK={ack[0]}" if ack else "RX : pas d'ACK")

        time.sleep(1)

        # 2. Turn LED OFF
        print("TX : commande LED OFF")
        ack = send_led(can_mgr, 0x00)
        print(f"RX : 0x210 ACK={ack[0]}" if ack else "RX : pas d'ACK")

        # 3. Request Counter Value
        print("TX : demande compteur")
        can_mgr.send(CAN_ID_VALUE_REQ)
        data = can_mgr.receive_id(CAN_ID_COUNTER)
        # Receiving and Reconstructing the 16-Bit Integer
        if data and len(data) >= 2:
            print("RX : 0x201")
            value = (data[0] << 8) | data[1] #shifts the received high byte
            print(f"Valeur : {value}")
        else:
            print("RX : pas de réponse")


if __name__ == "__main__":
    main()