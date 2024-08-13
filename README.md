# Experiments 🧪

▶️ These experiments are conducted for the european Reindeer project and submitted to the *3rd Edition of the International Conference on 6G Networking*. The main objective here is to find out how much energy is available in the Techtile space at initial access for a certain energy neutral device. A subset of tiles (only the ceiling ones) is taken to perform the measurements. Three techniques to provide the energy during the initial access phase are compared.

## Transmitter side

### 1️⃣ Equipment
- Techtile base infrastructure N tile with RPI + USRP + PSU
- Max. 280 path antennas (917 MHz, bandwidth 20 MHz) can be used for these measurements.
- PPS and 10 MHz required for these measurements.

### 2️⃣ Controlling Techtile transmitters (non coherent)

#### Experiment details

Tiles of the ceiling are involved in following measurements.

Via this ZMQ [script](https://github.com/techtile-by-dramco/ansible/blob/main/src/server/random_phases_ZMQ.py), the server can take control over client phases and start captures.
- Send "init" --> The server will start all the client scripts.
- Send "start"
  - --> The client script will start the transmission. (Only if client script is active.)
  - --> The server will start logging the 'measurement data'.
- Send "stop" --> Alle clients scripts will be terminated.
- Send "close" --> Close the server script.

#### Script locations

The most crusial python and yaml file are listed here. With the specific "*script to control a single measurment*", a measurement is conducted like it is configured in the "config.yaml". This latter contains all settings. The parent script serves to perform multiple measurements automatically and is retrievable in "*measurements control*".  

| Script name | Info | Location |
|-|-|-|
| Client (RPI) script | Controlling USRP | [tx_waveforms_random_phase.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/tree/main/client/tx_waveforms_random_phase.py) |
| Ansible copy files | Copy config.yaml and SCRIPT_NAME.py to all hosts/clients | [copy_client_script.yaml](https://github.com/techtile-by-dramco/ansible/blob/main/experiments/copy_client_script.yaml) |
| Ansible start up | Start up all client scripts | [start_client_script.yaml](https://github.com/techtile-by-dramco/ansible/blob/main/experiments/start_client_script.yaml) |
| Script control single measurment | Control capture EP/scope/location data | [main.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/server/main.py) |
| Measurements control | Controls multiple measurements | [meas_multi_vs_single.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/meas/meas_multi_vs_single.py) |
| Config YAML file | Contains all measurement settings | [config.yaml](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/config.yaml) |
| Frequency config | Antenna center frequency configurator | [config_signal_args.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/meas/config_signal_args.py) |

<!--
❗❗ Change name of the scripts

Start transmitters
```
ansible-playbook -i inventory/hosts.yaml start_waveform.yaml -e "tiles=walls" -e "gain=100"
```
Stop transmitters
```
ansible-playbook -i inventory/hosts.yaml kill-transmitter.yaml -e tiles=walls"
```
-->

## Receiver side

The following image provides a setup overview, consisting of the Qualisys system for determining the location and the receiver antenna. The scope in the background receives the RF signals and determines the received power.

<img src="https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/energy-profiler-white.png" height="400" />

More information of the receiver, see following requirements

### 1️⃣ Equipment at the mobile receiver
- Qualisys markers for location
- Part 1: Measurement of RF levels (spectrum)
  - Receiver device --> Tektronix MSO64B
  - Receive antenna --> 917 MHz dipole antenna
- Part 2: Measuremnt harvested DC energy (Energy harvesting test IC)
  - Energy profiler [firmware/hardware files](https://github.com/techtile-by-dramco/END-design/tree/main/00-END-EF-Profiler)
  - Power bank/battery for energy profiler
  - BLE Adv. receiver board 

### 2️⃣ RSS script (calculate receive power [dBm])

Communicate with the oscilloscope and apply Parseval’s Theorem of Fourier Transform.
- Function *calc_channel_power_peaks* in [scope.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/blob/main/server/scope/scope.py) combines only the relevant spectral peaks

### 3️⃣ Script to get location in Techtile
The location will be determined via Qualisys system. 
- Qualisys system running on remote computer publishing ZeroMQ data.
- Running ZeroMQ script --> broadcasting 'timestamp' + 'xyz' location

## Combined to perform measurements

Server script [server/main.py](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/server/main.py) supports following features:
- TX Ansible instructions to control Techtile transmitters
- RX **Location script**
- RX **RSS oscilloscope script**
- RX **Energy profiler data**


### 1️⃣ Experiment 4aa PART 1: 🧪 >> Transmit signals with exactly the same frequency << 🧪

#### Purpose
- Proof occurance of dead spots in the room (This is expected, caused by frequency synchronization)
- Measure harvested power with energy profiler

Ceiling tile [A -> G][5 -> 10] could be set by using the 'all' function (in the [config.yaml](https://github.com/techtile-by-dramco/wpt-signals-for-initial-access/config.yaml) file under client/hosts/all).
```
client:
  hosts:
    all:
      freq: 920000000.0
      gain: 70
      channels: [0, 1]
      duration: 3600
```
Measurement settings
- USRP gain 70
- LO frequency 920 MHz
- Duration 3600 seconds (should be sufficient high, otherwize the relative phases between multiple USRPs will change.)

### 2️⃣ Experiment 4aa PART 2: 🧪 >> Transmit signals with exactly the same frequency and change phase randomly << 🧪

Ceiling tile [A -> G][5 -> 10] could be set by using the 'all' function.
```
client:
  hosts:
    all:
      freq: 917000000.0
      gain: 80
      channels: [0, 1]
      duration: 1
```

### 3️⃣ Experiment 4aa PART 3: 🧪 >> Random beamforming << 🧪

Ceiling tile [A -> G][5 -> 10] should be set individually by selecting a different frequency for every tile.
```
client:
  hosts:
    all:
      freq: 917000000.0
      gain: 80
      channels: [0, 1]
      duration: 1
      lo_offsets:
      - 0
      - 100
    G05:
      freq: 917000000.0
    G06:
      freq: 917500000.0
```

## Results

The results are included in the text of the manuscript.

