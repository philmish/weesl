# weesl

create basic setup scripts with python from yaml files.

The flow-dev.yml file is an example for a weesl setup.
A Setup can use different modules from the modules directory.
Just define them in the file to load them on startup.

Setups define Tasks which is have a list of Calls which they will make in the order defined by the
setup file.

A Call takes arguments and keyword arguments and can save the output of the call to a Receiver (WIP).
This can be used to utilize the variable spaces provided (global for the run time and locals for a Task) by
specifying them as Receiver to a Call.

Variables will be used to interpolate arguments and keyword arguments when a Call is executed.
If only the variable name with the correlating prefix is given it will be interpolated to any data type
which is contained in the variable. If it is part of a string the value will be fomatted into the string.

weesl can also resolve env vars. To specify an env var as a value for a variable use the following syntax:
ENV:<var-name[:<default-value]
ENV:HOME:/home/root

