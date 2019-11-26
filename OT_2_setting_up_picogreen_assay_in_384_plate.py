"""
The protocol is adapted to be used at UTS NGS facility.
The protocol set up a 384 well plate, picogreen assay.
It uses epMotion 10mL as a reservoir for Picogreen, transferring sample from a PCR plate, using multichannel.
Change the number of the assay start, end and the sample 1 and 2 start end according to the sample.
Author: Kay Anantanawat
Update date: 05/8/2019
"""


from opentrons import instruments, labware, robot

############PARAMETER#################

assay_start=2 #The start of the column of 384 well plates I want to dispense TE into.
assay_end=48 #The end of the column I want to disepnse TE
assay_1_start=2
assay_2_start=22
sample_1_start=0 #the column of 384 well plate where the sample was first dispensed into.
sample_1_end=11 #the column of 384 well plate where the sample was last dispensed into.
sample_2_start=0 #the column of 384 well plate where the sample from plate 2 was first dispensed into.
sample_2_end=11 #the column of 384 well plate where the sample from plate 2 was last dispensed into.

plate_name = 'epMotion_10mL'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(7, 1),                    # specify amount of (columns, rows)
        spacing=(17.5, 0),               # distances (mm) between each (column, row)
        diameter=5,                     # diameter (mm) of each well on the plate
        depth=30,                       # depth (mm) of each well on the plate
        volume=10000)

PG = labware.load('epMotion_10mL', '11', 'PG')
plate_384 = labware.load('corning_384_wellplate_112ul_flat', '2', 'plate')
sample_1=labware.load('biorad_96_wellplate_200ul_pcr','3')
sample_2=labware.load('biorad_96_wellplate_200ul_pcr','6')


tiprack_200 = labware.load('tiprack-200ul', '1', 'p200rack')

tiprack_10_1=labware.load('opentrons_96_tiprack_10ul','4')
tiprack_10_2=labware.load('opentrons_96_tiprack_10ul','7')


P10_8 = instruments.P10_Multi(
	mount='left',
	tip_racks=[tiprack_10_1,tiprack_10_2])

P50_8 = instruments.P50_Multi(
	mount='right',
	tip_racks=[tiprack_200])

alternating_wells = []
for column in plate_384.cols():
		alternating_wells.append(column.wells('A'))
		alternating_wells.append(column.wells('B'))

##Transfer the Picogreen
while assay_start<(assay_end-6):
	P50_8.pick_up_tip()
	P50_8.transfer(19, PG.wells('A1'), alternating_wells[assay_start:assay_start+6], new_tip='never')
	P50_8.drop_tip()
	assay_start=assay_start+6

P50_8.pick_up_tip()
P50_8.transfer(19, PG.wells('A1'), alternating_wells[assay_start:assay_end])

##Transfer Picogreen
##Sample Plate 1
j1=assay_1_start
for i in sample_1.cols(sample_1_start, to=sample_1_end):
	if j1<47:
		k=j1+2
		P10_8.pick_up_tip()
		P10_8.transfer(1,i,alternating_wells[j1:k],new_tip='never')
		P10_8.drop_tip()
		j1=j1+2

##Sample Plate 2
for i in sample_2.cols(sample_2_start, to=sample_2_end):
	if j1<47:
		k=j1+2
		P10_8.pick_up_tip()
		P10_8.transfer(1,i,alternating_wells[j1:k],new_tip='never')
		P10_8.drop_tip()
		j1=j1+2

robot.home()
