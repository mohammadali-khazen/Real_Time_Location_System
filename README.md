# Tracking Workers and Objects in Construction Sites through Bluetooth Low Energy Technology
Here are codes and datasets of a Real-time Localization System (RTLS) through Bluetooth Low Energy Technology.
The main goal of the developed system is to track workers and objects in construction sites by considering various aspects affecting the RTLS applicability in the construction domain, including portability, affordability, scalability, and high positioning accuracy. In the proposed RTLS, the beacons replaced the commonly used receivers for the first time in localization that makes the system independent from wiring work and DC power supply, resulting in substantiality increasing the system's applicability on-site.

For this purpose, the beacons’ configurations are tuned, and a record correction algorithm is developed to solve the shortage of BLE packets limited payload that the receiver relies on to broadcast the location data to the gateway. Besides, a modular system infrastructure placement plan is proposed based on the effective devices' range to minimize the number of required devices on-site and improve the localization accuracy. The proposed localization estimation model leverages the placement strategy to categorize the records based on the estimated distances and the transmitter's position and finally localize them based on a developed technique for each category.

## Real-time Localization System (RTLS)
The following modules consist of the proposed RTLS

  
The Excel file from Elasticsearch should be uploaded in the "Data Pre-Processing" module.

Requirement 2) The CSV files of the RSSI-distance relationship of the different orientations of the transmitter with respect to the receiver should be uploaded in (distance (Trx)\ Random Forest mode\ Training) of the "RSSI-distance Prediction" module.

### Module 1 (Data Pre-Processing)
Firstly, this module is meant to pre-process the raw dataset coming from Elasticsearch in order for the raw dataset to be in a suitable format for localization. Secondly, the (x,y) coordinates of the fixed transmitter on-site replace the IDs of the transmitters. Finally, a Semi-Logical record to Logical record converter Model is used to increase the ratio of the Logical records to improve the accuracy of the system.

### Module 2 (RSSI-distance Prediction through a Machine Learning Model)
In this module, the distance between the trasnmiiting and receiveing beacons is estimated through the Recieved Signal Strength Identity (RSSI). Random Forest (RF) is deployed for the RSSI-distance prediction model. To train the model,

### Module 3 (Localization through a Combination of Triangulation and Min-Max Techniques)

### Module 4 (Estimated Locations Post-Processing)

