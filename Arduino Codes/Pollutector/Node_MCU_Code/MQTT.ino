// Basic mqtt protocol setup
void InitClient()
{
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
}

void reconnect()
{
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str()))
    {
      Serial.println("connected");
      client.publish("ENTC/Wifi_Outgoing", "Welcome to ENTC WiFi Analyzer | Portal");
      client.subscribe("ENTC/Wifi_incoming");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      delay(1000);
    }
  }
}

void ReconnectSilent()
{
  while (!client.connected())
  {
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str()))
    {
      // Serial.println("connected");
      // client.publish("ENTC/Wifi_Outgoing", "Welcome to ENTC WiFi Analyzer | Portal");
      // client.subscribe("ENTC/Wifi_incoming");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      delay(1000);
    }
  }
}