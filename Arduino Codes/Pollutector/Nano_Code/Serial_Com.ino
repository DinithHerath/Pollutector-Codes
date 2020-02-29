void InitSerialCommunication()
{
    Serial.begin(9600);
    SUART.begin(9600); //to match with NodeMCU which prefers higher Bd to work
}

void ReadSerial()
{
    if (SUART.available())
    {
        char message = SUART.read();
    }
}

void WaitforMain(char Text)
{
    while (1)
    {
        if (SUART.available())
        {
            char message = SUART.read();
            if (message == Text)
            {
                break;
            }
        }
    }
}