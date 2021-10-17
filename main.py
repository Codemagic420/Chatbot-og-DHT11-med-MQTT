# Importere library til at forbinde til adafruit.io
import umqtt_robust2
from machine import Pin
import dht
from time import sleep_ms, sleep
lib = umqtt_robust2

sensor = dht.DHT11(Pin(14))
led = Pin(27, Pin.OUT)

while True:
    sleep_ms(500)
    besked = lib.besked
    # haandtere fejl i forbindelsen og hvor ofte den skal forbinde igen
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        # Det er primært herinde at i skal tilfoeje kode
        if besked == "Hej Bot":
            print("modtaget")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="Hej master")
            lib.besked = ""
        if besked == "fortæl en joke jarvis":
            print("modtaget")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="""Hvilke bogstaver kan flyve? Ænder :D""")
            lib.besked = ""
        if besked == "fortæl en joke mere jarvis":
            print("modtaget")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="""Hvorfor har blondiner altid en pistol med på indkøb? Så de kan skyde en genvej""")
            lib.besked = ""
        if besked == "hvad er temperaturen jarvis?":
            sleep(2)
            sensor.measure()
            temp = sensor.humidity()
            print("temp")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="temperaturen er "+str(temp * (9/5) + 32.0)+" F")
            lib.besked = ""
        if besked == "hvad er temperaturen jarvis?":
            sleep(2)
            sensor.measure()
            temp = sensor.temperature()
            print(temp)
            # Vi har sat den til 20C grader, da vi ikke kunne varme sensoren op til 30)
            if temp >20:
                for x in range(0, 5):
                    lib.c.publish(topic=lib.mqtt_pub_feedname, msg="det er for varmt")
            lib.besked = ""
        if besked == "hvad er temperaturen jarvis?":
            sleep(2)
            sensor.measure()
            temp = sensor.temperature()
            print(temp)
        # Vi har sat den til 30C grader, da vi ikke kunne justere på sensorens varmeinput)
            if temp <30:
                for x in range(0, 5):
                    lib.c.publish(topic=lib.mqtt_pub_feedname, msg="det er for koldt")
            lib.besked = ""
        if besked == "hvad er fugtigheden jarvis?":
            sleep(2)
            sensor.measure()
            hum = sensor.humidity()
            print("modtaget")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="fugtigheden er "+str(hum)+" %")
            lib.besked = ""
        if besked == "taend lys jarvis":
            sleep(2)
            led.value(not led.value())
            print("taender LED")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="taender LED")
            lib.besked = ""
        if besked == "sluk lys jarvis":
            sleep(2)
            led.value(led.value())
            print("sluk LED")
            lib.c.publish(topic=lib.mqtt_pub_feedname, msg="sluk LED")
            lib.besked = ""
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.client.disconnect()
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages
lib.c.disconnect()




