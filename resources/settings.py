from cred import TOKEN, API_URL

SCRAPE_INTERVAL = 15
METRIC_PFX = "sun2k"
ENTITY_PFX = "sensor.inverter"
PORT = 9177
ADDR = "192.168.4.244"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
}

COUNTER_NAMES = [
    "total_yield",  # all-time produced energy
    "daily_yield",
]

GAUGE_NAMES = [
    "input_power",
    "day_active_power_peak",
    "active_power",
    "reactive_power",
    "power_factor",
    "efficiency",
    "internal_temperature",
]

# input_power
# a_b_line_voltage
# b_c_line_voltage
# c_a_line_voltage
# phase_a_voltage
# phase_b_voltage
# phase_c_voltage
# phase_a_current
# phase_b_current
# phase_c_current
# day_active_power_peak
# active_power
# reactive_power
# power_factor
# efficiency
# internal_temperature
# device_status
# startup_time
# shutdown_time
# total_yield
# daily_yield
# inverter_state
# locking_status
# pv_connection_status
# dsp_data_collection
# off_grid_status
# off_grid_switch
# alarms
# pv_1_voltage
# pv_1_current
# pv_2_voltage
# pv_2_current
