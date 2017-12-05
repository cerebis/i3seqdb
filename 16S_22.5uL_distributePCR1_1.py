from opentrons import containers, instruments

# a 1.5mL tube rack sources primer+KAPA+Water:
tuberack = containers.load('tube-rack-2ml', 'D2')

# destination plate: 
plate = containers.load('96-PCR-flat', 'C1')

# a tip rack for our pipette:
p100rack = containers.load('tiprack-200ul', 'B2')

# wells to dispense samples for the forward primers:
F0_wells = [
    well.bottom() for well in plate.wells(
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
		'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12')]

F1_wells = [
    well.bottom() for well in plate.wells(
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
		'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12')]

F2_wells = [
    well.bottom() for well in plate.wells(
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
		'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12')]
		
F3_wells = [
    well.bottom() for well in plate.wells(
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
		'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12')]
				

# F0 solution location
F0 = tuberack('A1')
# F1 solution location
F1 = tuberack('B1')
# F2 solution location
F2 = tuberack('C1')
# F3 solution location
F3 = tuberack('D1')

def run_custom_protocol(
        pipette_axis: 'StringSelection...'='B (left side)'):

    p200 = instruments.Pipette(
        axis='b' if pipette_axis[0] == 'B' else 'a',
        min_volume=10,
        max_volume=100,
        tip_racks=[p100rack],
    )

    # macro commands like .distribute() make writing long sequences easier:
    # distribute ForwardPrimerF1 solution to the wells
    p200.distribute(22.5, F0, F0_wells, disposal_vol=0, touch_tip=True, blow_out=False)
    # distribute ForwardPrimerF1 solution to the wells
    p200.distribute(22.5, F1, F1_wells, disposal_vol=0, blow_out=False)
    # distribute ForwardPrimerF1 solution to the wells
    p200.distribute(22.5, F2, F2_wells, disposal_vol=0, blow_out=False)
    # distribute ForwardPrimerF1 solution to the wells
    p200.distribute(22.5, F3, F3_wells, disposal_vol=0, blow_out=False)
   
run_custom_protocol(**{'pipette_axis': 'A (right side)'})
