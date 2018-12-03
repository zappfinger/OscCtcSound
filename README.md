# OscCtcSound

This a work in progress. Using PySimpleGUI, ctcsound and Csound. A SQLite database contains Csound code and corresponding GUI code.
The template is meant to be a structure with maybe one preloaded instrument and effects. It should be possible to load other instruments and effects after the initial loading of the template.
This initial example shows some sliders controlling the template and a simple VU meter...

To use this, you should install Csound for your platform (ctcsound will come with that). Also install PySimpleGUI via pip.
Then run simpleGUI.py and play your attached midi keyboard.
You can inspect and change the database (csounds.sqlite) best with the FireFox SQLite plugin.
You might have to change the soundcard and midi input for your situation in the templates table. I have attached a screenshot of this table. The field 'template' contains the Csound code that will be loaded, the field 'GUI' contains the PySimpleGUI code that creates the layout. When you run the program for the first time, the Csound code will be stored in a file called temp.csd. You can uncomment the database loading and edit the file locally. When you are done, do not forget to insert the contents of the file back into the database. In a similar way the GUI code is also in a function called getLayout(). I probably will make this a file also in the near future.  
