from opentrons import robot,labware, instruments
import math

###This has been tested and worked well with 10 ul tips, when pipetting with 10 ul tip onlyself.
##Do not use two pipettes at the same time at the moment to avoid tips crashing the plateself.

##At the moment, the robot gets the location and the volume of the samples from the entry belowself.
##The robot will go through the location in row and column manners, not random.
##The reason is if things happen, and the robot needs to stop, I can manually start pipetting where it left off.

ep_rack = labware.load('epMotion2', '1')
###
#epMotion2 is a epMotion reservoir rack with 10mL reservoir. I have already created this before using this script.

tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['6', '7']]
tiprack_50 = labware.load('tiprack-200ul', '9')

pool=ep_rack.cols('1')

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tiprack_10)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tiprack_50)

######### Pooling
#1.Get the number and location from CSV files
#2.Transfer a particular volume from particular well to the epMotion reservoir 10 mL
#3.Change tips

##The current dead volume for PCR-flat is 3 ul.
##Do two plates at a time.

def run_custom_protocol(
        volumes_csv: 'FileInput'=example_csv,
        tip_reuse: 'StringSelection...'='new tip each time'
        ):
    data = [
        [well, float(vol)]
        for well, vol in
        [row.split(',') for row in volumes_csv.strip().split('\n') if row]
    ]

    dest_plate = pool

    for well_idx, (source_well, vol) in enumerate(data):
            p10.transfer(
            vol,
            source_plate.wells(source_well),
            pool
            )

##Source Plate 1
source_plate = labware.load('96-flat','3')
run_custom_protocol(**{'volumes_csv':
'A1,2.4\r\nB1,1.7\r\nC1,4.3\r\nD1,2.1\r\nE1,7.7\r\nF1,3.4\r\nG1,15.6\r\nH1,1.8\r\nA2,3.4\r\nB2,2.4\r\nC2,2.3\r\nD2,1.7\r\nE2,6.3\r\nF2,2.3\r\nG2,5.8\r\nH2,2.2\r\nA3,2.5\r\nB3,3.4\r\nC3,3.0\r\nD3,1.8\r\nE3,7.5\r\nF3,2.1\r\nG3,2.8\r\nA4,2.2\r\nB4,2.3\r\nC4,2.3\r\nD4,1.6\r\nE4,11.3\r\nF4,2.0\r\nG4,3.1\r\nA5,2.2\r\nB5,2.0\r\nC5,1.9\r\nD5,2.0\r\nE5,5.1\r\nF5,1.9\r\nG5,3.4\r\nH5,1.8\r\nA6,2.1\r\nB6,2.3\r\nC6,2.2\r\nD6,2.1\r\nE6,8.9\r\nF6,2.0\r\nG6,14.8\r\nH6,2.1\r\nA7,2.3\r\nB7,2.4\r\nC7,2.6\r\nD7,2.7\r\nE7,3.3\r\nF7,2.2\r\nG7,3.6\r\nH7,3.1\r\nA8,2.7\r\nB8,1.9\r\nC8,2.2\r\nD8,2.2\r\nE8,12.1\r\nF8,1.8\r\nG8,3.1\r\nH8,2.8\r\nA9,2.6\r\nB9,2.8\r\nD9,2.1\r\nE9,13.9\r\nF9,2.4\r\nG9,3.7\r\nH9,2.5\r\nA10,2.6\r\nB10,2.1\r\nC10,2.5\r\nD10,2.4\r\nE10,8.6\r\nF10,3.4\r\nG10,5.0\r\nH10,2.5\r\nA11,2.9\r\nB11,2.2\r\nC11,1.9\r\nD11,1.9\r\nE11,5.2\r\nF11,2.0\r\nG11,14.6\r\nH11,1.9\r\nA12,1.4\r\nB12,2.0\r\nC12,2.6\r\nD12,2.8\r\nE12,13.7\r\nF12,2.5\r\nG12,11.9\r\nH12,2.2', 'tip_reuse': 'reuse tip'})


##Source Plate 2
source_plate = labware.load('96-flat','2')
run_custom_protocol(**{'volumes_csv':
'A1,2.3\r\nB1,2.2\r\nC1,4.3\r\nD1,1.8\r\nE1,2.0\r\nF1,2.1\r\nG1,1.8\r\nH1,2.0\r\nA2,2.3\r\nB2,2.5\r\nC2,2.8\r\nD2,11.0\r\nE2,3.5\r\nF2,3.6\r\nG2,2.2\r\nH2,2.3\r\nA3,2.3\r\nB3,4.4\r\nC3,2.1\r\nD3,18.1\r\nE3,2.1\r\nF3,2.3\r\nG3,2.0\r\nH3,1.9\r\nB4,2.4\r\nC4,2.1\r\nD4,1.8\r\nE4,2.0\r\nF4,2.1\r\nG4,2.2\r\nH4,2.0\r\nA5,2.3\r\nB5,2.5\r\nC5,1.9\r\nD5,1.9\r\nE5,2.1\r\nF5,2.4\r\nG5,2.2\r\nH5,2.6\r\nA6,2.1\r\nB6,2.2\r\nC6,2.2\r\nD6,2.2\r\nE6,2.1\r\nF6,1.9\r\nG6,2.0\r\nH6,2.9\r\nA7,2.5\r\nB7,2.1\r\nC7,1.8\r\nD7,2.3\r\nE7,2.9\r\nF7,2.0\r\nG7,2.8\r\nA8,2.2\r\nB8,2.0\r\nC8,2.4\r\nD8,2.5\r\nE8,2.3\r\nF8,3.0\r\nG8,2.6\r\nH8,3.0\r\nA9,2.7\r\nB9,1.9\r\nC9,2.2\r\nD9,2.1\r\nE9,1.8\r\nF9,2.5\r\nG9,2.3\r\nH9,2.4\r\nA10,2.3\r\nB10,2.5\r\nC10,2.3\r\nD10,2.1\r\nE10,2.0\r\nF10,2.5\r\nG10,2.4\r\nH10,1.9\r\nA11,3.0\r\nB11,2.1\r\nC11,2.2\r\nD11,2.0\r\nE11,2.5\r\nF11,2.1\r\nG11,2.0\r\nH11,2.1\r\nA12,1.7\r\nB12,2.2\r\nC12,2.6\r\nD12,2.0\r\nE12,2.2\r\nF12,2.1\r\nG12,1.9\r\nH12,1.8', 'tip_reuse': 'reuse tip'})


robot.home()
