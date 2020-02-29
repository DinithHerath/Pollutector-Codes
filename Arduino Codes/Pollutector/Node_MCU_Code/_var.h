SoftwareSerial SUART(4, 5); //SRX=Dpin-D2; STX-DPin-D1  //9,10

int temperature;
int humidity;
int gasvalue;

const char *ssid = "AladeenMF";
const char *password = "12345678";
const char *mqtt_server = "broker.hivemq.com";
char JSONmessageBuffer[400];

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
