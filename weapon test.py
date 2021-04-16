import json
import traceback

local_file = "E:\Roguetech\RogueTech\RogueModuleTech\VanillaWeapons\Weapon_Autocannon_AC10_0-STOCK.json"

with open(local_file) as f:
    data = json.load(f)

#weapon damage module - pulls the highest damage from base + any available modes and sets value to weapon_damage variable.
try:
    max_mode_dam = 0 #set mode index of mode highest dam weapon
    max_dam_mode = 0 #set value of highest additional damage in modes
    weapon_damage = 0 #Damage modes loop max damage value
    for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
        print('Damage mode', i)
        try:
            if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                max_mode_dam = data['Modes'][i]['DamagePerShot']
                max_dam_mode = i
            try:
                if data['Modes'][i]['ShotsWhenFired']:#check for ShotsWhenFired in mode
                    weapon_damage = data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
            except KeyError:
                traceback.print_exc()
                weapon_damage = data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * data['ShotsWhenFired']
        except KeyError: #if no DamagePerShot in mode found
            traceback.print_exc()
            print('skipped')
except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
    print('No modes. Reverting to base values.')
    traceback.print_exc()
    weapon_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot

try:
    max_shots_mode = 0 #set mode index of mode with highest shot count
    max_mode_shots = 0 #set value of mode with most additional shots
    weapon_damage2 = 0 #Shots modes loop max damage value
    for i in range(len(data['Modes'])):
        print('Shots loop:', i)
        try:#if no damage in modes found then check modes for additional shots and calculate damage against base value
            if data['Modes'][i]['ShotsWhenFired'] > max_mode_shots:
                max_mode_shots = data['Modes'][i]['ShotsWhenFired']
                max_shots_mode = i
            try:
                weapon_damage2 = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_shots_mode]['ShotsWhenFired']) #damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
                print(max_mode_shots)
            except:
                print('can this be reached?')
                traceback.print_exc()
        except:
            weapon_damage2 = data['Damage'] + max_mode_shots * data['ProjectilesPerShot'] * data['ShotsWhenFired']   
except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
    print('No modes. Reverting to base values.')
    weapon_damage2 = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot

if weapon_damage2 > weapon_damage:#checks the max damage mode and the max shots mode loop max damage values against each other and sets the highest 
    weapon_damage = weapon_damage2

print(weapon_damage, weapon_damage2)
print('Tonnage ', data['Tonnage'] )