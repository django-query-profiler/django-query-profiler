manifest.json is the entry point for the chrome plugin.  It has two important attributes that define how the plugin works:
1. devtools_page:  This specifies how the plugin is displayed
    - we have to specify a html page here, and ours is devtools.html.  All this page does is include devtools.js
    - In devtools.js, we have the code to create a devtools panel, and add a listener `onRequestFinished`.  This 
    listener gets called for every api, but acts on it ONLY when the api has the headers it is looking for (which 
    we are setting in the middleware).  Once it finds them, it appends a row in the table (in the panel) -- which 
    gets created in next step
2. options_page: This specifies the contents of the plugin.  
    - This page is defined as panel_table.html.  The file
      panel_table.html contains code to create an empty table.  It is in this table that the listener adds rows to
    - We have defined two buttons in the panel - and panel_controls.js defines what functions should be called on
      button click

    
