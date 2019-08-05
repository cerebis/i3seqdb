from opentrons import robot,labware,instruments
import math

#################################
##Normalisation of gDNA#########
# Author: Kay Anantanawat
# The script is to create for OT-2 for normalisation of gDNA, so that all samples will have the same concentration of DNA.
# This protocol assumes that the volume of gDNA added into a plate are the same regardless of their concentration.
# Therefore, the amount of water added will be different to make the concentration of the sample the same.
# The list for volume and destination well can be created from the csv file, template_volume.csv.
# At the moment, the protocol doesn't import the csv file. I just used copy and paste from the file into the list.
# The protocol is tested 5/8/2019. 
# Change the list Vol, the dest_well, and the volume of gDNA transfer below. 
# I recommend that the dest_well is in order as it is easy to resume the protocol if you need to stop in the middle. 

Vol=[
18.4148174012499,
11.3547016119498,
18.5676873620165,
9.59169664385614,
10.6308313927433,
9.53740637741565,
18.9253363979534,
17.331393224477,
17.1789994941177,
4.41650080693718,
4.67890376139953,
8.36826072731572,
17.8914401835473,
16.3594069630294,
14.2554210232568,
5.34419764049917,
1.74961052565015,
2.33727884834805,
13.3877292210238,
15.3840870887301,
12.4557463137955,
5.53754718589248,
8.72257615040099,
20.6183354961633,
19.4287119385463,
8.97402580549377,
10.4127178661667,
7.67201187173685,
7.77725879176622,
11.982373288867,
16.1779631778204,
4.2698218414664,
8.54589466926573,
10.4960581874569,
8.44160021005111,
]

dest_well=[
	'A8',
'B8',
'C8',
'D8',
'E8',
'F8',
'G8',
'H8',
'A9',
'B9',
'C9',
'D9',
'E9',
'F9',
'G9',
'H9',
'A10',
'B10',
'C10',
'D10',
'E10',
'G10',
'H10',
'A11',
'B11',
'C11',
'D11',
'E11',
'F11',
'G11',
'H11',
'A12',
'B12',
'C12',
'D12',
	]

water_rack=labware.load('tube-rack-2ml','5')
gDNA_plate=labware.load('96-flat','2')
dest_plate=labware.load('96-flat','1')
water=water_rack.wells('A1')

tiprack_10 = [labware.load('tiprack-10ul', slot)
	for slot in ['6','7']]


p10=instruments.P10_Single(
	mount='right',
	tip_racks=tiprack_10)

p10.pick_up_tip()
p10.transfer(
	Vol,
	water,
	dest_plate.wells(dest_well),
	blow_out=True,
	new_tip='never'
	)
p10.drop_tip()

i=1

tiprack_10_2 = labware.load('tiprack-10ul','8')

p10_8 = instruments.P10_Multi(
	mount='left',
	max_volume=10,
	tip_racks=tiprack_10_2)

##Change the number 2 to the volume of DNA we would like to add. 

for i in range(12):
	p10_8.pick_up_tip(tiprack_10_2.cols(i))
	p10_8.aspirate(2,gDNA_plate.cols(i))
	p10_8.dispense(2,dest_plate.cols(i))
	p10_8.drop_tip()
#p10_8.transfer(8,gDNA_plate.wells('A1'),dest_plate.wells('A1'))

robot.home()

for c in robot.commands():
    print(c)
