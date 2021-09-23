import os
import csv
import json
import requests
from dotenv import load_dotenv

def getparsed(raid):
    raid = raid.lower()
    csv_name = 'res.txt'
    downloadcsv(raid, csv_name)
    arr = parsecsv(csv_name)
    str = writearrtostr(raid, arr)
    return str

def writearrtostr(raid, arr):
    raid = raid.upper()
    master_str = f'**__{raid}__**\n'

    for boss in arr:
        boss_name = boss['name']
        tanks = boss['tanks']
        healers = boss['healers']

        master_str += f'**{boss_name}**\n'
        for tank in tanks:
            master_str += f'{tank}\n'
        master_str += '\n'
        for healer in healers:
            master_str += f'{healer}\n'
        master_str += '\n'
    return master_str

def downloadcsv(raid, name):
    load_dotenv()
    
    url = None
    if raid == 'ssc':
        url = os.getenv('CSV_URL_SSC')
    elif raid == 'tk':
        url = os.getenv('CSV_URL_TK')
    else:
        return None

    result = requests.get(url, allow_redirects=True)
    open('res.txt', 'wb').write(result.content)

def parsecsv(csv_name):
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        x_index = 0
        double_arr = []
        for row in csv_reader:
            y_index = 0
            x_index += 1
            inner_arr = []
            for col in row:
                y_index += 1
                inner_arr.append(col)
            double_arr.append(inner_arr)
        
        tank_assignments = []
        healer_assignments = []
        y = 0
        while y < len(double_arr):
            x = 0
            while x < len(double_arr[y]):
                if double_arr[y][x] == 'Tanks': #tanks
                    print(f':Found a tank assignment at (y,x)=({y},{x})')

                    # check if assigned
                    ass_y = y
                    ass_x = x + 1
                    assigned = double_arr[ass_y][ass_x]
                    if assigned.lower() != '--unassigned':
                        # boss name
                        boss_y = y - 1
                        boss_x = x
                        boss_name = double_arr[boss_y][boss_x]

                        boss_assignments_json = '{"name":"", "tanks":[], "healers":[]}'
                        boss_assignments = json.loads(boss_assignments_json)
                        boss_assignments['name'] = boss_name

                        # find tanks
                        tank_assigns = []
                        tank_y = y + 1
                        tank_x = x
                        current_row = double_arr[tank_y][tank_x] # first tank
                        while current_row:
                            current_item = current_row
                            tank_str = current_item + ": " # target row
                            index = 0
                            row_x = tank_x + 1
                            current_item = double_arr[tank_y][row_x]
                            while current_item:
                                if index > 0:
                                    tank_str += ", "
                                index += 1
                                tank_str += current_item

                                row_x += 1
                                current_item = double_arr[tank_y][row_x]
                            tank_assigns.append(tank_str)
                            tank_y += 1
                            current_row = double_arr[tank_y][tank_x]
                        
                        # append boss
                        boss_assignments['tanks'] = tank_assigns
                        tank_assignments.append(boss_assignments)
                if double_arr[y][x] == 'Healers': #healers
                    print(f':Found a healer assignment at (y,x)=({y},{x})')

                    boss_assignments_json = '{"name":"", "tanks":[], "healers":[]}'
                    boss_assignments = json.loads(boss_assignments_json)

                    # find boss
                    boss_y = y
                    boss_x = x
                    boss_search = double_arr[boss_y][boss_x]
                    while boss_search != "Tanks":
                        boss_y -= 1
                        boss_search = double_arr[boss_y][boss_x]
                    boss_search = double_arr[boss_y - 1][boss_x]
                    boss_assignments['name'] = boss_search

                    # check if assigned
                    ass_y = boss_y + 1
                    ass_x = boss_x + 1
                    assigned = double_arr[ass_y][ass_x]
                    if assigned.lower() != '--unassigned':
                        # find healers
                        heal_assigns = []
                        heal_y = y + 1
                        heal_x = x
                        current_row = double_arr[heal_y][heal_x] # first healer
                        if current_row != "Healer":
                            while current_row:
                                current_item = current_row
                                heal_str = current_item + ": " # healer row
                                row_x = heal_x
                                while current_item:
                                    row_x += 1
                                    current_item = double_arr[heal_y][row_x]
                                    heal_str += current_item
                                heal_assigns.append(heal_str)
                                heal_y += 1
                                current_row = double_arr[heal_y][heal_x]
                        else:
                            phases = []
                            phase_y = heal_y
                            phase_x = heal_x + 1
                            current_phase = double_arr[phase_y][phase_x] # first phase
                            while current_phase:
                                phases.append(current_phase)
                                phase_x += 1
                                current_phase = double_arr[phase_y][phase_x]

                            heal_y += 1
                            current_healer = double_arr[heal_y][heal_x]
                            while current_healer:
                                heal_str = current_healer + ": "
                                target_x = heal_x + 1
                                index = 0
                                for phase in phases:
                                    if index > 0:
                                        heal_str += " & "
                                    target = double_arr[heal_y][target_x]
                                    heal_str += target + " during " + phase
                                    target_x += 1
                                    index += 1
                                heal_assigns.append(heal_str)
                                heal_y += 1
                                current_healer = double_arr[heal_y][heal_x]

                        # append boss
                        boss_assignments['healers'] = heal_assigns
                        healer_assignments.append(boss_assignments)
                # iterate
                x += 1
            y += 1

        # merge to one array
        for assignment in tank_assignments:
            match = next((x for x in healer_assignments if x['name'] == assignment['name']), None)
            assignment['healers'] = match['healers']
        
        #print(f'BOSS ASSIGNMENTS:')
        #for assignment in tank_assignments:
        #    print("---")
        #    print(assignment['name'])
        #    print(assignment['tanks'])
        #    print(assignment['healers'])
        #
        #print(f'Done.')
        return tank_assignments