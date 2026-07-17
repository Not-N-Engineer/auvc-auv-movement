def pid(desired_position, measured_position, previous_error, dt, Kp = 1.0, Ki = 1.0, Kd = 1.0):
    error = desired_position - measured_position
    p = p_control(Kp, error)
    i = i_control(Ki, error, dt)
    d= d_control(Kd, error, previous_error, dt)

    pid = p + i + d
    return (pid, error)

#P, I, and D methods
def p_control(Kp, error):
    proportional = Kp * error
    return proportional
    
def i_control(Ki, error, dt):
    error_accumulator += error * dt # dt is the time since the last update
    integral = Ki * error_accumulator
    integral = min(Ki * error_accumulator, 1.0)
    return integral
    
def d_control(Kd, error, previous_error, dt):
    derivative = Kd * (error - previous_error) / dt # dt is the time since the last update
    return derivative