import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Import both PID versions
from pid_v1 import PIDController as PIDControllerV1

st.title("PID Controller Simulator")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")
pid_version = st.sidebar.selectbox("Select PID Version", ["pid_v1", "pid_v2"])
setpoint = st.sidebar.number_input("Desired Temperature", min_value=-100.0, max_value=200.0, value=100.0, key="sym:setpoint")
process_variable = st.sidebar.number_input("Initial Temperature", min_value=-100.0, max_value=200.0, value=20.0, key="sym:process_variable")
time_seconds = st.sidebar.number_input("Simulation Time (seconds)", min_value=1, max_value=1000, value=10)
time_steps = st.sidebar.number_input("Number of Steps", min_value=10, max_value=10000, value=100)
Kp = st.sidebar.number_input("Kp", min_value=0.0, max_value=100.0, value=1.0)
Ki = st.sidebar.number_input("Ki", min_value=0.0, max_value=100.0, value=0.1)
Kd = st.sidebar.number_input("Kd", min_value=0.0, max_value=100.0, value=0.05)

run_sim = st.sidebar.button("Run Simulation")

if run_sim:
    time = np.linspace(0, time_seconds, int(time_steps))
    dt = time[1] - time[0]
    pv = process_variable
    process_values = []
    setpoints = []

    if pid_version == "pid_v1":
        pid = PIDControllerV1(Kp, Ki, Kd, setpoint)
        for t in time:
            control_output = pid.compute(pv, dt)
            pv += control_output * dt - 0.1 * (pv - 20) * dt
            process_values.append(pv)
            setpoints.append(setpoint)
    else:
        pid = PIDControllerV2(Kp, Ki, Kd, setpoint)
        for i, t in enumerate(time):
            pid.set_setpoint(setpoint)
            control_output = pid.compute(pv, current_time=t)
            pv += control_output * dt - 0.1 * (pv - 20) * dt
            process_values.append(pv)
            setpoints.append(setpoint)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(time, process_values, label="Process Variable (Temperature)")
    ax.plot(time, setpoints, "r--", label="Setpoint")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature")
    ax.set_title("PID Controller Simulation")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

st.markdown("""
- **Desired Temperature**: The setpoint for the PID controller.
- **Initial Temperature**: The starting process variable.
- **Simulation Time**: Total time for the simulation.
- **Number of Steps**: Number of simulation steps (resolution).
- **Kp, Ki, Kd**: PID controller gains.
- **PID Version**: Choose between your two implementations.
""")
