# Bandwidth \& Gain bandwidth

## Bandwidth

### 1. RC Circuit

First-Order Low-Pass Filter, also known as an RC circuit is the main idea of bandwidth

### 2. Time domain (rise time)

Rise time is defined as the time it takes for the signal to go from 10% to 90% of its final value.

The equation for voltage charging up in this circuit is:

$$
V(t) = V_{max} \cdot (1 - e^{-t / \tau})
$$

where $\tau = R \cdot C$. is the *time constant*


The rise time ($t_r$) is the time required to go from 10\% to 90\% of the final value.

$$
t_r = t_{90} - t_{10} \approx 2.302\tau - 0.105\tau \approx 2.2\tau
$$

### 3. Frequency domain (bandwidth)

Bandwidth is defined as the frequency where the signal power drops by half (or voltage drops to 70.7%).

With RC circuit, the physics formula for cutoff frequency is:

$$
BW = \frac{1}{2 \pi \tau}
$$


### 4. Rise time \& bandwidth ?

$$
BW \times t_r = \left( \frac{1}{2 \pi \tau} \right) \times (2.2 \tau)
$$

$$
BW \times t_r = \frac{2.2}{2 \pi} \approx \frac{2.2}{6.283}
$$

$$
BW \times t_r \approx 0.35
$$

### Summary

$$
BW \times t_r \approx 0.35 (constant)
$$

## Gain Bandwidth