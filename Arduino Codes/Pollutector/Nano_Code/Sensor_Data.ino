void ReadSensorData()
{
    dht11.read(&temperature, &humidity, NULL);    
    gassensorValue = analogRead(gas_sensor_pin); // read analog input pin 0 
    // Serial.println(sensorValue, DEC); // prints the value read
    //---show temp and humidity as integers on Serial moniotr
    Serial.print("Temperature = ");
    Serial.print((int)temperature);
    Serial.print(" degC");
    Serial.print("  "); //space
    Serial.print("Humidity = ");
    Serial.print((int)humidity);
    Serial.print(" %H");
    Serial.print("Gas = ");
    Serial.println((int)gassensorValue);
    
    String DataMessage = String(temperature) + String(humidity) + String(gassensorValue);

    SUART.print(DataMessage);
    delay(1000);
}
