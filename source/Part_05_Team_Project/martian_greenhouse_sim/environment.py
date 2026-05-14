"""
Martian external environment model based on REMS (Rover Environmental
Monitoring Station) data patterns.

Provides:
  - Diurnal temperature cycle (sine wave): highs ~ -5 °C, lows ~ -70 °C.
  - Diurnal solar irradiance (half-wave rectified sine, Mars-attenuated).
  - Global dust storm events that raise atmospheric opacity (Tau) and reduce
    incident solar radiation by up to 97 %.

Usage
-----
    env = MarsEnvironment(rng=random.Random(42))
    env.schedule_dust_storm(start_time_s=5 * SOL_SECONDS, duration_s=3 * SOL_SECONDS)

    for step in range(n_steps):
        env.update(dt_seconds=60)
        print(env.get_temperature_c(), env.get_solar_irradiance_w_per_m2())
"""

import math
import random
from dataclasses import dataclass
from typing import Optional

from .constants import (
    I_PEAK_MARS,
    SOL_SECONDS,
    T_AMPLITUDE_C,
    T_MEAN_C,
    T_PHASE,
    TAU_CLEAR,
    TAU_REDUCTION_MAX,
    TAU_STORM_MAX,
    TAU_STORM_MIN,
)


@dataclass
class DustStorm:
    """Records the schedule and peak intensity of a single dust storm event."""

    start_time_s: float   #: Simulation time (s) at which the storm begins.
    end_time_s: float     #: Simulation time (s) at which the storm clears.
    peak_tau: float       #: Maximum atmospheric opacity reached during the storm.


class MarsEnvironment:
    """
    Simulates external Martian atmospheric and solar conditions.

    Temperature model
    -----------------
    A sinusoidal diurnal cycle over one Martian sol (88 775 s):

        T_out(t) = T_mean + T_amp * sin(2π·t/sol − π/2)

    where T_mean = −37.5 °C and T_amp = 32.5 °C, yielding a maximum of
    −5 °C at local noon and a minimum of −70 °C at local midnight.

    Solar irradiance model
    ----------------------
    Clear-sky irradiance follows a half-wave rectified sine (zero at night):

        I_clear(t) = I_peak_mars × max(0, sin(2π·t/sol − π/2))

    Dust storms increase the atmospheric opacity (Tau) from a clear-sky
    baseline of 0.5 up to 5.0 – 8.5, linearly reducing transmittance so
    that at peak opacity the incident solar is reduced by up to 97 %:

        transmittance(τ) = 1 − 0.97 × (τ − 0.5) / 8.0

    Parameters
    ----------
    rng : random.Random, optional
        Random number generator for storm parameter sampling.  Pass a seeded
        instance for reproducible runs.
    initial_time_s : float
        Starting simulation time in seconds (default 0 = Martian midnight).
    """

    def __init__(
        self,
        rng: Optional[random.Random] = None,
        initial_time_s: float = 0.0,
    ) -> None:
        self._time_s: float = initial_time_s
        self._rng: random.Random = rng if rng is not None else random.Random()
        self._tau: float = TAU_CLEAR
        self._active_storm: Optional[DustStorm] = None

    # ------------------------------------------------------------------
    # Time
    # ------------------------------------------------------------------

    def update(self, dt_seconds: float) -> None:
        """Advance simulation time by *dt_seconds* and refresh storm state."""
        self._time_s += dt_seconds
        self._update_storm_tau()

    def get_time_s(self) -> float:
        """Return the current simulation time in seconds."""
        return self._time_s

    def get_sol(self) -> float:
        """Return the current simulation time expressed as a fractional sol."""
        return self._time_s / SOL_SECONDS

    # ------------------------------------------------------------------
    # Atmospheric state
    # ------------------------------------------------------------------

    def get_temperature_c(self) -> float:
        """
        Return the external Martian air temperature (°C).

        Follows a sinusoidal diurnal cycle with a high of ~ −5 °C at noon
        and a low of ~ −70 °C at midnight.
        """
        phase_angle = 2.0 * math.pi * self._time_s / SOL_SECONDS - T_PHASE
        return T_MEAN_C + T_AMPLITUDE_C * math.sin(phase_angle)

    def get_solar_irradiance_w_per_m2(self) -> float:
        """
        Return incident solar irradiance at the greenhouse surface (W/m²).

        Accounts for the Martian solar attenuation factor (43 % of Earth),
        the diurnal solar angle, and the current atmospheric opacity (Tau).
        Returns 0 during night hours.
        """
        clear_sky = self._clear_sky_irradiance()
        return clear_sky * self._solar_transmittance()

    def get_tau(self) -> float:
        """Return the current atmospheric opacity (Tau)."""
        return self._tau

    def is_daytime(self) -> bool:
        """
        Return True when the sun is above the horizon.

        Uses the clear-sky (Tau-independent) solar elevation to classify
        day/night, so a dust storm does not convert 'day' into 'night'.
        """
        return self._clear_sky_irradiance() > 0.0

    # ------------------------------------------------------------------
    # Dust storm scheduling
    # ------------------------------------------------------------------

    def schedule_dust_storm(
        self,
        start_time_s: float,
        duration_s: float,
        peak_tau: Optional[float] = None,
    ) -> DustStorm:
        """
        Schedule a global dust storm event.

        The storm opacity ramps up during the first 10 % of its duration,
        holds at *peak_tau* for the middle 80 %, then ramps back down over
        the last 10 %.

        Parameters
        ----------
        start_time_s : float
            Simulation time (s) at which the storm begins.
        duration_s : float
            Total storm duration in seconds.
        peak_tau : float, optional
            Peak atmospheric opacity.  Sampled from [TAU_STORM_MIN,
            TAU_STORM_MAX] if not provided.

        Returns
        -------
        DustStorm
            The scheduled storm descriptor.
        """
        if peak_tau is None:
            peak_tau = self._rng.uniform(TAU_STORM_MIN, TAU_STORM_MAX)
        storm = DustStorm(
            start_time_s=start_time_s,
            end_time_s=start_time_s + duration_s,
            peak_tau=peak_tau,
        )
        self._active_storm = storm
        return storm

    def get_active_storm(self) -> Optional[DustStorm]:
        """Return the scheduled DustStorm descriptor, or None."""
        return self._active_storm

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _clear_sky_irradiance(self) -> float:
        """Solar irradiance ignoring opacity — zero at night, peak at noon."""
        phase_angle = 2.0 * math.pi * self._time_s / SOL_SECONDS - T_PHASE
        return I_PEAK_MARS * max(0.0, math.sin(phase_angle))

    def _solar_transmittance(self) -> float:
        """
        Map current Tau to a solar transmittance factor in
        [1 − TAU_REDUCTION_MAX, 1.0].

            transmittance = 1 − 0.97 × (τ − 0.5) / (8.5 − 0.5)

        At τ = 0.5 (clear sky) : transmittance = 1.00
        At τ = 8.5 (peak storm): transmittance = 0.03  (97 % reduction)
        """
        tau_range = TAU_STORM_MAX - TAU_CLEAR
        storm_progress = max(0.0, min(1.0, (self._tau - TAU_CLEAR) / tau_range))
        return 1.0 - TAU_REDUCTION_MAX * storm_progress

    def _update_storm_tau(self) -> None:
        """Update self._tau based on the active storm schedule."""
        storm = self._active_storm
        if storm is None:
            self._tau = TAU_CLEAR
            return

        t = self._time_s
        if t < storm.start_time_s or t >= storm.end_time_s:
            self._tau = TAU_CLEAR
            return

        duration = storm.end_time_s - storm.start_time_s
        elapsed_frac = (t - storm.start_time_s) / duration

        # Trapezoidal envelope: ramp up 0–10 %, flat 10–90 %, ramp down 90–100 %
        if elapsed_frac < 0.1:
            envelope = elapsed_frac / 0.1
        elif elapsed_frac > 0.9:
            envelope = (1.0 - elapsed_frac) / 0.1
        else:
            envelope = 1.0

        self._tau = TAU_CLEAR + (storm.peak_tau - TAU_CLEAR) * envelope
