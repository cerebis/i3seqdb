from opentrons import containers, instruments

# a 1.5mL tube rack sources primer+KAPA+Water:
tuberack = containers.load('tube-rack-2ml', 'D2')

# destination plate: 
plate = containers.load('96-PCR-flat', 'C1')

# a tip rack for our pipette:
p100rack = containers.load('tiprack-200ul', 'B2')

# wells to dispense samples for the reverse primers:
R0_wells = [
    well.bottom() for well in plate.wells(
        'A1','B1','C1','D1','E1','F1','H1','G1','A5','B5','C5','D5','E5','F5','H5',
        'G5','A9','B9','C9','D9','E9','F9','H9','G9')]

R1_wells = [
    well.bottom() for well in plate.wells(
        'A2','B2','C2','D2','E2','F2','H2','G2','A6','B6','C6','D6','E6','F6','H6',
        'G6','A10','B10','C10','D10','E10','F10','H10','G10')]
        
R2_wells = [
    well.bottom() for well in plate.wells(
        'A3','B3','C3','D3','E3','F3','H3','G3','A7','B7','C7','D7','E7','F7','H7',
        'G7','A11','B11','C11','D11','E11','F11','H11','G11')]
        
R3_wells = [
    well.bottom() for well in plate.wells(
        'A4','B4','C4','D4','E4','F4','H4','G4','A8','B8','C8','D8','E8','F8','H8',
        'G8','A12','B12','C12','D12','E12','F12','H12','G12')]


# R0 solution location
R0 = tuberack('A1')
# R1 solution location
R1 = tuberack('B1')
# R2 solution location
R2 = tuberack('C1')
# R3 solution location
R3 = tuberack('D1')



def run_custom_protocol(
        pipette_axis: 'StringSelection...'='B (left side)'):

    p200 = instruments.Pipette(
        axis='b' if pipette_axis[0] == 'B' else 'a',
        min_volume=10,
        max_volume=100,
        tip_racks=[p100rack],
    )

    # macro commands like .distribute() make writing long sequences easier:
    # distribute R0 solution to the wells
    p200.distribute(22.5, R0, R0_wells, disposal_vol=0, blow_out=False)
    # distribute R1 solution to the wells
    p200.distribute(22.5, R1, R1_wells, disposal_vol=0, blow_out=False)
    # distribute R2 solution to the wells
    p200.distribute(22.5, R2, R2_wells, disposal_vol=0, blow_out=False)
    # distribute R3 solution to the wells
    p200.distribute(22.5, R3, R3_wells, disposal_vol=0, blow_out=False)
    

run_custom_protocol(**{'pipette_axis': 'A (right side)'})
