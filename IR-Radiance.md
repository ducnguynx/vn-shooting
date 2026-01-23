# IR Radiance calculation at the sensor

### 1. Total Irradiance

The final Irradiance ($E_{total}$) at the sensor is the product of the axial intensity, distance loss, and angular loss factors:

$$E_{total} = \frac{I_e}{d^2} \times L(\theta) \times S(\alpha)$$

Where:
* $E_{total}$: Irradiance falling on the sensor (mW/cm²).
* $I_e$: Radiant Intensity of the LED at 0° (mW/sr) (with current sensor 1025 mW/sr)
* $d$: Distance between LED and Sensor (cm).
* $L(\theta)$: Normalized emission pattern of the LED.
* $S(\alpha)$: Normalized sensitivity pattern of the Sensor.

---

### 2. Angular Approximations

Neither component is linear. Their behavior is best modeled using the Cosine Power Law approximation:

$$f(\phi) \approx \cos^n(\phi)$$

We can derive the coefficient **$n$** for each component using the "Angle of Half Intensity" ($\phi_{1/2}$) provided in the datasheets, where the signal drops to 0.5 (50%).

$$0.5 = \cos^n(\phi_{1/2}) \implies n = \frac{\ln(0.5)}{\ln(\cos(\phi_{1/2}))}$$

#### A. The Emitter (VSMA1094400X02)
* Half Angle ($\phi_{1/2}$): $\pm 40^{\circ}$
* Calculation:
    $$n_{LED} = \frac{\ln(0.5)}{\ln(\cos(40^{\circ}))} \approx \frac{-0.693}{-0.266} \approx \mathbf{2.6}$$
* Resulting Function:
    $$L(\theta) \approx \cos^{2.6}(\theta)$$

#### B. The Sensor (VEMD1160X01)
* Half Angle ($\phi_{1/2}$): $\pm 70^{\circ}$
* Calculation:
    $$n_{Sensor} = \frac{\ln(0.5)}{\ln(\cos(70^{\circ}))} \approx \frac{-0.693}{-1.073} \approx \mathbf{0.65}$$
* Resulting Function:
    $$S(\alpha) \approx \cos^{0.65}(\alpha)$$


---
