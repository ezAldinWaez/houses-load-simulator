from dataclasses import dataclass


@dataclass
class ApplianceSettings:
    """
    Attributes
    ----------
    - options : (setting name -> list of all possible values).
    - powerFactors : (setting name -> (value -> power multiplier)).
    """
    options: dict[str, list[str]]
    power_factors: dict[str, dict[str, float]]


@dataclass
class ADSRParams:
    """
    Attributes
    ----------
    - a : Attack Time (in sec).
    - d : Decay Time (in sec).
    - s : Sustain Level (in watt).
    - r : Release Tiem (in sec).
    - wt : Wave Type ("none" | "sine" | "square" | "random").
    - wp : Wave Period (in sec).
    - wa : Wave Amplitude Multiplier (betweent 0 and 1).
    """
    a: float
    d: float
    s: float
    r: float
    wt: str = "none"
    wp: float = 0
    wa: float = 0


# Define devices configuration
DEVICES_CONFIG = {
    "LED Lights": {
        "wattage": 9,
        "max_count": 20,
        "adsr": ADSRParams(a=1.0, d=1.0, s=1.0, r=1.0),
        "settings": None
    },
    "TV/Entertainment": {
        "wattage": 120,
        "max_count": 4,
        "adsr": ADSRParams(a=1.0, d=1.0, s=0.8, r=1.5, wt="sine", wp=.5, wa=0.1),
        "settings": None
    },
    "Refrigerator": {
        "wattage": 150,
        "max_count": 2,
        "adsr": ADSRParams(a=1.0, d=1.0, s=0.3, r=2.0, wt="square", wp=3, wa=0.06),
        "settings": None
    },
    "HVAC": {
        "wattage": 3500,
        "max_count": 1,
        "adsr": ADSRParams(a=3.0, d=2.0, s=0.8, r=0.5, wt="sine", wp=2, wa=0.07),
        "settings": None
    },
    "Washing Machine": {
        "wattage": 500,
        "max_count": 1,
        "adsr": ADSRParams(a=2.0, d=2.0, s=0.7, r=0.5, wt="sine", wp=.5, wa=0.04),
        "settings": ApplianceSettings(
            options={
                "program": ["Quick Wash", "Normal", "Heavy Duty", "Delicate"],
                "temperature": ["Cold", "Warm", "Hot"],
                "spin_speed": ["Low", "Medium", "High"]
            },
            power_factors={
                "program": {
                    "Quick Wash": 0.7,
                    "Normal": 1.0,
                    "Heavy Duty": 1.3,
                    "Delicate": 0.8
                },
                "temperature": {
                    "Cold": 0.6,
                    "Warm": 1.0,
                    "Hot": 1.4
                },
                "spin_speed": {
                    "Low": 0.8,
                    "Medium": 1.0,
                    "High": 1.2
                }
            }
        )
    },
    "Dryer": {
        "wattage": 3000,
        "max_count": 1,
        "adsr": ADSRParams(a=2.0, d=1.0, s=0.9, r=2.0, wt="sine", wp=2, wa=0.03),
        "settings": ApplianceSettings(
            options={
                "program": ["Quick Dry", "Normal", "Heavy Duty", "Delicate"],
                "temperature": ["Low", "Medium", "High"],
                "time": ["30 min", "60 min", "90 min"]
            },
            power_factors={
                "program": {
                    "Quick Dry": 0.8,
                    "Normal": 1.0,
                    "Heavy Duty": 1.2,
                    "Delicate": 0.7
                },
                "temperature": {
                    "Low": 0.7,
                    "Medium": 1.0,
                    "High": 1.3
                },
                "time": {
                    "30 min": 1.0,
                    "60 min": 1.0,
                    "90 min": 1.0
                }
            }
        )
    },
    "Dishwasher": {
        "wattage": 1800,
        "max_count": 1,
        "adsr": ADSRParams(a=3.0, d=1.5, s=0.6, r=2.0, wt="sine", wp=1, wa=0.05),
        "settings": ApplianceSettings(
            options={
                "program": ["Quick", "Eco", "Normal", "Intensive"],
                "temperature": ["Low", "Medium", "High"],
                "dry": ["No Heat", "Heat Dry"]
            },
            power_factors={
                "program": {
                    "Quick": 0.8,
                    "Eco": 0.6,
                    "Normal": 1.0,
                    "Intensive": 1.4
                },
                "temperature": {
                    "Low": 0.7,
                    "Medium": 1.0,
                    "High": 1.3
                },
                "dry": {
                    "No Heat": 0.7,
                    "Heat Dry": 1.2
                }
            }
        )
    },
    "Water Heater": {
        "wattage": 4500,
        "max_count": 1,
        "adsr": ADSRParams(a=1.0, d=0.5, s=0.9, r=1.0, wt="square", wp=5, wa=0.1),
        "settings": None
    },
    "Microwave": {
        "wattage": 1100,
        "max_count": 1,
        "adsr": ADSRParams(a=0.5, d=0.2, s=1.0, r=0.5),
        "settings": None
    }
}
