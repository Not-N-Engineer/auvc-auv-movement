# from std_msgs.msg import Float64

def pid(previous_error, error, error_acc, dt, Kp = 1.0, Ki = 1.0, Kd = 1.0):
    p = p_control(Kp, error)
    i = i_control(Ki, error, error_acc, dt)
    d = d_control(Kd, error, previous_error, dt)

    pid = p + i + d
    return (pid, error)

#P, I, and D methods
def p_control(Kp, error):
    proportional = Kp * error
    return proportional
    
def i_control(Ki, error, error_acc, dt):
    error_acc += error * dt # dt is the time since the last update
    integral = Ki * error_acc
    integral = min(Ki * error_acc, 1.0)
    return integral
    
def d_control(Kd, error, previous_error, dt):
    derivative = Kd * (error - previous_error) / dt # dt is the time since the last update
    return derivative
