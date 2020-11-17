# ctf_tesla_logs

Post mortem teardown of Tesla CAN traffic from DEFCON28 Virtual Car Hacking Village.

https://www.carhackingvillage.com/

# Usage

## Data Smuggling

The ctf/lab setup was [CHVpi](https://github.com/will-caruana/CHVpi) running on RaspberryPi. Socketcan devices were setup and they were connected to a Tesla Model3.

This particular machine did have access to git & outside world.

1. Create git repo somewhere.
2. Copy the chvpi ssh-key to your account.
  Disclaimer: This is a huge security issue as it gives the owner of the CHVpi access to your Git repo.
  Solution: Use a throw away GitHubAccount.
3. Run `00_log.sh`. Every 10000 CAN messages it will `bzip2` the log, add it to git and push.

## Data analysis.

1. `./01_unpack.sh` unpacks all `*.log.bz2` files into `final_log`.
2. [opt] `./02_uniqueids.sh` will dump all of the unique CAN ID's found in `final_log`. It was a quick script during CTF time to peek at the messaging.
3. [01_PostMortem_Local.ipynb](01_PostMortem_Local.ipynb) - Local analysis of the log files directly parsing the `final_log` output.
4.

# Scaleable Cloud Based Analytic Solution for the Modern Era(tm).

Based on [dask-docker][https://github.com/dask/dask-docker]

`
cd dask-docker/
docker-compose up
`

1. Copy and paste the `http://127.0.0.1:8888/` URL into your browser.
2. Control-click on the URL depending on your terminal emulator.

## Data Collection Methodology.

This was our first CTF event and weren't sure what to expect or do. We ignored the set CTF goals and instead opted for bulk data collection with the intention of leaving the Prüfstand and going back to the desk for the actual work. This way the next time we're in the test cell,

This development style worked for our team while assisting [Caterpillar M46](https://www.cat.com/en_US/products/new/power-systems/marine-power-systems/commercial-propulsion-engines/18547528.html) development and [Caterpillar 795F AC](https://www.cat.com/en_US/products/new/equipment/off-highway-trucks/mining-trucks/18232553.html) dSpace HIL testing.

## Team Experience:

Industry experience in developing for heavy equipment, automotive, and aerospace.

Usual tools & chain: Simulink Embedded Coder, diab, Vector CANape, Vector CANalyzer. MDF

# Sponsored By: ![](https://www.csselectronics.com/script/getLogoImage/id/klikthis:LogoImage:sm011685180628698/logo.png)

> [CSS Electronics](https://www.csselectronics.com/screen/page/can-bus-logger-about) is a developer of professional-grade, simple-to-use and low cost CAN bus data loggers. We're based in Denmark and operate globally:

> - We supply 1,000+ companies across 80+ countries
> - Applications include telematics, development & diagnostics
> - Industries include automotive, heavy duty, motorsports, & production
> - Users include OEM engineers, operators, site managers & researchers
> - Assembly is done by ISO 9001:2015 certified US partners - scaling to any volume
> - We offset 100% of our CO2 footprint

![](https://s3-eu-west-1.amazonaws.com/images.smoolis.com/c408510c-077d-4269-bd67-0f6c55129510/CANedge2-CAN-Bus-Data-Logger-WiFi-Telematics.jpg)

>> [CANedge2: 2x CAN Bus Data Logger (SD + WiFi)](https://www.csselectronics.com/screen/product/can-lin-logger-wifi-canedge2/language/en#void)

> The plug & play 2xCAN/LIN logger records timestamped CAN data (Classical/CAN FD) to the extractable 8 GB industrial SD card.

> The small device connects via WiFi access points (e.g. WLAN or 3G/4G routers) to securely push data to your server. Further, the device can be updated over-the-air.

> The CANedge2 is ideal for telematics & fleet management - as well as R&D field tests, diagnostics and predictive maintenance.

> Software/APIs are free & open source - with no subscription fees or vendor lock-in.

>> [Secure CAN Bus Logging & Telematics - A Simple Intro](https://www.csselectronics.com/screen/page/secure-can-bus-logging-telematics-intro)

> 9 security factors to review in your CAN logging setup

> 1. Is the manufacturing process secure?
> 2. Does the logger enable code protection?
> 3. Is the firmware digitally signed and updatable OTA?
> 4. Can passwords be encrypted & rotated as per NIST guidelines?
> 5. Can SD data be encrypted as per NIST guidelines?
> 6. Is data uploaded securely as per NIST guidelines?
> 7. Can server access be monitored and controlled?
> 8. Are security critical data unique for each device/purpose?
> 9. Can TLS certificates be updated over-the-air?


## Reverse Engineering Case Studies

![](https://canlogger1000.csselectronics.com/img/cases/use-cases/Louter-Control-Logo-Use-Case.jpg)

[Louter Control. Control Systems / Netherlands - *Remote reverse engineering of machinery *Louter Control. Control Systems / Netherlands.*](https://www.csselectronics.com/screen/page/can-logger-use-case-study-examples#louter-control-case-wifi-reverse-engineering)

![](https://canlogger1000.csselectronics.com/img/cases/use-cases/Albach-Use-Case-Logo_v3.png)

[Albach Maschinenbau. Self Propelled Mobile Tree Fellers / ~100 FTEs / Germany - *Optimizing systems in mobile foresters*](https://www.csselectronics.com/screen/page/can-logger-use-case-study-examples#albach-case-mobile-forester)
