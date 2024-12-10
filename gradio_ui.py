import gradio as gr

# The main simulation function
def particle_simulation(x_i, y_i, V):
    # Constants
    m = 9.1093837e-31
    q = -1.6021766e-19
    k = 8.99e9
    x_q = 0.068
    y_q = -0.022
    Q = -81e-12

    # Validate inputs
    x_i = int(x_i)
    y_i = int(y_i)
    V = int(V)

    if abs(x_i) > 20 or abs(y_i) > 20 or V < 10 or V > 10000:
        return "Invalid input: Parameters out of range."

    # Adjust initial positions
    x_i = x_i / 100 - x_q
    y_i = y_i / 100 - y_q

    # Simulation
    dt = 1e-9  # Time step
    r_x, r_y, r_z = [], [], []
    x_old, y_old, z_old = x_i, y_i, -5e2
    vx_old, vy_old, vz_old = 0, 0, (abs(2 * q * V / m))**0.5

    z_new = 0
    is_forward = True
    i = 0

    while z_new <= 0.5 and i <= 1e7 and is_forward:
        vx_new = vx_old + (k * Q * q * x_old / m) / ((x_old**2 + y_old**2 + z_old**2)**1.5) * dt
        vy_new = vy_old + (k * Q * q * y_old / m) / ((x_old**2 + y_old**2 + z_old**2)**1.5) * dt
        vz_new = vz_old + (k * Q * q * z_old / m) / ((x_old**2 + y_old**2 + z_old**2)**1.5) * dt

        x_new = x_old + vx_new * dt
        y_new = y_old + vy_new * dt
        z_new = z_old + vz_new * dt

        r_x.append(x_new)
        r_y.append(y_new)
        r_z.append(z_new)

        is_forward = z_new > z_old
        vx_old, vy_old, vz_old = vx_new, vy_new, vz_new
        x_old, y_old, z_old = x_new, y_new, z_new
        i += 1

    if abs(r_x[-1] + x_q) > 0.5 or abs(r_y[-1] + y_q) > 0.5 or not is_forward:
        return "Beam did not reach the detector screen."
    else:
        return f"Beam reached the screen:\nX: {round((r_x[-1] + x_q) * 100, 2)} cm\nY: {round((r_y[-1] + y_q) * 100, 2)} cm\nZ: {round(r_z[-1], 2)} cm"

# Create the Gradio interface
iface = gr.Interface(
    fn=particle_simulation,
    inputs=[
        gr.Number(label="Initial X-axis Position (cm)"),
        gr.Number(label="Initial Y-axis Position (cm)"),
        gr.Number(label="Beam Accelerating Voltage (V)"),
    ],
    outputs="text",
    title="Particle Simulation",
    description="Enter the parameters to calculate the beam trajectory. Note: Inputs out of range will result in errors.",
    flagging_mode="never",
)