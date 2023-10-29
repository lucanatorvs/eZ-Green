# eZ-Green Gauge Cluster Project

This repository contains the firmware and related files for the eZ-Green gauge cluster project, designed for a BMW E36, as part of an EV conversion detailed on [vanstraatenelectric.nl](https://vanstraatenelectric.nl/projects/cluster.html). The firmware operates on an RP2040 microcontroller, interfacing with the gauge motors for precise control.

## Structure
- [Driver_FW](https://github.com/lucanatorvs/eZ-Green/tree/main/Driver_FW): Directory containing the driver firmware for the RP2040.
- [Air-core_stepper_motor_LUT_generator.ipynb](https://github.com/lucanatorvs/eZ-Green/blob/main/Air-core_stepper_motor_LUT_generator.ipynb): Notebook for generating Look-Up Table (LUT) for air-core stepper motor.
- [Face](https://github.com/lucanatorvs/eZ-Green/tree/main/Face): Directory containing design files for the gauge face.
- [GUI](https://github.com/lucanatorvs/eZ-Green/tree/main/GUI): Directory containing the GUI script.
- [eZ-E36-brakeout](https://github.com/lucanatorvs/eZ-Green/tree/main/eZ-E36-brakeout): Directory containing files for the breakout board design.
- [eZ-Green-Driver](https://github.com/lucanatorvs/eZ-Green/tree/main/eZ-Green-Driver): Directory containing files for the driver board design.


## Getting Started

```bash
git clone https://github.com/lucanatorvs/eZ-Green.git
```

## Usage

Refer to the [project page](https://vanstraatenelectric.nl/projects/cluster.html) for more information on the project.

## Contributing

Feel free to open an issue or submit a Pull Request.

## License

This project is licensed under the MIT License:

```text
Copyright 2023 Luca van Straaten (lucanatorvs)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```