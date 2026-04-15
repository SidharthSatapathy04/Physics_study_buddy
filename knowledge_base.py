"""
Physics Study Buddy Knowledge Base
12 comprehensive documents covering core B.Tech Physics topics
Each document: 150-400 words, one specific topic, accurate formulas and definitions
"""

DOCUMENTS = [
    {
        "id": "doc_001",
        "topic": "Newton's Laws of Motion",
        "text": "Newton's Laws of Motion form the foundation of classical mechanics. The First Law states that an object at rest remains at rest and an object in motion continues with constant velocity unless acted upon by an external force. This property is called inertia. The Second Law is expressed as F = ma, where force equals mass times acceleration. This means acceleration is directly proportional to the net force applied and inversely proportional to the mass. The Third Law states that for every action, there is an equal and opposite reaction. When forces are balanced, the net force is zero and the object is in equilibrium. Friction is a resistive force opposing motion between surfaces in contact. Static friction prevents motion until overcome by applied force: fs ≤ μs × N. Kinetic friction acts during motion: fk = μk × N, where μ is the coefficient of friction and N is the normal force. Understanding these laws enables us to analyze motion of objects in everyday situations—from vehicles accelerating to blocks sliding on inclined planes. Applications include calculating forces needed for given accelerations, determining equilibrium conditions, and understanding how friction affects motion in real-world scenarios."
    },
    {
        "id": "doc_002",
        "topic": "Kinematics and Equations of Motion",
        "text": "Kinematics describes motion without considering forces. The four SUVAT equations relate displacement (s), initial velocity (u), final velocity (v), acceleration (a), and time (t). These are: v = u + at; s = ut + (1/2)at²; v² = u² + 2as; s = (u + v)t/2. These equations apply to uniform acceleration in one dimension. Velocity-time (v-t) graphs show velocity on the vertical axis and time horizontally; the slope gives acceleration and the area under the curve gives displacement. Displacement-time (s-t) graphs show position versus time; the slope at any point gives instantaneous velocity. Projectile motion describes an object launched with an initial velocity under gravity. The horizontal velocity remains constant (vx = v₀ cos θ) while vertical velocity changes as vy = v₀ sin θ - gt. Time of flight is t = 2v₀ sin θ / g. Maximum height is h = (v₀ sin θ)² / 2g. Range is R = v₀² sin(2θ) / g. These concepts are essential for analyzing athlete performance, ballistics, and orbital mechanics."
    },
    {
        "id": "doc_003",
        "topic": "Work, Energy and Power",
        "text": "Work is defined as W = F × d × cos θ, where force and displacement form angle θ. Energy exists in multiple forms: kinetic energy KE = (1/2)mv², potential energy PE = mgh (gravitational) or PE = (1/2)kx² (elastic spring). The work-energy theorem states that net work equals change in kinetic energy: W = ΔKE. Conservation of energy dictates that in an isolated system, total mechanical energy remains constant: KE + PE = constant. During collisions and deformations, some mechanical energy converts to heat and sound—this is explained through inelastic collisions. Power is the rate of energy transfer: P = W/t (average power) or P = dW/dt (instantaneous power). Measured in watts (J/s), power indicates how quickly work is performed. Efficiency η = (useful energy output / total energy input) × 100%. Real machines have efficiency less than 100% due to friction and other losses. In an ideal pulley system, mechanical advantage MA = output force / input force = length of effort / length of load. These principles apply to engines, motors, and everyday machines like inclined planes and levers."
    },
    {
        "id": "doc_004",
        "topic": "Gravitation and Orbital Motion",
        "text": "Newton's Law of Universal Gravitation states F = G(m₁m₂)/r², where G = 6.674 × 10⁻¹¹ N⋅m²/kg² is the gravitational constant. This describes the attractive force between any two masses. The gravitational field strength is g = GM/r², where g ≈ 9.8 m/s² at Earth's surface. Escape velocity is the minimum speed needed to escape a planet's gravity: ve = √(2GM/R). Orbital velocity for circular orbits is v = √(GM/r). Kepler's Three Laws describe planetary motion: (1) planets orbit in ellipses with the sun at one focus; (2) a line from sun to planet sweeps equal areas in equal times (L = mvr = constant for circular orbits); (3) T² ∝ r³ or T² = (4π²/GM)r³. For geostationary satellites, orbital period equals Earth's rotation period (24 hours), requiring an orbital radius of 42,164 km from Earth's center. These satellites maintain fixed positions above the equator. Understanding gravitation is crucial for satellite design, space missions, and studying celestial mechanics."
    },
    {
        "id": "doc_005",
        "topic": "Thermodynamics—Laws and Processes",
        "text": "The Zeroth Law states that if two systems are each in thermal equilibrium with a third, they are in equilibrium with each other—this defines temperature. The First Law is the law of energy conservation: ΔU = Q - W, where internal energy change equals heat absorbed minus work done by the system. The Second Law states that entropy of an isolated system always increases: ΔS ≥ 0. Four fundamental thermodynamic processes: Isothermal (constant T, ΔU = 0, Q = W = nRT ln(Vf/Vi)); Adiabatic (Q = 0, W = nCvΔT); Isobaric (constant P, W = PΔV); Isochoric (constant V, W = 0, Q = nCvΔT). Carnot efficiency is the maximum for any heat engine: η = 1 - (Tc/Th), where Tc and Th are cold and hot reservoir temperatures in Kelvin. Specific heat capacity c = Q/(m⋅ΔT) is energy needed to raise 1 kg by 1 K. Latent heat L = Q/m is energy for phase change without temperature change. The equation of state for ideal gas is PV = nRT. Applications include designing engines, refrigerators, and understanding atmospheric processes."
    },
    {
        "id": "doc_006",
        "topic": "Waves and Simple Harmonic Motion",
        "text": "Waves are disturbances that propagate through media. Wave speed v = f × λ, where f is frequency (Hz) and λ is wavelength (m). Transverse waves oscillate perpendicular to propagation (e.g., light, water waves); longitudinal waves oscillate parallel (e.g., sound). Intensity I = P/A (power per unit area), and I ∝ (amplitude)². Simple Harmonic Motion (SHM) satisfies a = -ω²x, where ω = 2πf is angular frequency. Displacement in SHM: x(t) = A sin(ωt + φ); velocity v(t) = Aω cos(ωt + φ); acceleration a(t) = -Aω² sin(ωt + φ). Total energy in SHM: E = (1/2)kA² = (1/2)mω²A². A simple pendulum has period T = 2π√(L/g) for small angles. A mass-spring system has T = 2π√(m/k). The Doppler effect describes frequency shift when source or observer moves: f' = f(v ± vobserver)/(v ± vsource). Applications include understanding musical instruments, seismic waves, medical ultrasound, and radar."
    },
    {
        "id": "doc_007",
        "topic": "Electrostatics",
        "text": "Coulomb's Law describes the electrostatic force between charges: F = k|q₁q₂|/r², where k = 8.99 × 10⁹ N⋅m²/C². The electric field E = F/q represents force per unit positive charge: E = kQ/r² for a point charge. Electric potential V = U/q is energy per unit charge: V = kQ/r for a point charge, measured in volts. Potential difference is ΔV = Vb - Va = -∫ E·dl. Gauss's Law states ∮ E·dA = Qenc/ε₀, where ε₀ = 8.854 × 10⁻¹² F/m is permittivity of free space. For conductors in electrostatic equilibrium, E = 0 inside and charge resides on surface. Capacitance C = Q/V is charge per unit voltage, measured in farads: C = ε₀A/d for a parallel-plate capacitor. Energy stored: U = (1/2)CV² = (1/2)QV. Dielectrics placed between plates increase capacitance by factor κ (relative permittivity): C = κε₀A/d. Applications include sensor design, energy storage, touchscreens, and understanding atmospheric electricity."
    },
    {
        "id": "doc_008",
        "topic": "Current Electricity",
        "text": "Electric current I = dQ/dt is charge flow rate, measured in amperes. Ohm's Law states V = IR, where resistance R = ρL/A depends on resistivity ρ, length L, and cross-sectional area A. Temperature affects resistance: R = R₀[1 + α(T - T₀)] where α is temperature coefficient. Resistivity ρ = 1/σ where σ is conductivity. Power dissipation P = VI = I²R = V²/R. In series circuits, currents are equal and voltages add; total resistance Rs = R₁ + R₂ + ... In parallel circuits, voltages are equal and currents add; 1/Rp = 1/R₁ + 1/R₂ + ... Kirchhoff's Current Law: Iin = Iout (conservation of charge at a junction). Kirchhoff's Voltage Law: ∑V around closed loop = 0 (conservation of energy). EMF (ε) drives current; terminal voltage V = ε - Ir where r is internal resistance. The Wheatstone bridge is balanced when R₁/R₂ = R₃/R₄, producing zero current through detector. Applications include circuit analysis, power distribution, and electrical measurements."
    },
    {
        "id": "doc_009",
        "topic": "Magnetic Effects and Electromagnetic Induction",
        "text": "The Lorentz force on a moving charge is F = q(v × B), perpendicular to both velocity and magnetic field. For a current-carrying wire: F = I(L × B) where L is length vector. The Biot-Savart Law gives magnetic field from current element: dB = (μ₀I dl × r)/(4πr³), where μ₀ = 4π × 10⁻⁷ T⋅m/A. A solenoid with n turns produces field B = μ₀nI inside. Faraday's Law describes electromagnetic induction: ε = -dΦ/dt where Φ is magnetic flux (Φ = B⋅A). Lenz's Law states induced current opposes flux change. Motional EMF: ε = Blv when conductor moves in magnetic field. Self-inductance L describes coil's opposition to current change: ε = -L(dI/dt). Mutual inductance M describes induction between circuits: ε₂ = -M(dI₁/dt). Energy stored in inductor: U = (1/2)LI². AC generators produce sinusoidal EMF; transformers transfer energy between circuits with different voltages: Vs/Vp = Ns/Np. Applications include motors, generators, transformers, and wireless charging."
    },
    {
        "id": "doc_010",
        "topic": "Ray Optics",
        "text": "The law of reflection states angle of incidence equals angle of reflection on a plane surface. For curved mirrors, the mirror equation is 1/f = 1/u + 1/v, where f is focal length, u is object distance, v is image distance. Magnification m = -v/u = hi/ho (negative for real images). A concave mirror (f > 0) converges rays; a convex mirror (f < 0) diverges rays. Snell's Law describes refraction at interface: n₁ sin θ₁ = n₂ sin θ₂ where n is refractive index. Critical angle θc for total internal reflection: sin θc = n₂/n₁ (when light goes from denser to less dense medium). For lenses, thin lens equation is identical: 1/f = 1/u + 1/v. Lens power P = 1/f (diopters = m⁻¹). A convex lens (f > 0) converges rays; concave lens (f < 0) diverges rays. Lens maker's equation: 1/f = (n - 1)(1/R₁ - 1/R₂). Eye defects: myopia (short sight) corrected with concave lens; hyperopia (far sight) with convex lens. Applications include cameras, microscopes, telescopes, and vision correction."
    },
    {
        "id": "doc_011",
        "topic": "Modern Physics—Photoelectric Effect and Quantum Theory",
        "text": "Einstein's photoelectric equation is hf = Φ + KEmax, where hf is photon energy, Φ is work function, KEmax is maximum electron kinetic energy. Here h = 6.626 × 10⁻³⁴ J⋅s is Planck's constant. The stopping potential Vs satisfies eVs = KEmax. Threshold frequency f₀ = Φ/h; photons below this frequency cannot eject electrons. De Broglie wavelength relates particle momentum to wave properties: λ = h/p where p = mv. Heisenberg Uncertainty Principle states ΔxΔp ≥ h/(4π); we cannot simultaneously know position and momentum precisely. The Bohr model for hydrogen gives energy levels En = -13.6 eV / n². Transitions between levels emit/absorb photons: hf = E₂ - E₁. The Rydberg formula for hydrogen spectrum: 1/λ = R(1/n₁² - 1/n₂²) where R = 1.097 × 10⁷ m⁻¹. Principal spectral series: Lyman (n₁=1, UV), Balmer (n₁=2, visible), Paschen (n₁=3, IR). Applications include photodiodes, LED displays, solar cells, and understanding atomic structure."
    },
    {
        "id": "doc_012",
        "topic": "Nuclear Physics",
        "text": "Radioactive decay describes spontaneous nuclear transformations. Alpha decay (α): nucleus emits ⁴₂He, reducing mass and atomic number. Beta-minus (β⁻) decay: neutron converts to proton plus electron (antineutrino), increasing atomic number. Beta-plus (β⁺) decay: proton converts to neutron plus positron and neutrino. Gamma (γ) decay: nucleus emits high-energy photon. The decay law is N(t) = N₀e⁻ᵏᵗ where λ is decay constant. Half-life t₁/₂ = ln(2)/λ = 0.693/λ is time for half the nuclei to decay. Binding energy BE = (Zmp + Nmn - mnucleus)c² represents energy holding nucleus together. Higher BE/A (binding energy per nucleon) means greater nuclear stability. Nuclear fission splits heavy nuclei (e.g., ²³⁵U), releasing energy. Nuclear fusion combines light nuclei (e.g., deuterium + tritium), also releasing energy. Both processes follow E = mc² where c = 3 × 10⁸ m/s. Applications include medical imaging (PET, gamma cameras), power generation, cancer treatment, and dating archaeological artifacts."
    }
]

if __name__ == "__main__":
    print(f"✅ Knowledge base loaded: {len(DOCUMENTS)} documents")
    for doc in DOCUMENTS:
        word_count = len(doc["text"].split())
        print(f"  {doc['id']}: {doc['topic']} — {word_count} words")
