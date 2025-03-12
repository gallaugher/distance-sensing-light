# circuitplayground-distance-sensing-light.py
import board, time, adafruit_vl53l1x
import neopixel

# i2c = board.STEMMA_I2C()
i2c = board.I2C()
distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
distance_sensor.start_ranging()

lights_on_strip = 20
output_range = 20 # 0 through 20, so 21 possibilities.
# strip = neopixel.NeoPixel(board.GP16, lights_on_strip)
strip = neopixel.NeoPixel(board.A1, lights_on_strip)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
chosen_color = BLUE
max_reading = 150-30

print("Sensing Distance")
while True:
    if distance_sensor.data_ready:
        distance = distance_sensor.distance
        if distance != None: # We've got a real number, not infinity or an error
            inches = distance * 0.394
            print(f"{distance: .1f}cm, {inches: .1f}in, {inches/12: .1f}ft")
            if distance > 150: # if lights above 15, turn all black
                strip.fill(BLACK)
            else:
                distance = min(max(distance, 30), 150) # will ensure value is between 20 & 150
                # The distance-30 is because we're measuring 150-30, but want range from 120-0
                lights_to_turn_on = int((distance-30) * (output_range/max_reading))
                lights_to_turn_on = output_range-lights_to_turn_on
                print(f"distance: {distance}, light_number: {lights_to_turn_on}")
                strip[:lights_to_turn_on] = chosen_color * (lights_to_turn_on)
                strip[lights_to_turn_on:] = BLACK * (lights_on_strip-lights_to_turn_on)
        else: # deal with inifinity & error below
            print("****** NONE/INFINITY ******")
            strip.fill(BLACK)
        distance_sensor.clear_interrupt() # prepare for next reading
        time.sleep(0.1)
