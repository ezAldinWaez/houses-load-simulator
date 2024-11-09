import ttkbootstrap as ttk
import math
import random

from data import ApplianceSettings, ADSRParams
from sim_time import SimulationTime


class DeviceState:
    def __init__(self, base_wattage: float, adsr: ADSRParams, settings: ApplianceSettings | None = None):
        self.base_wattage = base_wattage
        self.adsr = adsr
        self.settings = settings
        self.count = 0
        self.active_envelopes: list[tuple[float, bool]] = []
        self.load = ttk.StringVar(value="- Watts")

        # Initialize current settings for each option if appliance settings exist
        self.current_settings: dict[str, str] = {}
        if settings:
            for option_name, possible_values in settings.options.items():
                # Default to first option
                self.current_settings[option_name] = possible_values[0]

        # Keep track of settings controls for UI updates
        self.settings_controls: dict[str, ttk.Combobox] = {}

    def update_count_and_active_envelopes(self, sim_time: SimulationTime, value: str):
        new_count = int(float(value)) if value.strip() else 0

        # Convert to real time for envelope tracking
        sim_time_elapsed = sim_time.get_elapsed()

        if new_count > self.count:
            for _ in range(new_count - self.count):
                self.active_envelopes.append((sim_time_elapsed, True))

        elif new_count < self.count:
            excess = self.count - new_count
            for i, (_, is_active) in enumerate(self.active_envelopes):
                if is_active and excess > 0:
                    self.active_envelopes[i] = (sim_time_elapsed, False)
                    excess -= 1

        self.count = new_count

    def update_setting(self, setting_name: str, value: str):
        """Update a specific setting for the device"""
        if self.settings and setting_name in self.settings.options:
            self.current_settings[setting_name] = value

    def get_settings_multiplier(self) -> float:
        """Calculate the power multiplier based on current settings"""
        if not self.settings:
            return 1.0

        total_multiplier = 1.0
        for setting_name, current_value in self.current_settings.items():
            if setting_name in self.settings.power_factors:
                factor = self.settings.power_factors[setting_name].get(
                    current_value, 1.0)
                total_multiplier *= factor

        return total_multiplier

    def get_wave_multiplier(self, elapsed: float) -> float:
        """Calculate the power multiplier based on adsr wave parameters"""
        match self.adsr.wt:
            case "none":
                return 1.0
            case "sine":
                phase = (elapsed % self.adsr.wp) / self.adsr.wp
                wave = self.adsr.wa * math.sin(2 * math.pi * phase)
                return 1.0 + wave
            case "square":
                phase = (elapsed % self.adsr.wp) / self.adsr.wp
                return 1.0 + (self.adsr.wa if phase < 0.5 else -self.adsr.wa)
            case "random":
                random.seed(int(elapsed / self.adsr.wp))
                return 1.0 + (self.adsr.wa * random.uniform(-1, 1))
            case _:
                raise ("`adsr.wt` is invalid!")

    def get_current_wattage(self, sim_time: SimulationTime) -> float:
        if not self.active_envelopes:
            return 0

        current_elapsed = sim_time.get_elapsed()
        total_wattage = 0
        settings_multiplier = self.get_settings_multiplier()

        for start_time, is_active in self.active_envelopes:
            elapsed = current_elapsed - start_time

            if not is_active:
                if elapsed <= self.adsr.r:
                    multiplier = 1.0 - (elapsed / self.adsr.r)
                else:
                    multiplier = 0
            else:
                if elapsed <= self.adsr.a:
                    multiplier = elapsed / self.adsr.a
                elif elapsed <= (self.adsr.a + self.adsr.d):
                    decay_progress = (
                        elapsed - self.adsr.a) / self.adsr.d
                    multiplier = 1.0 - \
                        ((1.0 - self.adsr.s) * decay_progress)
                else:
                    base_multiplier = self.adsr.s
                    wave_multiplier = self.get_wave_multiplier(elapsed)
                    multiplier = base_multiplier * wave_multiplier

            # Apply both the ADSR envelope multiplier and the settings multiplier
            total_wattage += self.base_wattage * multiplier * settings_multiplier

        return total_wattage
