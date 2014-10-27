Configuration
=============

.. _config:

Public/Private
--------------
This is to separate your environment with the default environment.
For testing and for fast prototyping, you can use the public configuration.
In other case, copy the public directory like this :

>>> cp configurations/public configurations/private

Adapt config.py and thirdparty.json to your system.

config.py
---------
Actually, the configuration file is a Python file.

Implemented feature:
 - keep_alive_media : when a media is started, the stop will be ignore
 - active_configuration : used in private configuration for active it
 - log_path : directory to save file
 - lst_media : append your :ref:`media_template` in this list
 - show_public_filterchain : used in private configuration, to enable default filterchains
 - show_public_filter : used in private configuration, to enable default filters
 - def cmd_on_start(cmd_handler) : a function called when the server is started
    + example of use, start media at start.

.. _third-party:

thirdparty.json
---------------
You can include external feature with the configuration file thirdparty.json in your configuration directory.

 - name : the directory name, must be unique
 - git : the repository to clone
 - type : module type when SeagoatVision will interpret it
 - active : boolean if load the third-party at the runtime

Media
^^^^^
An example of media

>>> {
>>>   "name":"ros_media",
>>>   "git":"https://github.com/seagoatvision/ros_seagoatvision_media.git",
>>>   "type":"media",
>>>   "active":true
>>> }