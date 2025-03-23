import numpy as np
import matplotlib.pyplot as plt

p_term = 0.125
i_term = 0.00001
d_term = 0.2

timestep = 0.1

process_event = 0
setpoint = 100

acceleration_cap = (-40, 40)
acceleration = 9 * timestep
gravity = 9.8 * timestep


frame_passed = 0
step_passed = 0
frame_limit = 12000

speed = 0
error_integral = 0
error_prev = setpoint - process_event
error_derivative = 0

speed_array = []
setpoint_array = []
acceleration_array = []
distance_array = []
error_integral_array = []
error_derivative_array = []
proportional_array = []
error_array = []

while frame_passed < frame_limit:
    setpoint = np.sin((frame_passed/frame_limit) * 4 * np.pi) * 100
    setpoint_array.append(setpoint)

    distance_array.append(process_event)
    speed_array.append(speed)

    error = setpoint - process_event
    error_integral += error * timestep
    error_derivative = (error - error_prev) / timestep

    proportion = (p_term * error) / acceleration_cap[1]
    integral = i_term * error_integral
    derivative = d_term * error_derivative

    error_array.append(error)
    proportional_array.append(proportion)
    error_integral_array.append(integral)
    error_derivative_array.append(derivative)

    # Add acceleration
    # processed_acceleration = acceleration * (
    #        proportion + integral + derivative)
    processed_acceleration = acceleration * (
            proportion + integral + derivative)

    acceleration_array.append(processed_acceleration)
    speed += processed_acceleration

    """
    if error > 0:
        acceleration_array.append(processed_acceleration)
        speed += processed_acceleration
    elif error < 0:
        acceleration_array.append(-processed_acceleration)
        speed -= processed_acceleration
    else:
        acceleration_array.append(0)
    """

    error_prev = error
    process_event += speed
    speed -= gravity

    frame_passed += timestep
    step_passed += 1

x = np.arange(0, step_passed)
y0 = np.array(setpoint_array)
y1 = np.array(distance_array)
y2 = np.array(speed_array)
y3 = np.array(acceleration_array)
y4 = np.array(error_integral_array)
y5 = np.array(error_derivative_array)
y6 = np.array(proportional_array)
y7 = np.array(error_array)

fig, ((ax1, ax2, ax3, ax7), (ax4, ax5, ax6, ax8)) = plt.subplots(2, 4)

ax1.plot(x, y1)
ax1.set_title("process event")

ax2.plot(x, y0)
ax2.set_title("setpoint")

ax3.plot(x, y2)
ax3.set_title("speed")

ax4.plot(x, y3)
ax4.set_title("acceleration")

ax5.plot(x, y4)
ax5.set_title("integral")

ax6.plot(x, y5)
ax6.set_title("derivative")

ax7.plot(x, y6)
ax7.set_title("proportional")

ax8.plot(x, y7)
ax8.set_title("error")

plt.show()
