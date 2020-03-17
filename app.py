import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledYlw = 19
ledYlwSts = 0
ledYlwStsTxt = ""

GPIO.setup(ledYlw, GPIO.OUT)
GPIO.output(ledYlw, GPIO.LOW)

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4);

#-----------------------------------------
@app.route("/")
def index():

	# Read Sensors Status
	ledYlwSts = GPIO.input(ledYlw)

	templateData = {
		'title' : 'GPIO output Status!',
		'ledYlw'  : ledYlwSts,
		'temp'  : temperature,
        }
	return render_template('index.html', **templateData)
#-----------------------------------
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
	ledYlwSts = GPIO.input(ledYlw)


	templateData = {
		'ledYlw'  : ledYlwSts,
	}
	return render_template('index.html', **templateData)
#----------------------------------------------
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
