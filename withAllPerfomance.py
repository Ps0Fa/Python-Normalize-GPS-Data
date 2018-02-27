import getpass
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import time
#import numpy as np
tic = time.clock()

importedCSVName = 'DATALOG.csv'
exportedCSVName = 'RaceRender_ViewSC.csv'
mainPath = 'C://Users//' + getpass.getuser() + '//Desktop//'
arduinoData = pd.read_csv(mainPath + importedCSVName,header=None)

#igx	igy	igz	iax	iay	iaz	gpsSats	gpsHour	gpsMinute	gpsSeconds	gpsMilliseconds	gpsAlt	gclat	gclon	sound	ksound	trackp	UpORDown	positionOnTrack	prevpositionOnTrack	lapTime	startLapTime	lapcounterD	lapcounterU	lapCounterDown	lapCounterUp	currentLap	myLaptiming
arduinoData.columns = ['igx','igy','igz','iax','iay','iaz','gpsSats','gpsHour','gpsMinute','gpsSeconds','gpsMilliseconds','gpsAlt','gclat','gclon','sound','ksound','trackp','UpORDown','positionOnTrack','prevpositionOnTrack','lapTime','startLapTime','lapcounterD','lapcounterU','lapCounterDown','lapCounterUp','currentLap','myLaptiming']

mySessions = []
for x in range(0,len(arduinoData)):
	if (arduinoData['igx'][x] == 'NewSession'):
		mySessions.append(x)

SessionsDf = []
if (len(mySessions) > 1):
	for x in range(1, len(mySessions)):
		currentDf = arduinoData[mySessions[x-1]+1:mySessions[x]]
		currentDf = currentDf.reset_index()
		del currentDf['index']
		SessionsDf.append(currentDf)
	currentDf = arduinoData[mySessions[x]+1:len(arduinoData)]
	currentDf = currentDf.reset_index()
	del currentDf['index']
	SessionsDf.append(currentDf)
else:
	currentDf = arduinoData[1:len(arduinoData)]
	currentDf = currentDf.reset_index()
	del currentDf['index']
	SessionsDf.append(currentDf)
		
SessionToExport = 1 #Select Session To Export for RaceRender, Starts From Zero

#Import Lattitude and Longitude
runTime = [0]
flat = [ SessionsDf[SessionToExport]['gclat'][0] ]
flon = [ SessionsDf[SessionToExport]['gclon'][0] ]
laptime = [0]
altitude = [0]
upOrDown = ['NA']
lapsum = [0]

#Normalized seconds
currentDif = [int(round((j-i)/100)) for i,j in zip(SessionsDf[SessionToExport]['gpsMilliseconds'], SessionsDf[SessionToExport]['gpsMilliseconds'][1:])]
currentDif = [10+x if x < 0 else x for x in currentDif]

#Normalized Lattitude and Longitude
currentIndex = 0
for x in range(1, len(SessionsDf[SessionToExport]) - 1):
	if (currentDif[x-1] > 1):
		latDif = SessionsDf[SessionToExport]['gclat'][x] - SessionsDf[SessionToExport]['gclat'][x-1]
		lonDif = SessionsDf[SessionToExport]['gclon'][x] - SessionsDf[SessionToExport]['gclon'][x-1]
		laptimeDif = SessionsDf[SessionToExport]['lapTime'][x] - SessionsDf[SessionToExport]['lapTime'][x-1]
		for j in range(0,currentDif[x-1]):
			currentIndex = currentIndex + 1
			runTime.append(runTime[currentIndex-1] + 0.1)
			flat.append(latDif / currentDif[x-1] + flat[currentIndex - 1])
			flon.append(lonDif / currentDif[x-1] + flon[currentIndex - 1])
			laptime.append(SessionsDf[SessionToExport]['lapTime'][x])
			altitude.append(SessionsDf[SessionToExport]['gpsAlt'][x])
			upOrDown.append(SessionsDf[SessionToExport]['UpORDown'][x])
			lapsum.append(SessionsDf[SessionToExport]['lapCounterDown'][x]+SessionsDf[SessionToExport]['lapCounterUp'][x])
	elif (currentDif[x-1] == 1):
		currentIndex = currentIndex + 1
		runTime.append(runTime[currentIndex-1] + 0.1)
		flat.append(SessionsDf[SessionToExport]['gclat'][x])
		flon.append(SessionsDf[SessionToExport]['gclon'][x])
		laptime.append(SessionsDf[SessionToExport]['lapTime'][x]/1000)
		altitude.append(SessionsDf[SessionToExport]['gpsAlt'][x])
		upOrDown.append(SessionsDf[SessionToExport]['UpORDown'][x])
		lapsum.append(SessionsDf[SessionToExport]['lapCounterDown'][x]+SessionsDf[SessionToExport]['lapCounterUp'][x])

lattitude = []
longitude = []
for x in range(0,5):
	lattitude.append(flat[x])
	longitude.append(flon[x])
for x in range(5, len(flat) - 5):
	lattitude.append(flat[x-2] * 0.15 + flat[x-1] * 0.2 + flat[x] * 0.3 + flat[x+1] * 0.2 + flat[x+2] * 0.15)
	longitude.append(flon[x-2] * 0.15 + flon[x-1] * 0.2 + flon[x] * 0.3 + flon[x+1] * 0.2 + flon[x+2] * 0.15)
for x in range(len(flat) - 5,len(flat)):
	lattitude.append(flat[x])
	longitude.append(flon[x])

for j in range(1,6):
	for x in range(2,len(lattitude) - 2):
		lattitude[x] = lattitude[x-2] * 0.15 + lattitude[x-1] * 0.2 + lattitude[x] * 0.3 + lattitude[x+1] * 0.2 + lattitude[x+2] * 0.15
		longitude[x] = longitude[x-2] * 0.15 + longitude[x-1] * 0.2 + longitude[x] * 0.3 + longitude[x+1] * 0.2 + longitude[x+2] * 0.15

for j in range(1,5):
	for x in range(2,len(lattitude) - 2):
		lattitude[x] = lattitude[x-1] * 0.3 + lattitude[x] * 0.4 + lattitude[x+1] * 0.3
		longitude[x] = longitude[x-1] * 0.3 + longitude[x] * 0.4 + longitude[x+1] * 0.3
		
for j in range(1,10):
	for x in range(2,len(lattitude) - 2):
		lattitude[x] = lattitude[x-1] * 0.1 + lattitude[x] * 0.8 + lattitude[x+1] * 0.1
		longitude[x] = longitude[x-1] * 0.1 + longitude[x] * 0.8 + longitude[x+1] * 0.1

#End normalization of lattitude, longitude

#Distance Traveled on 0.1 sec
myMeters =[0]
for x in range (1, len(lattitude)):
	lat1=lattitude[x]
	lon1=longitude[x]
	lat2=lattitude[x-1]
	lon2=longitude[x-1]
	R = 6378.137
	dLat = lat2 * 3.14159 / 180 - lat1 * 3.14159 / 180
	dLon = lon2 * 3.14159 / 180 - lon1 * 3.14159 / 180
	a = m.sin(dLat/2) * m.sin(dLat/2) + m.cos(lat1 * 3.14159 / 180) * m.cos(lat2 * 3.14159 / 180) * m.sin(dLon/2) * m.sin(dLon/2)
	c = 2 * m.atan2(m.sqrt(a), m.sqrt(1-a))
	d = R * c * 1000
	myMeters.append(d)

#velocity km/h
velocity =[]
for x in range (0, len(myMeters)):
	velocity.append(myMeters[x] * (10*3600/1000)) #to prwto 10 to kanw ta milliseconds mou

#normalize velocity
for x in range (2, len(velocity)-2):
	velocity[x] = velocity[x-2] * 0.1 + velocity[x-1] * 0.2 + velocity[x] * 0.4 + velocity[x+1] * 0.2 + velocity[x+2] * 0.1

#AccelerationG
gx = [0]
for x in range (1, len(velocity)):
	gx.append( (velocity[x] - velocity[x-1]) / (0.1*36) )

for j in range (0, 10):
	for x in range (2, len(gx)-2):
		gx[x] = gx[x-2] * 0.1 + gx[x-1] * 0.2 + gx[x] * 0.4 + gx[x+1] * 0.2 + gx[x+2] * 0.1

#Turn Angle
turnAngle =[]
for x in range (0,5):
	turnAngle.append(0)

for x in range (5, len(velocity)-5):
	turnAngle.append( -( m.atan2(lattitude[x] - lattitude[x-5], longitude[x] - longitude[x-5]) - m.atan2(lattitude[x+5] - lattitude[x-5], longitude[x+5] - longitude[x-5]) ) )

for x in range (0,5):
	turnAngle.append(0)
	
for x in range(0,len(turnAngle)):
	if ( abs(turnAngle[x]) > 1):
		turnAngle[x] = turnAngle[x-1]

#gy			 
gy = []
for x in range(0,len(turnAngle)):
	gy.append(turnAngle[x]* (velocity[x])/10)

for j in range (0, 5):
	for x in range (2, len(gx)-2):
		gy[x] = gy[x-2] * 0.1 + gy[x-1] * 0.2 + gy[x] * 0.4 + gy[x+1] * 0.2 + gy[x+2] * 0.1

#leanAngle
LeanAngle = []
for x in range(0,len(gy)):
	LeanAngle.append(-m.atan2(gy[x],1) * 180 / 3.14159)
	
for x in range(5,len(velocity)-10):
	if (velocity[x-5] < 5 and velocity[x-4] < 5 and velocity[x-3] < 5 and velocity[x-2] < 5 and velocity[x-1] < 5 and velocity[x+9] < 5 and velocity[x+10] < 5):
		velocity[x] = 0
		gx[x] = 0
		gy[x] = 0
		LeanAngle[x] = 0

#plt.plot(velocity)

alpha = []
for x in range(0, len(gy)):
	alpha.append(1 - (abs(gy[x])+abs(gx[x]))/2)

#PerformanceData
km060 = [0];km0100 = [0];km0160 = [0];km0200 = [0];km0230 = [0];km0300 = [0];m060 = [0];m0100 = [0];m0160 = [0];m0200 = [0];m0230 = [0];m0300 = [0];dm400 = [0]
dm1000 = [0];vm400 = [0];vm1000 = [0];km2000 = [0];km1600 = [0];km1000 = [0];km600 = [0];m2000 = [0];m1600 = [0];m1000 = [0];m600 = [0]

for x in range(1, len(velocity)):
	km060.append(0), km0100.append(0), km0160.append(0), km0200.append(0), km0230.append(0), km0300.append(0), m060.append(0), m0100.append(0), m0160.append(0), m0200.append(0), m0230.append(0), m0300.append(0), dm400.append(0), dm1000.append(0), vm400.append(0), vm1000.append(0), km2000.append(0), km1600.append(0), km1000.append(0), km600.append(0), m2000.append(0), m1600.append(0), m1000.append(0), m600.append(0)

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 100):
			while(velocity[x+swcounter] < 100 and swcounter < len(velocity) - 6 - x):
				km0100[x-1] = 0.1
				m0100[x-1] = myMeters[x+swcounter]
				km0100[x+swcounter] = km0100[x+swcounter-1] + 0.1
				m0100[x+swcounter] = m0100[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km0100[x+swcounter] = km0100[x+swcounter-1] + 0.1
			m0100[x+swcounter] = m0100[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 60):
			while(velocity[x+swcounter] < 60 and swcounter < len(velocity) - 6 - x):
				km060[x-1] = 0.1
				m060[x-1] = myMeters[x+swcounter]
				km060[x+swcounter] = km060[x+swcounter-1] + 0.1
				m060[x+swcounter] = m060[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km060[x+swcounter] = km060[x+swcounter-1] + 0.1
			m060[x+swcounter] = m060[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 160):
			while(velocity[x+swcounter] < 160 and swcounter < len(velocity) - 6 - x):
				km0160[x-1] = 0.1
				m0160[x-1] = myMeters[x+swcounter]
				km0160[x+swcounter] = km0160[x+swcounter-1] + 0.1
				m0160[x+swcounter] = m0160[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km0160[x+swcounter] = km0160[x+swcounter-1] + 0.1
			m0160[x+swcounter] = m0160[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 200):
			while(velocity[x+swcounter] < 200 and swcounter < len(velocity) - 6 - x):
				km0200[x-1] = 0.1
				m0200[x-1] = myMeters[x+swcounter]
				km0200[x+swcounter] = km0200[x+swcounter-1] + 0.1
				m0200[x+swcounter] = m0200[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km0200[x+swcounter] = km0200[x+swcounter-1] + 0.1
			m0200[x+swcounter] = m0200[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 230):
			while(velocity[x+swcounter] < 230 and swcounter < len(velocity) - 6 - x):
				km0230[x-1] = 0.1
				m0230[x-1] = myMeters[x+swcounter]
				km0230[x+swcounter] = km0230[x+swcounter-1] + 0.1
				m0230[x+swcounter] = m0230[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km0230[x+swcounter] = km0230[x+swcounter-1] + 0.1
			m0230[x+swcounter] = m0230[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 300):
			while(velocity[x+swcounter] < 300 and swcounter < len(velocity) - 6 - x):
				km0300[x-1] = 0.1
				vm400[x-1] = velocity[x+swcounter]
				km0300[x+swcounter] = km0300[x+swcounter-1] + 0.1
				vm400[x+swcounter] = velocity[x+swcounter]
				swcounter = swcounter + 1
			km0300[x+swcounter] = km0300[x+swcounter-1] + 0.1
			vm400[x+swcounter] = velocity[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			coruptData = coruptData + myMeters[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 400):
			while(performanceCounter < 400 and swcounter < len(velocity) - 6 - x):
				performanceCounter = performanceCounter + myMeters[x+swcounter]
				dm400[x-1] = 0.1
				vm400[x-1] = velocity[x-1]
				dm400[x+swcounter] = dm400[x+swcounter-1] + 0.1
				vm400[x+swcounter] = velocity[x+swcounter]
				swcounter = swcounter + 1
			dm400[x+swcounter] = dm400[x+swcounter-1] + 0.1
			vm400[x+swcounter] = velocity[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] < 5 and velocity[x] > 5):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			coruptData = coruptData + myMeters[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData > 1000):
			while(performanceCounter < 1000 and swcounter < len(velocity) - 6 - x):
				performanceCounter = performanceCounter + myMeters[x+swcounter]
				dm400[x-1] = 0.1
				vm400[x-1] = velocity[x-1]
				dm400[x+swcounter] = dm400[x+swcounter-1] + 0.1
				vm400[x+swcounter] = velocity[x+swcounter]
				swcounter = swcounter + 1
			dm400[x+swcounter] = dm400[x+swcounter-1] + 0.1
			vm400[x+swcounter] = velocity[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] > 100 and velocity[x] < 100):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData < 100):
			while(velocity[x+swcounter] > 5 and swcounter < len(velocity) - 6 - x):
				km1000[x-1] = 0.1
				m1000[x-1] = myMeters[x+swcounter]
				km1000[x+swcounter] = km1000[x+swcounter-1] + 0.1
				m1000[x+swcounter] = m1000[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km1000[x+swcounter] = km1000[x+swcounter-1] + 0.1
			m1000[x+swcounter] = m1000[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] > 60 and velocity[x] < 60):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData < 60):
			while(velocity[x+swcounter] > 5 and swcounter < len(velocity) - 6 - x):
				km600[x-1] = 0.1
				m600[x-1] = myMeters[x+swcounter]
				km600[x+swcounter] = km600[x+swcounter-1] + 0.1
				m600[x+swcounter] = m600[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km600[x+swcounter] = km600[x+swcounter-1] + 0.1
			m600[x+swcounter] = m600[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] > 200 and velocity[x] < 200):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData < 200):
			while(velocity[x+swcounter] > 5 and swcounter < len(velocity) - 6 - x):
				km2000[x-1] = 0.1
				m2000[x-1] = myMeters[x+swcounter]
				km2000[x+swcounter] = km2000[x+swcounter-1] + 0.1
				m2000[x+swcounter] = m2000[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km2000[x+swcounter] = km2000[x+swcounter-1] + 0.1
			m2000[x+swcounter] = m2000[x+swcounter-1] + myMeters[x+swcounter]

for x in range(3,len(velocity) - 3):
	performanceCounter = 0
	wcounter = 0
	swcounter = 0
	coruptData = 0
	if (velocity[x-1] > 160 and velocity[x] < 160):
		while(velocity[x+wcounter] > 5 and wcounter < len(velocity) - 6 - x):
			if (coruptData < velocity[x+wcounter]):
				coruptData = velocity[x+wcounter]
			wcounter = wcounter + 1
		if (coruptData < 160):
			while(velocity[x+swcounter] > 5 and swcounter < len(velocity) - 6 - x):
				km1600[x-1] = 0.1
				m1600[x-1] = myMeters[x+swcounter]
				km1600[x+swcounter] = km1600[x+swcounter-1] + 0.1
				m1600[x+swcounter] = m1600[x+swcounter-1] + myMeters[x+swcounter]
				swcounter = swcounter + 1
			km1600[x+swcounter] = km1600[x+swcounter-1] + 0.1
			m1600[x+swcounter] = m1600[x+swcounter-1] + myMeters[x+swcounter]

for x in range(1,len(velocity)):
	if (km060[x]==0):
		km060[x] = km060[x-1]
	if (km0100[x]==0):
		km0100[x] = km0100[x-1]
	if (km0160[x]==0):
		km0160[x] = km0160[x-1]
	if (km0200[x]==0):
		km0200[x] = km0200[x-1]
	if (km0230[x]==0):
		km0230[x] = km0230[x-1]
	if (km0300[x]==0):
		km0300[x] = km0300[x-1]
	if (m060[x]==0):
		m060[x] = m060[x-1]
	if (m0100[x]==0):
		m0100[x] = m0100[x-1]
	if (m0160[x]==0):
		m0160[x] = m0160[x-1]
	if (m0200[x]==0):
		m0200[x] = m0200[x-1]
	if (m0230[x]==0):
		m0230[x] = m0230[x-1]
	if (m0300[x]==0):
		m0300[x] = m0300[x-1]
	if (dm400[x]==0):
		dm400[x] = dm400[x-1]
	if (dm1000[x]==0):
		dm1000[x] = dm1000[x-1]
	if (vm400[x]==0):
		vm400[x] = vm400[x-1]
	if (vm1000[x]==0):
		vm1000[x] = vm1000[x-1]
	if (km2000[x]==0):
		km2000[x] = km2000[x-1]
	if (km1600[x]==0):
		km1600[x] = km1600[x-1]
	if (km1000[x]==0):
		km1000[x] = km1000[x-1]
	if (km600[x]==0):
		km600[x] = km600[x-1]
	if (m2000[x]==0):
		m2000[x] = m2000[x-1]
	if (m1600[x]==0):
		m1600[x] = m1600[x-1]
	if (m1000[x]==0):
		m1000[x] = m1000[x-1]
	if (m600[x]==0):
		m600[x] = m600[x-1]



#DataFrame To RaceRender
dataFrameToPrint = pd.DataFrame(
	{'Time': runTime,
		'speed': velocity,
		'laptime': laptime,
		'lattitude': lattitude,
		'longitude': longitude,
		'Altitude': altitude,
		'WhatRound': upOrDown,
		'currentLap': lapsum,
		'LeanAngle': LeanAngle,
		'alpha': alpha,
		'gpsX': gx,
		'gpsY': gy,
		'km060': km060,
		'km0100': km0100,
		'km0160': km0160,
		'km0200': km0200,
		'km0230': km0230,
		'km0300': km0300,
		'm060': m060,
		'm0100': m0100,
		'm0160': m0160,
		'm0200': m0200,
		'm0230': m0230,
		'm0300': m0300,
		'dm400': dm400,
		'dm1000': dm1000,
		'vm400': vm400,
		'vm1000': vm1000,
		'km2000': km2000,
		'km1600': km1600,
		'km1000': km1000,
		'km600': km600,
		'm2000': m2000,
		'm1600': m1600,
		'm1000': m1000,
		'm600': m600
	})

dataFrameToPrint.to_csv(mainPath+exportedCSVName, index=False, header=True)
#SyncVid 2.6

toc = time.clock()
print(toc - tic)