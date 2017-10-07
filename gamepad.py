from inputs import devices

pad = devices.gamepads[0]
stick_max = 2.0**1.5

def turn(event)
    if abs(event.state/stick_max) < .15:
        


