# Wyrmy

Watch a demonstration of Wyrmy at https://avirut.github.io/Wyrmy.

I developed Wyrmy while interning at the Kirienko Lab at Rice University. A large portion of the experiment I worked on during this period involved data analysis, and manual scoring of the virulence of chemical and biological samples on a population of Caenorhabditis elegans, measured in a high-throughput manner through the use of multiple 384-well plates which were then photographed through a microscope system.

In order to manually score C. elegans samples, I would analyze images as a whole, counting how many worms were present in each image and then counting how many of these were dead, inputting both numbers manually into a spreadsheet. This was an intensive task as it required complete focus on keeping track of what had and had not been counted, and the effort required additionally led to inaccuracies and mis-scores over time.

To solve this issue, I developed Wyrmy with the aim of reducing the task to its simplest form - identifying individual roundworms as dead or alive. Wyrmy allows the user to mark individual specimens one way or another, keeping track of how many have been marked on each image individually. When a dataset is complete, the collected information can be exported to a spreadsheet. Wyrmy also makes it possible to keep track of which worms were marked each way - individual scores can be saved into a proprietary file format and later loaded back with the dataset, even on another computer.

## Use

To use Wyrmy, simply download a release, extract all the files, and run `python wyrmy.py` in the directory after ensuring that all dependencies (specifically PyQt5) have been installed. If PyQt5 isn't installed, just run `pip install pyqt5` first. Python must be installed prior to use.
