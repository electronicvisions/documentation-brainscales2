(halco)=
# Introduction to the BrainScaleS Coordinate Systems

For configuration it is essential to be able to address different hardware entities uniquely.
Therefore, the coordinate system `halco` was introduced for the BrainScaleS system.

## Repeated Components

In the BrainScaleS system there exist components which are repeated several times in the system.
These components are numbered in the [row-major](https://en.wikipedia.org/wiki/Row-_and_column-major_order).
As the number of each component in the system is known, the corresponding coordinates are restricted to ranges.

### BrainScaleS-1 example

BrainScales-1 is a wafer scale system.
The neuromorphic chips (called HICANN) are connected on the silicon wafer to form large networks.
The coordinate {cpp:class}`halco::hicann::v2::HICANNOnWafer` refers to a single chip on a BrainScaleS-1 wafer.
Since the wafer is composed of 384 chips, the coordinate is restricted to the range from 0 to 383.
According to the row major ordering the chip on the top left has the number 0; the chip to the right number 1 and so on.


### BrainScaleS-2 example

On BrainScaleS-2 neuron circuits are organized in a 2D-grid of 2x256 circuits.
The coordinate connected to a single neuron circuit is the {cpp:class}`halco::hicann_dls::vx::v2::AtomicNeuronOnDLS`.
The neuron on the top left has number 0; the one to the right of right number 1 and so on.

## Component Hierarchy

The "repeated circuits" described in the previous section  might themselves be part of a larger hardware component which is repeated several times.
`halco` allows to reference to these circuits at different levels of abstraction by combining several coordinates.

### BrainScaleS-1 example

{cpp:class}`halco::hicann::v2::NeuronOnHICANN` represents a neuron circuit on a single neuromorphic chip.
In order to refer to a specific neuron circuit on the wafer the coordinate {cpp:class}`halco::hicann::v2::NeuronOnWafer` is used which is a combination of the coordinates {cpp:class}`halco::hicann::v2::NeuronOnHICANN` and {cpp:class}`halco::hicann::v2::HICANNOnWafer`.

### BrainScaleS-2 example

The BrainScaleS-2 chip is composed of an upper and lower half (called hemispheres).
On each hemisphere are two analog parameter storages (CapMemBlock) referenced by the coordinate {cpp:class}`halco::hicann_dls::vx::v2::CapMemBlockOnHemisphere`.
To identify an analog parameter storage on the chip this coordinate is combined with {cpp:class}`halco::hicann_dls::vx::v2::HemisphereOnDLS` to form {cpp:class}`halco::hicann_dls::vx::v2::CapMemBlockOnDLS`.

## Coordinate Transformation

`halco` offers the possibility to convert between different coordinates.
This is done by providing member functions with the name `to<new_coordinate>`.
Lets take the examples from above and show how the coordinate transformation works.

```python
# BrainScaleS-1
enum = halco.common.Enum(512)  # first neuron on second HICANN
neuron_on_wafer = halco.NeuronOnWafer(enum)
neuron_on_hicann = neuron_on_wafer.toNeuronOnHICANN()
assert neuron_on_hicann == halco.NeuronOnHICANN(halco.common.Enum(0))

# BrainScaleS-2
capmem_on_chip = halco.CapMemBlockOnDLS(3)
campmem_on_hemisphere = capmem_on_chip.toCapMemBlockOnHemisphere()
assert campmem_on_hemisphere == halco.CapMemBlockOnHemisphere(1)
```
