void InitSerialCommunication()
{
  Serial.begin(9600);
  SUART.begin(9600);
}
//
//void ReadSerial()
//{
//    byte n = SUART.available();
//    String y;
//    if (n > 0)
//    {
//        String x = SUART.readString();
//        y = x;
//        String temp = String(y[0]) + String(y[1]);
//        String humid = String(y[2]) + String(y[3]);
//        // String gas = y.substring(4);
//        String gas = String(y[4]) + String(y[5]+ String(y[6]));
//        temperature = temp.toInt();
//        humidity = humid.toInt();
//        gasvalue = gas.toInt();
//        Serial.print(temperature);
//        Serial.print(humidity);
//        Serial.println(gasvalue);
//    }
//}

void ReadSerial()
{
  temperature = 25;
  humidity = 88;
  gasvalue = 140;
}

void ReadDataAll()
{
  if (SUART.available())
  {
    String FullData = "";
    for (int i = 0; i < 4; i++)
    {
      char TempData = SUART.read();
      FullData += TempData;
    }
    Serial.print(FullData);
  }
}
