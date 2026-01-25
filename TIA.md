# Timing & requirements

## How to choose Transimpedance Amplifier

Based on [Texas Instruments Guide](https://www.youtube.com/watch?v=Q-AZpagmtCw)

https://www.youtube.com/watch?v=33C8MmsCBuc

https://www.mouser.com/c/semiconductors/amplifier-ics/transimpedance-amplifiers/?sort=pricing

### 1. Choose Rf
Choose $R_F$ based on your desired output voltage (sensitivity).

### 2. Choose Cf
Calculate $C_F$ to limit the bandwidth.

$$
C_F \approx \frac{1}{2 \pi \cdot R_F \cdot \text{BW}}
$$

### 3. Choose OpAmps
Now, calculate the Minimum GBW required to support that $R_F$ and $C_F$ without oscillating.

$$
GBW_{required} > \frac{C_{in} + C_F}{2\pi \cdot R_F \cdot C_F^2}
$$

## How to calculate rise time of the signal


https://www.jensign.com/AD8065/

![alt text](image.png)

https://www.ti.com/lit/ds/symlink/dac6571.pdf?ts=1769360583183&ref_url=https%253A%252F%252Fwww.mouser.com%252F