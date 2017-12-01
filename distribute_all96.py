from opentrons import containers, instruments

# a 12 row trough for sources
trough = containers.load('trough-12row', 'D2')

# destination plate 
plate = containers.load('96-PCR-flat', 'C1')

# a tip rack for our pipette
p200rack = containers.load('tiprack-200ul', 'B2')

# wells to dispense samples
green_wells = [
    well.bottom() for well in plate.wells(
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
		'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
		'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
		'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
		'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
		'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
		'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12',
		'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',)]

# wells to dispense samples back plates in blue, incase with a different volume:
blue_wells = [
    well.bottom() for well in plate.wells(
        'C3', 'B4', 'A5', 'B5', 'B6', 'A7', 'B7',
        'C8', 'C9', 'D9', 'E10', 'E11', 'F11', 'G12')]

# green solution location
green = trough.wells('A1')
# blue solution location
blue = trough.wells('A7')


def run_custom_protocol(
        pipette_axis: 'StringSelection...'='B (left side)'):

    p200 = instruments.Pipette(
        axis='b' if pipette_axis[0] == 'B' else 'a',
        min_volume=20,
        max_volume=200,
        tip_racks=[p200rack],
    )

    # macro commands like .distribute() make writing long sequences easier:
    # distribute green solution to the wells
    p200.distribute(100, green, green_wells, disposal_vol=0, blow_out=False)
	# distribute blue solution to specific wells:
	#run p200.distribute(50, blue_wells, disposal_vol=0, blow_out=False/True)

run_custom_protocol(**{'pipette_axis': 'A (right side)'})
