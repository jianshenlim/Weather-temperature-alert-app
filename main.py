import requests, json , winsound
import time
import threading
from datetime import datetime





class weatherAPP:

    # API key
    api_key = "c51fdc88f75f5957511081a28c59d723"
    # URL
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # Base city name
    city_name = "melbourne"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

    current_temperature = None
    feels_like_temperature = None
    min_temperature = None
    max_temperature = None
    current_pressure = None
    current_humidity = None
    weather_description = None

    alertTemp = None
    alertHumidity = None

    backgroundThread = None
    lastCheckedTime = None

    exitEvent = threading.Event()

    def callAPI(self):
        response = requests.get(self.complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            self.current_temperature = y["temp"]
            self.feels_like_temperature = y["feels_like"]
            self.min_temperature = y["temp_min"]
            self.max_temperature = y["temp_max"]
            self.current_pressure = y["pressure"]
            self.current_humidity = y["humidity"]
            z = x["weather"]
            self.weather_description = z[0]["description"]
        else:
            print("Error with API call")

    def printResults(self):
        print("Current Temperature = " +
              str(self.current_temperature) + '\u00b0' + "C" +
              "\n Temperature Range = " +
              str(self.min_temperature) + " - " + str(self.max_temperature) + '\u00b0' + "C" +
              "\n Feels like = " +
              str(self.feels_like_temperature) + '\u00b0' + "C" +
              "\n Atmospheric pressure = " +
              str(self.current_pressure) + "Pa" +
              "\n Humidity = " +
              str(self.current_humidity) + "%" +
              "\n Weather Description = " +
              str(self.weather_description))

    def setTempAlert(self):
        self.alertTemp = int(input("Enter Alert Temp ("+'\u00b0' + "C): "))

    def setHumidityAlert(self):
        self.alertHumidity = int(input("Enter Alert Humidity (%): "))

    def playAlert(self):
        duration = 500  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        winsound.Beep(freq, duration)
        winsound.Beep(freq, duration)

    def cycleReport(self,seconds):
        exceeded = False
        while True:
            self.callAPI()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.lastCheckedTime = current_time
            if (self.alertTemp is not None and self.current_temperature >= self.alertTemp):
                exceeded = True
            if (self.alertHumidity is not None and self.current_humidity >= self.alertHumidity):
                exceeded = True
            if exceeded:
                self.playAlert()
                print("Alert Triggered")
                print("Current Temp: " + str(self.current_temperature) + " Current Humidity: " + str(self.current_humidity))
                break
            if self.exitEvent.is_set():
                break
            time.sleep(seconds)



    def startMonitor(self):
        print("1: 15 Mins")
        print("2: 30 Mins")
        print("3: 60 Mins")
        userinput = int(input("Select Refresh Interval: "))

        if (userinput == 1):
            seconds = 900
        elif (userinput == 2):
            seconds = 1800
        elif (userinput == 3):
            seconds = 3600
        else:
            print("Non Valid Option")
            return
        if self.alertTemp is None and self.alertHumidity is None:
            print("No Alert Set")
        else:
            self.backgroundThread = threading.Thread(name='background',target=self.cycleReport,args=[seconds,])
            self.backgroundThread.start()

    def getLastChecked(self):
        if self.lastCheckedTime is None:
            print("Monitoring Not Started")
        else:
            print("Last Checked Time: "+self.lastCheckedTime)

    def stopMonitor(self):
        print("Alert Stopped")
        self.exitEvent.set()
        self.exitEvent = threading.Event()

def menu():
    print("\n1: Current Weather Report")
    print("2: Set Alert")
    print("3: Check Current Alerts")
    print("4: Start monitoring")
    print("5: Last Checked Time")
    print("6: Reset/Stop Monitoring")
    print("7: Exit\n")

def main():

    test = weatherAPP()
    running = True
    while (running):
        menu()
        userinput = int(input("Enter option: "))
        if (userinput == 1):
            test.callAPI()
            test.printResults()
        elif (userinput == 2):
            test.setTempAlert()
            test.setHumidityAlert()
        elif (userinput == 3):
            print("Temperature Alert: ", end='')
            print(test.alertTemp)
            print("Humidity Alert: ", end='')
            print(test.alertHumidity)
        elif (userinput == 4):
            test.startMonitor()
        elif (userinput == 5):
            test.getLastChecked()
        elif (userinput == 6):
            test.stopMonitor()
        elif (userinput == 7):
            test.stopMonitor()
            running = False
        else:
            continue


if __name__ == '__main__':
    main()

