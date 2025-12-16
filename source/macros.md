```{role} matlab(code)
:language: matlab
```
```{role} python(code)
:language: python
```
% This is a hack to add the Bootstrap "d-none" class to these math macros so
% that they won't take up any space on the page. Once myst-parser 0.19 or
% greater is available, we will be able to use block attributes to do this by
% simply placing {.d-none} above the math directive.
%
% https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-attributes-block

```{role} raw-html(raw)
:format: html
```
{raw-html}`<div class="d-none">`
%{.d-none}
```{math}

\newcommand\blank{~\underline{\hspace{1.2cm}}~}

% Bold symbols (vectors)
\newcommand\bs[1]{\mathbf{#1}}

% Differential
\newcommand\dd[2][]{\mathrm{d}^{#1}{#2}}  % use as \dd, \dd{x}, or \dd[2]{x}

% Poor man's siunitx
\newcommand\unit[1]{\mathrm{#1}}
\newcommand\num[1]{#1}
\newcommand\qty[2]{#1~\unit{#2}}

\newcommand\per{/}
\newcommand\squared{{}^2}
\newcommand\cubed{{}^3}
%
% Scale
\newcommand\milli{\unit{m}}
\newcommand\centi{\unit{c}}
\newcommand\kilo{\unit{k}}
\newcommand\mega{\unit{M}}
%
% Percent
\newcommand\percent{\unit{{\kern-4mu}\%}}
%
% Angle
\newcommand\radian{\unit{rad}}
\newcommand\degree{\unit{{\kern-4mu}^\circ}}
%
% Time
\newcommand\second{\unit{s}}
\newcommand\s{\second}
\newcommand\minute{\unit{min}}
\newcommand\hour{\unit{h}}
%
% Distance
\newcommand\meter{\unit{m}}
\newcommand\m{\meter}
\newcommand\inch{\unit{in}}
\newcommand\foot{\unit{ft}}
%
% Force
\newcommand\newton{\unit{N}}
\newcommand\kip{\unit{kip}} % kilopound in "freedom" units - edit made by Sri
%
% Mass
\newcommand\gram{\unit{g}}
\newcommand\g{\gram}
\newcommand\kilogram{\unit{kg}}
\newcommand\kg{\kilogram}
\newcommand\grain{\unit{grain}}
\newcommand\ounce{\unit{oz}}
%
% Temperature
\newcommand\kelvin{\unit{K}}
\newcommand\K{\kelvin}
\newcommand\celsius{\unit{{}^\circ C}}
\newcommand\C{\celsius}
\newcommand\fahrenheit{\unit{{}^\circ F}}
\newcommand\F{\fahrenheit}
%
% Area
\newcommand\sqft{\unit{sq\,\foot}}  % square foot
%
% Volume
\newcommand\liter{\unit{L}}
\newcommand\gallon{\unit{gal}}
%
% Frequency
\newcommand\hertz{\unit{Hz}}
\newcommand\rpm{\unit{rpm}}
%
% Voltage
\newcommand\volt{\unit{V}}
\newcommand\V{\volt}
\newcommand\millivolt{\milli\volt}
\newcommand\mV{\milli\volt}
\newcommand\kilovolt{\kilo\volt}
\newcommand\kV{\kilo\volt}
%
% Current
\newcommand\ampere{\unit{A}}
\newcommand\A{\ampere}
\newcommand\milliampereA{\milli\ampere}
\newcommand\mA{\milli\ampere}
\newcommand\kiloampereA{\kilo\ampere}
\newcommand\kA{\kilo\ampere}
%
% Resistance
\newcommand\ohm{\Omega}
\newcommand\milliohm{\milli\ohm}
\newcommand\kiloohm{\kilo\ohm} % correct SI spelling
\newcommand\kilohm{\kilo\ohm} % "American" spelling used in siunitx
\newcommand\megaohm{\mega\ohm} % correct SI spelling
\newcommand\megohm{\mega\ohm} % "American" spelling used in siunitx
%
% Capacitance
\newcommand\farad{\unit{F}}
\newcommand\F{\farad}
\newcommand\microfarad{\micro\farad}
\newcommand\muF{\micro\farad}
%
% Inductance
\newcommand\henry{\unit{H}}
\newcommand\H{\henry}
\newcommand\millihenry{\milli\henry}
\newcommand\mH{\milli\henry}
%
% Power
\newcommand\watt{\unit{W}}
\newcommand\W{\watt}
\newcommand\milliwatt{\milli\watt}
\newcommand\mW{\milli\watt}
\newcommand\kilowatt{\kilo\watt}
\newcommand\kW{\kilo\watt}
%
% Energy
\newcommand\joule{\unit{J}}
\newcommand\J{\joule}
%
% Composite units
%
% Torque
\newcommand\ozin{\unit{\ounce}\,\unit{in}}
\newcommand\newtonmeter{\unit{\newton\,\meter}}
%
% Pressure
\newcommand\psf{\unit{psf}}  % pounds per square foot
\newcommand\pcf{\unit{pcf}}  % pounds per cubic foot
\newcommand\pascal{\unit{Pa}}
\newcommand\Pa{\pascal}
\newcommand\ksi{\unit{ksi}} % kilopound per square inch
\newcommand\bar{\unit{bar}}

```
{raw-html}`</div>`

{sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read
