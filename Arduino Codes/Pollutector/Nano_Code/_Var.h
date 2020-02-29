int pinDHT11 = A0;
SimpleDHT11 dht11(pinDHT11);
byte temperature = 0;
byte humidity = 0;

NeoSWSerial SUART(2,3); //SRX  = DPin-2; STX = DPin-3

int gassensorValue;
int digitalValue;
