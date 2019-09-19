# UncannyIndex
Run Adafruit's Uncanny Eyes inside a Valve Index and use the cameras to look at anyone who comes near!

This project is a proof of concept, rather than a complete ready-to-use package. The script hard codes the USB camera and the COM port that the Teensy can be found on. 

To limit CPU usage, I am building an executable using pyinstaller and then using Windows CPU affinity to limit which cores run the program.
