# Conversion Calculator

A desktop rate and pay conversion calculator built with Python and PySide6 that supports two-way currency conversion alongside real-time calculations across hourly, daily, weekly, bi-monthly, and monthly periods[cite: 2, 4, 5].

## Features

* **Two-Way Currency Conversion:** Adjust the conversion rate or edit either currency's hourly rate to automatically update the counterpart value and downstream totals.
* **Multi-Period Breakdown:** Calculates values step-by-step across **per hour**, **per day** (using editable hours), **per week** (using editable days), **per bi month** (`× 2`), and **per month** (`× 2`)[cite: 2, 4, 5].
* **Clear Input vs. Read-Only Fields:** Editable inputs are distinct from read-only fixed and calculated fields, while keeping read-only values selectable and easy to copy.
* **Quick Actions:** Includes **Swap** to exchange currencies and rates, and **Reset** to restore default values.

## Requirements

* Python 3.9+
* `PySide6`

## Installation

Install the required dependency:

```bash
pip install PySide6
