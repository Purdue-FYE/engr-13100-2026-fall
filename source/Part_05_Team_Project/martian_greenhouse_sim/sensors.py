"""
Virtual sensor layer for the Martian greenhouse simulation.

Each sensor method returns the corresponding greenhouse state variable with
a small amount of Gaussian noise added to simulate real-world measurement
inaccuracies.  Sensor names match real hardware used in MLGH research:

+-----------+--------------------------------------------+----------------+
| Sensor    | Measurement                                | Noise (1-sigma)|
+===========+============================================+================+
| DHT22     | Temperature (°C) + Relative humidity (%)   | 0.2 °C, 1.0 %  |
+-----------+--------------------------------------------+----------------+
| K30       | CO₂ concentration (ppm)  — PRIMARY         | 20 ppm         |
|           | ⚠ Subject to freeze fault (stuck at 400)  |                |
+-----------+--------------------------------------------+----------------+
| SCD41     | CO₂ concentration (ppm)  — BACKUP          | 20 ppm         |
|           | Always returns a noisy-but-correct reading |                |
+-----------+--------------------------------------------+----------------+
| TEROS12   | Soil volumetric water content (VWC) [0-1]  | 0.01           |
+-----------+--------------------------------------------+----------------+
| SQ-500    | PAR (µmol/m²/s)                            | 10 µmol/m²/s   |
+-----------+--------------------------------------------+----------------+

CO₂ Freeze Fault (K30)
-----------------------
The K30 primary CO₂ sensor occasionally freezes, returning a stuck value of
400 ppm regardless of the true internal CO₂ level.  When the true level is
800–1000 ppm and the K30 reads 400 ppm, a naive controller will open the CO₂
valve wide and drive the greenhouse to toxic CO₂ levels (> 5 000 ppm).

Students must implement sensor redundancy logic:

    discrepancy = abs(readings.co2_ppm_primary - readings.co2_ppm_backup)
    if discrepancy > 200:   # primary has likely frozen
        co2_actual = readings.co2_ppm_backup
    else:
        co2_actual = readings.co2_ppm_primary
"""

import random
from typing import Optional, Tuple

from .constants import (
    NOISE_CO2_PPM,
    NOISE_PAR_UMOL,
    NOISE_RH_PCT,
    NOISE_TEMP_C,
    NOISE_VWC,
)
from .greenhouse import Greenhouse


class VirtualSensors:
    """
    Data acquisition layer that reads greenhouse state with realistic noise.

    Parameters
    ----------
    greenhouse : Greenhouse
        The greenhouse instance to read state from.
    rng : random.Random, optional
        Random number generator.  Pass a seeded instance for reproducible
        noise and fault patterns.
    freeze_prob_per_step : float
        Probability that the K30 sensor enters a freeze fault at any given
        time step.  Default 1.5e-4 gives roughly 6–7 events in a 30-sol run
        at Δt = 60 s.
    freeze_duration_range_s : tuple of (float, float)
        (min, max) duration of a K30 freeze event in seconds.
        Default (1 800, 10 800) = 30 min – 3 hours.
    """

    #: The value the K30 sensor returns when it is frozen.
    CO2_FREEZE_VALUE_PPM: float = 400.0

    def __init__(
        self,
        greenhouse: Greenhouse,
        rng: Optional[random.Random] = None,
        freeze_prob_per_step: float = 1.5e-4,
        freeze_duration_range_s: Tuple[float, float] = (1_800.0, 10_800.0),
    ) -> None:
        self._gh = greenhouse
        self._rng: random.Random = rng if rng is not None else random.Random()
        self._freeze_prob = freeze_prob_per_step
        self._freeze_dur_min, self._freeze_dur_max = freeze_duration_range_s
        self._co2_freeze_active: bool = False
        self._freeze_end_time_s: float = 0.0

    # ------------------------------------------------------------------
    # Required sensor API
    # ------------------------------------------------------------------

    def read_DHT22(self) -> Tuple[float, float]:
        """
        Read internal air temperature and relative humidity.

        Returns
        -------
        (temperature_c, relative_humidity_pct) : tuple of float
            Noisy readings from the DHT22 capacitive humidity/temperature
            sensor.  Temperature noise σ = 0.2 °C, RH noise σ = 1.0 %.
        """
        state = self._gh.state
        temp = state.temp_c + self._rng.gauss(0.0, NOISE_TEMP_C)
        rh = state.rh_pct + self._rng.gauss(0.0, NOISE_RH_PCT)
        rh = max(0.0, min(100.0, rh))
        return temp, rh

    def read_K30(self) -> float:
        """
        Read CO₂ concentration in ppm from the primary K30 NDIR sensor.

        .. warning::
            **Fault Mode Active.**  This sensor occasionally freezes and
            returns a stuck value of 400 ppm, regardless of the actual CO₂
            level inside the greenhouse.  Always cross-check against
            ``read_SCD41()`` before actuating the CO₂ valve.

        Returns
        -------
        float
            CO₂ concentration in ppm.  Returns 400 ppm when the freeze
            fault is active.
        """
        if self._co2_freeze_active:
            return self.CO2_FREEZE_VALUE_PPM
        return self._noisy_co2()

    def read_SCD41(self) -> float:
        """
        Read CO₂ concentration in ppm from the backup SCD41 NDIR sensor.

        This sensor does **not** suffer from the freeze fault and always
        returns a noisy-but-correct reading.  Use it to validate the
        primary K30 reading.

        Returns
        -------
        float
            CO₂ concentration in ppm.
        """
        return self._noisy_co2()

    def read_TEROS12(self) -> float:
        """
        Read soil moisture as volumetric water content (VWC).

        Returns
        -------
        float
            VWC in the range [0, 1].  Noise σ = 0.01.
        """
        state = self._gh.state
        vwc = state.soil_vwc + self._rng.gauss(0.0, NOISE_VWC)
        return max(0.0, min(1.0, vwc))

    def read_SQ500(self) -> float:
        """
        Read photosynthetically active radiation (PAR) at crop level.

        Returns
        -------
        float
            PAR in µmol/m²/s.  Noise σ = 10 µmol/m²/s; clamped to ≥ 0.
        """
        state = self._gh.state
        par = state.par_umol_m2_s + self._rng.gauss(0.0, NOISE_PAR_UMOL)
        return max(0.0, par)

    # ------------------------------------------------------------------
    # Fault management
    # ------------------------------------------------------------------

    def tick_faults(self, current_time_s: float, dt_seconds: float) -> None:
        """
        Advance fault state for the current simulation step.

        Call **once per tick, before reading any sensor**, to allow the fault
        state to transition correctly.

        Parameters
        ----------
        current_time_s : float
            Current simulation time in seconds.
        dt_seconds : float
            Duration of the current time step in seconds.
        """
        if self._co2_freeze_active:
            # Check whether the freeze duration has elapsed.
            if current_time_s >= self._freeze_end_time_s:
                self._co2_freeze_active = False
        else:
            # Probabilistically trigger a new freeze event.
            if self._rng.random() < self._freeze_prob:
                duration = self._rng.uniform(self._freeze_dur_min, self._freeze_dur_max)
                self._co2_freeze_active = True
                self._freeze_end_time_s = current_time_s + duration

    @property
    def co2_freeze_active(self) -> bool:
        """True when the K30 primary CO₂ sensor is currently frozen."""
        return self._co2_freeze_active

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _noisy_co2(self) -> float:
        """Return true CO₂ with Gaussian noise, clamped to ≥ 200 ppm."""
        co2 = self._gh.state.co2_ppm + self._rng.gauss(0.0, NOISE_CO2_PPM)
        return max(200.0, co2)
