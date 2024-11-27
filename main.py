import requests
from datetime import datetime
import smtplib
from requests.exceptions import ConnectionError, Timeout
import time

MY_EMAIL = "golesanket491@gmail.com"
MY_PASSWORD = "xstxvsmotvtrnoyd"
MY_LAT = 16.7140
 # Your latitude
MY_LONG =74.4882



 # Your longitude


def is_iss_overhead():
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])
        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True
    except (ConnectionError, Timeout) as e:
        print(f"Error connecting to {url}: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(15)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com",port=587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up\n\nThe ISS is above you in the sky."
        )


