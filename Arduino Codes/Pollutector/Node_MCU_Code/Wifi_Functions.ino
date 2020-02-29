void InitWiFi()
{
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(200);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

// void InitWiFiSilent()
// {
//     delay(10);
//     WiFi.begin(ssid, password);

//     while (WiFi.status() != WL_CONNECTED)
//     {
//         delay(20);
//     }

//     randomSeed(micros());

//     Serial.println("WiFi connected");
// }

void UpdateBuffer()
{
    StaticJsonBuffer<300> JSONbuffer;
    JsonObject &JSONencoder = JSONbuffer.createObject();

    JSONencoder["GasSensorValue"] = String(gasvalue);
    JSONencoder["Temperature"] = String(temperature);
    JSONencoder["Humidity"] = String(humidity);
    

     
    JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    Serial.println("Sending message to MQTT topic..");
    Serial.println(JSONencoder.measureLength());
    Serial.println(JSONmessageBuffer);
}