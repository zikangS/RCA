- [srsRAN Setup](#srsran-setup)
  - [1. Install USRP driver (before cmake)](#1-install-usrp-driver-before-cmake)
    - [if driver installed before cmake](#if-driver-installed-before-cmake)
  - [2. srsGUI(optional)](#2-srsguioptional)
    - [cmake and install](#cmake-and-install)
    - [Installation verification](#installation-verification)
    - [Setting Environment Variables](#setting-environment-variables)
  - [3. cmake and install srsRAN](#3-cmake-and-install-srsran)
    - [If srsGUI installed](#if-srsgui-installed)
  - [4. Update shared library](#4-update-shared-library)
  - [5. Try c programs in lib/example](#5-try-c-programs-in-libexample)
    - [cmake cannot find fftw](#cmake-cannot-find-fftw)
    - [cell\_search](#cell_search)
  - [6. FALCON](#6-falcon)
    - [Dependency](#dependency)
    - [Cmake \& installation](#cmake--installation)
  - [some commands](#some-commands)
  - [memo](#memo)

# srsRAN Setup
## 1. Install USRP driver (before cmake)
[Official driver](https://github.com/EttusResearch/uhd)  
[Official installation guide](https://files.ettus.com/manual/page_install.html)  

Connecting USRP to update firmware and download FPGA image: 
> uhd_images_downloader

### if driver installed before cmake
<details>
<summary>Only some srsRAN components will be installed, this can be observed in installation log and config generation log.</summary>
> srsran_install_configs.sh user  

```
Installing srsRAN configuration files:
 - /usr/local/share/srsran/ue.conf.example doesn't exists. Skipping it.
 - /usr/local/share/srsran/enb.conf.example doesn't exists. Skipping it.
 - /usr/local/share/srsran/sib.conf.example doesn't exists. Skipping it.
 - /usr/local/share/srsran/rr.conf.example doesn't exists. Skipping it.
 - /usr/local/share/srsran/rb.conf.example doesn't exists. Skipping it.
 - /root/.config/srsran/epc.conf already exists. Skipping it.
 - /root/.config/srsran/mbms.conf already exists. Skipping it.
 - /root/.config/srsran/user_db.csv already exists. Skipping it.
Done.
```
And same symptoms like <https://github.com/srsran/srsRAN_4G/discussions/1305>:  
Instead of installing another driver, install USRP driver and redo make.
</details>

## 2. srsGUI(optional)
### cmake and install
<https://github.com/srsran/srsgui>  
### Installation verification
> ls /usr/local/lib/libsrs*.so  
> ls /usr/local/include/srsgui
### Setting Environment Variables
1. Dynamic Library Path (needed at runtime):  
> export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
2. Header File Path (needed at compile-time):  
> export CXXFLAGS="-I/usr/local/include" 
> export LDFLAGS="-L/usr/local/lib"




## 3. cmake and install srsRAN
Chose to make because no apt package, only ppa snap for Ubuntu.  
[Offical guide](https://docs.srsran.com/projects/4g/en/latest/general/source/1_installation.html)
### If srsGUI installed
Add parameters behind `cmake ../`:  
> cmake ../ -DUSE_SRSGUI=ON -DCMAKE_PREFIX_PATH=/usr/local  
Installation verifaction:  
In log: 
```
-- Found SRSGUI: /usr/local/lib/libsrsGUI.so  
```
And not: (todo: fix this)
```
CMake Warning:
  Manually-specified variables were not used by the project:

    USE_SRSGUI
```
> ldd /usr/local/lib/libsrsGUI.so

## 4. Update shared library
> sudo ldconfig  
<details>
<summary>Otherwise:  </summary>
> sudo srsue

```
srsue: error while loading shared libraries: libsrsran_rf.so.0: cannot open shared object file: No such file or directory
```
</details>

## 5. Try c programs in lib/example
### cmake cannot find fftw
When make: linking: undefined reference.  
Add `find_package(FFTW REQUIRED)` in CMakeLists.txt:  
```
CMake Error at CMakeLists.txt:24 (find_package):
  By not providing "FindFFTW.cmake" in CMAKE_MODULE_PATH this project has
  asked CMake to find a package configuration file provided by "FFTW", but
  CMake did not find one.

  Could not find a package configuration file provided by "FFTW" with any of
  the following names:

    FFTWConfig.cmake
    fftw-config.cmake

  Add the installation prefix of "FFTW" to CMAKE_PREFIX_PATH or set
  "FFTW_DIR" to a directory containing one of the above files.  If "FFTW"
  provides a separate development package or SDK, be sure it has been
  installed.
```

### cell_search
> ./cell_search -b 7 -s 3000 -e 3001

## 6. FALCON
### Dependency
> sudo apt-get install libglib2.0-dev libudev-dev libcurl4-gnutls-dev libboost-all-dev qtdeclarative5-dev libqt5charts5-dev
### Cmake & installation
```
git clone https://github.com/falkenber9/falcon.git
cd falcon
mkdir build
cd build
```
* before cmake: <https://github.com/falkenber9/falcon/issues/8>
* need to modify `lib/include/falcon/meas/probe_modem.h`
```
cmake -DCMAKE_INSTALL_PREFIX=/usr ../
make

# Install (optional)
sudo make install

# Uninstall (use carefully!)
sudo xargs rm < install_manifest.txt
```

## some commands
* ls /usr/local/lib/libsrs*.so
* ls /usr/local/include/srsgui
* sudo uhd_find_devices
* sudo uhd_usrp_probe

## memo
1. config generated in - Installing ue.conf.example in /home/xxx/.config/srsran/ue.conf, instead of /root/.config/srsran/ue.conf
2. To enable srsGUI: modify the config file, for example `ue.conf`.