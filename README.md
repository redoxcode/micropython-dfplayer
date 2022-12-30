## Description
A micropython library to control the [DFPlayer mini](https://www.dfrobot.com/product-1121.html) mp3 player module.

This library focuses on the most essential functions. Some advanced functions of the dfmini, like the equalizer modes are not implemented yet.

Further this library is made to use the folders function of the dfmini. You can use up to 99 folders and 255 files per folder.
The files on your micro sd card need to be structured like this:

	.
	├── 01
	│   ├── 001.mp3
	│   ├── 002.mp3
	│   └── ...
	├── 02
	│   ├── 001.mp3
	│   ├── 002.mp3
	│   └── ...
	├── 03
	│   ├── 001.mp3
	│   ├── 002.mp3
	│   └── ...
	└── ...

There should be no gaps in the numbering scheme.
It might be best to prepare the whole file structure on your harddrive first and then copy them in one go on a freshly formated micro sd card, as the dfmini might get confused from artifacts left on the sd cards filesystem.
You can use the files in [/sample_files](https://github.com/redoxcode/micropython-dfplayer/tree/main/sample_files) to test your module.

Sometimes the module isn't able to keep up if you try to send commands to fast, so some delay between the commands is needed.

## Examples

### Play a file from a folder
```Python
import time
from dfplayer import DFPlayer
df=DFPlayer(uart_id=1,tx_pin_id=4,rx_pin_id=5)
#wait some time till the DFPlayer is ready
time.sleep(0.2)
#change the volume (0-30). The DFPlayer doesn't remember these settings
df.volume(25)
time.sleep(0.2)
#play file ./01/001.mp3
df.play(1,1)
```
### Find the number of files in a folder
If a folder doesn't exist, get_files_in_folder will return -1
```Python
import time
from dfplayer import DFPlayer
df=DFPlayer(uart_id=1,tx_pin_id=4,rx_pin_id=5)
#wait some time till the DFPlayer is ready
time.sleep(0.2)
print(df.get_files_in_folder(1))
time.sleep(0.2)
print(df.get_files_in_folder(4))
```

## API
### class DFPlayer(uart_id,tx_pin_id=None,rx_pin_id=None)
- uart_id: Uart channel you want to use (0 or 1 for pi pico)
- tx_pin_id: Pin id for uart tx if your board supports changing the pins of the uart channel.  
- tx_pin_id: Pin id for uart rx if your board supports changing the pins of the uart channel.  

```play(folder,file)```
- play a file from a folder (stops all previous playback)
- folder: Folder number of the file you want to play
- file: File number of the file you want to play

```stop()```
- stop all playback

```volume(vol)```
- set the volume of the module
- vol: Volume of the module. The range is 0 to 30. The DFPlayer doesn't remember these settings

```get_volume()```
- returns the current volume setting of the module

```ìs_playing()```
- returns if currently some playback is running

```get_files_in_folder(folder)```
- returns the number of files in a folder or -1 if the folder doesn't exist
- folder: folder to get the number of files in

```reset()```
- reset the module

```send_cmd(cmd,param1=0,param2=0)```
- sends a command byte with 2 bytes for parameters to the module. This can be used to send commands not yet implemented in this library. Use the modules [documentation](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299) as reference.
- cmd: cammand byte (0-255)
- param1: parameter 1 or MSB of a 2 byte parameter
- param2: parameter 2 or LSB of a 2 byte parameter

```send_query(cmd,param1=0,param2=0)```
- like send_cmd, but returns the bytes the module sends as answer to the query
- cmd: cammand byte (0-255)
- param1: parameter 1 or MSB of a 2 byte parameter
- param2: parameter 2 or LSB of a 2 byte parameter

