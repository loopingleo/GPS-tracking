# -*- coding: utf-8 -*-
# @Author: loopingleo
# @Date:   2018-08-30
# @Last Modified by:   loopingleo
# @Last Modified time:


# IDEATION

# load data
# select data
# take a look
# processing



import gpxpy.parser as parser
import os, glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import gmplot
import folium
import mplleaflet
import numpy as np



## --------- READ multiple files with sensorLog data -------------------------------------------------------


path = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/SensorLogData/Kyoto")
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []

for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)

df_sensorData = pd.concat(list_, sort=True)


#frame.info()


## --------- READ sensorLog data -------------------------------------------------------

#df_sensorData = pd.read_csv(os.path.expanduser("~/Dropbox/04_Golf Analytics/SensorLog data/my_iOS_device_2018-02-15_20-55-33_+0100.csv"), sep=",")
df_sensorData.info()



df_compressed = df_sensorData[["loggingTime(txt)",
                               "locationTimestamp_since1970(s)",
                               "loggingSample(N)",
                               "locationLatitude(WGS84)",
                               "locationLongitude(WGS84)",
                               "locationAltitude(m)",
                               "locationSpeed(m/s)",
                               "accelerometerTimestamp_sinceReboot(s)",
                               "accelerometerAccelerationX(G)",
                               "accelerometerAccelerationY(G)",
                               "accelerometerAccelerationZ(G)",
                               "gyroRotationX(rad/s)",
                               "gyroRotationY(rad/s)",
                               "gyroRotationZ(rad/s)"
                               ]]

df_compressed = df_compressed.rename(index=str, columns={"loggingTime(txt)":"time",
                               "locationTimestamp_since1970(s)":"time_s1970",
                               "loggingSample(N)":"sample_ind",
                               "locationLatitude(WGS84)":"lat",
                               "locationLongitude(WGS84)":"lon",
                               "locationAltitude(m)":"altitude",
                               "locationSpeed(m/s)":"speed",
                               "accelerometerTimestamp_sinceReboot(s)":"accel_time",
                               "accelerometerAccelerationX(G)":"x",
                               "accelerometerAccelerationY(G)":"y",
                               "accelerometerAccelerationZ(G)":"z",
                               "gyroRotationX(rad/s)":"Xgyro",
                               "gyroRotationY(rad/s)":"Ygyro",
                               "gyroRotationZ(rad/s)":"Zgyro"
})
#df_compressed = df_compressed[:760]


df_compressed["Xgyro_pctChg"] = df_compressed["Xgyro"].pct_change(periods=1)
df_compressed["Ygyro_pctChg"] = df_compressed["Ygyro"].pct_change(periods=1)
df_compressed["Zgyro_pctChg"] = df_compressed["Zgyro"].pct_change(periods=1)

df_compressed["Xgyro_pctChg_rolling"] = df_compressed["Xgyro_pctChg"].rolling(window=3, min_periods=1).mean()
df_compressed["Ygyro_pctChg_rolling"] = df_compressed["Ygyro_pctChg"].rolling(window=3, min_periods=1).mean()
df_compressed["Zgyro_pctChg_rolling"] = df_compressed["Zgyro_pctChg"].rolling(window=3, min_periods=1).mean()

df_compressed["XYZgyro"] = df_compressed["Xgyro_pctChg_rolling"]*df_compressed["Ygyro_pctChg_rolling"]*\
                        df_compressed["Zgyro_pctChg_rolling"]



df_compressed["x_pctChg"] = df_compressed["x"].pct_change(periods=1)
df_compressed["y_pctChg"] = df_compressed["y"].pct_change(periods=1)
df_compressed["z_pctChg"] = df_compressed["z"].pct_change(periods=1)

df_compressed["x_pctChg_rolling"] = df_compressed["x_pctChg"].rolling(window=3, min_periods=1).mean()
df_compressed["y_pctChg_rolling"] = df_compressed["y_pctChg"].rolling(window=3, min_periods=1).mean()
df_compressed["z_pctChg_rolling"] = df_compressed["z_pctChg"].rolling(window=3, min_periods=1).mean()

df_compressed["xyz"] = df_compressed["x_pctChg_rolling"]*df_compressed["y_pctChg_rolling"]*\
                        df_compressed["z_pctChg_rolling"]

df_compressed["xyz_absSum"] = abs(df_compressed["x"]) + abs(df_compressed["y"]) + abs(df_compressed["z"])

df_compressed["alt_pctChg"] = df_compressed["altitude"].pct_change(periods=1)
df_compressed["alt_pctChg_rolling"] = df_compressed["alt_pctChg"].rolling(window=3, min_periods=1).mean()

#
df_compressed.z.median()
df_compressed.z.plot()
df_compressed.x.plot()
df_compressed.y.plot()

#
plt.plot(df_compressed.sample_ind, df_compressed.x)
plt.plot(df_compressed.sample_ind, df_compressed.y)
plt.plot(df_compressed.sample_ind, df_compressed.z)

plt.plot(df_compressed.sample_ind, df_compressed.altitude)
plt.plot(df_compressed.sample_ind, df_compressed.alt_pctChg_rolling)
plt.plot(df_compressed.sample_ind, df_compressed.speed*3.6)

plt.plot(df_down.sample_ind, df_down.speed)


plt.plot(df_compressed.lon, df_compressed.lat)



plt.plot(df_compressed.sample_ind, df_compressed.Xgyro)
plt.plot(df_compressed.sample_ind, df_compressed.Ygyro)
plt.plot(df_compressed.sample_ind, df_compressed.Zgyro)

plt.plot(df_compressed.sample_ind, df_compressed.Xgyro_pctChg_rolling)
plt.plot(df_compressed.sample_ind, df_compressed.Ygyro_pctChg_rolling)
plt.plot(df_compressed.sample_ind, df_compressed.Zgyro_pctChg_rolling)

plt.plot(df_compressed.sample_ind, df_compressed.x_pctChg_rolling)
plt.plot(df_compressed.sample_ind, df_compressed.y_pctChg_rolling)
plt.plot(df_compressed.sample_ind, df_compressed.z_pctChg_rolling)

plt.plot(df_compressed.sample_ind, df_compressed.xyz)
plt.plot(df_compressed.sample_ind, df_compressed.XYZgyro)

plt.plot(df_compressed.sample_ind, df_compressed.xyz_absSum)

plt.yscale("log")
plt.ylim(-1, 1)


round(abs(df_compressed.xyz),5).describe()
sort(df_compressed.xyz)[0.95*length(df_compressed.xyz)]

df_compressed.sort_values(["xyz"]).reset_index()[round(0.95*len(df_compressed))]

df_down = df_compressed.where(df_compressed.alt_pctChg_rolling < 0.00001)
df_down = df_down.dropna()
(df_down.speed*3.6).describe()

#
# plt.plot(df_accel.x/df_accel.x[0])
#
# #median centering
# plt.plot(df_accel.y - df_accel.y.median())
#
# df_accel["x_mad"] = (df_accel.x - df_accel.x.median()).abs()
# df_accel["y_mad"] = (df_accel.y - df_accel.y.median()).abs()
# df_accel["z_mad"] = (df_accel.z - df_accel.z.median()).abs()
# df_accel.z_mad.plot()
#
# df_accel["mad_mltpl"] = (1 + df_accel.x_mad) * (1 + df_accel.y_mad) * (1 + df_accel.z_mad) -1
# df_accel.mad_mltpl.plot()
#





## ---------- PLOT ON MAP  ----------------------------

gmap = gmplot.GoogleMapPlotter(df_compressed.lat.mean(), df_compressed.lon.mean(), 14)

#plot map circles in different sizes and colors
for i in range(0,len(df_compressed)-1,20):
    #if abs(df_compressed.xyz[i]) < abs(df_compressed.XYZgyro).quantile(0.1):
    if abs(df_compressed.speed[i]) < 3/3.6:#abs(df_compressed.speed).quantile(0.03):
        gmap.circle(df_compressed['lat'][i], df_compressed['lon'][i],
                    #color=df_gpx["markCol2"][i],
                    color="#f44242",
                    marker=False,
                    #radius=10*(1-abs(round(df_compressed["speed"][i],4))**0.2),
                    radius= 20 * (df_compressed["speed"][i])**(2),
                    #radius = 0.2*(df_compressed["xyz_absSum"][i])**2, ## for gyromovements
                    #radius=5 / (df_compressed["xyz_absSum"][i]) ** 2,  ## for gyromovements
                    #radius = 400,
                    ew = 0.3,
                    face_alpha=0.8,
                    )

#gmap.scatter(df['Latitude'][0], df['Longitude'][0], size=0.5, marker=False)
#gmap.scatter(df['Latitude'], df['Longitude'], df["markColScale"][i], size=0.5, marker=False)
#gmap.marker(48.8,9.2)

#gmap.heatmap(df_compressed['lat'], df_compressed['lon'], threshold=5, radius=40)


gmap.draw("plots/2018-08-30a_all_sensorLog.html")  # saves to html file for display below - hm, see note below about this.

#TODO: draw polygon box around standing positions








locationlist = df_compressed[["lat","lon"]].dropna().values.tolist()
map = folium.Map(location=[np.mean(df_compressed['lat']), np.mean(df_compressed['lon'])], zoom_start=12)


for point in range(0, len(locationlist), 30):
    #if abs(df_compressed.speed[point]) < 0.1 / 3.6:  #
        folium.Circle(locationlist[point], radius=2,#/(1+ (df_compressed["speed"][point])**(4)),
                            color='#f44242', fill=True, fill_color ='#f44242', fill_opacity=0.2, stroke = True, weight = 0.1).add_to(map)

folium.TileLayer('cartodbdark_matter').add_to(map)
#folium.TileLayer('cartodbpositron').add_to(map)
#folium.TileLayer('Stamen Toner').add_to(map)


map

filepath = 'kyoto/index.html'
map.save(filepath)








gmap = gmplot.GoogleMapPlotter(df_compressed.lat.mean(), df_compressed.lon.mean(), 15)

#plot map circles in different sizes and colors
#for i in range(0,len(df_compressed)-1,1):
    #if abs(df_compressed.xyz[i]) < abs(df_compressed.XYZgyro).quantile(0.1):
gmap.plot(df_compressed['lat'], df_compressed['lon'],
                    #color=df_gpx["markCol2"][i],
                    color="black",
                    ew = 3)

#gmap.scatter(df['Latitude'][0], df['Longitude'][0], size=0.5, marker=False)
#gmap.scatter(df['Latitude'], df['Longitude'], df["markColScale"][i], size=0.5, marker=False)
#gmap.marker(48.8,9.2)


#gmap.heatmap(df_compressed['lat'], df_compressed['lon'], threshold=20, radius=20)
gmap.draw("plots/2018-02-15h_sensorLog_path.html")  # saves to html file for display below - hm, see note below about this.

#TODO: draw polygon box around standing positions




