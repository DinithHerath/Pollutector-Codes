#include "_def.h"
#include "_var.h"

void setup()
{
    InitSerialCommunication();
    InitWiFi();
    InitClient();
}

void loop()
{
    ReadSerial();
    UpdateBuffer();
    if (!client.connected())
    {
        ReconnectSilent();
    }
    client.loop();
    if (client.publish("pollutector/outgoing", JSONmessageBuffer) == true)
    {
        Serial.println("Success sending message");
    }
    else
    {
        Serial.println("Error sending message");
    }
    delay(1000);
}
