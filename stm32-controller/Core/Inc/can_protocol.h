ifndef CAN_PROTOCOL_H
#define CAN_PROTOCOL_H


/* Contrôleur -> STM32 */
#define CAN_ID_LED_CMD     0x100   /* DB0 = état LED            */
#define CAN_ID_VALUE_REQ   0x101   /* aucune donnée utile       */


/* STM32 -> Contrôleur */
#define CAN_ID_LED_STATE   0x200   /* réservé, non implémenté   */
#define CAN_ID_COUNTER     0x201   /* DB0-DB1 = uint16 big-endian */
#define CAN_ID_ACK         0x210   /* DB0 = code                */


#define LED_OFF    0x00
#define LED_ON     0x01


#define ACK_ERROR  0x00
#define ACK_OK     0x01


#endif
