# ui_graphical Guide

# Widget Hierarchy

* Window: app/window_main.py
  *


# Tkinter Tips & Reference

## Widgets

* [Basic Widget Methods](https://effbot.org/tkinterbook/widget.htm)
    * Configuration
        * 'config', 'configure', 'cget', 'keys', 
    * Event Processing
        * 'mainloop', 'quit', 'update', 'update_idletasks',
            'waitvar', 'wait_variable', 'wait_visibility', 'wait_window',
    * Event Callbacks
        * 'bind', 'bind_all', 'bind_class', 'bindtags',
            'unbind', 'unbind_all', 'unbind_class', 
    * Alarm Handlers & Non-Event Callbacks
        * 'after', 'after_cancel', 'after_idle', 
    * Window Management
        * 'lift', 'lower', 
    * Window-related Info
        * 'winfo_width', 'winfo_reqwidth', 'winfo_id', 
            'winfo_atom', 'winfo_atomname', 'winfo_cells', 'winfo_children', 'winfo_class',
            'winfo_colormapfull', 'winfo_containing', 'winfo_depth', 'winfo_exists', 'winfo_fpixels',
            'winfo_geometry', 'winfo_height', 'winfo_interps', 'winfo_ismapped',
            'winfo_manager', 'winfo_name', 'winfo_parent', 'winfo_pathname', 'winfo_pixels',
            'winfo_pointerx', 'winfo_pointerxy', 'winfo_pointery', 'winfo_reqheight', 
            'winfo_rgb', 'winfo_rootx', 'winfo_rooty', 'winfo_screen', 'winfo_screencells',
            'winfo_screendepth', 'winfo_screenheight', 'winfo_screenmmheight', 'winfo_screenmmwidth',
            'winfo_screenvisual', 'winfo_screenwidth', 'winfo_server', 'winfo_toplevel',
            'winfo_viewable', 'winfo_visual', 'winfo_visualid', 'winfo_visualsavailable',
            'winfo_vrootheight', 'winfo_vrootwidth', 'winfo_vrootx', 'winfo_vrooty', 
            'winfo_x', 'winfo_y',
    * Option Database
        * 'option_add', 'option_get', 'option_clear', 'option_readfile',
    * Others
        * 'bbox', 'bell', 'columnconfigure', 'deletecommand', 'destroy',
        * 'clipboard_append', 'clipboard_clear', 'clipboard_get',
        * 'event_add', 'event_delete', 'event_generate', 'event_info',
        * 'focus', 'focus_displayof', 'focus_force', 'focus_get', 'focus_lastfor', 'focus_set',
        * 'getboolean', 'getvar',
        * 'grab_current', 'grab_release', 'grab_set', 'grab_set_global', 'grab_status',
        * 'image_names', 'image_types',
        * 'nametowidget',
        * 'pack_propagate', 'pack_slaves', 'place_slaves', 'propagate',
        * 'register',
        * 'rowconfigure',
        * 'selection_clear', 'selection_get', 'selection_handle', 'selection_own', 'selection_own_get',
        * 'send', 'setvar', 'size', 'slaves',
        * 'tk_bisque', 'tk_focusFollowsMouse', 'tk_focusNext', 'tk_focusPrev', 'tk_setPalette',
            'tk_strictMotif', 'tkraise',

### tk.Tk
* Contructor: super().\_\_init__(parent)
* Config(): 
    * bg='#ff0000' or background='red'
    * width=600, height=400 -- but shrinks when pack children.
    * TBD: 'bd', 'borderwidth', 'class', 'menu', 'relief', 'screen', 'use',
        'colormap', 'container', 'cursor', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'padx', 'pady', 'takefocus', 'visual',
* Tk methods:
    * Includes "Basic Widget Methods"
    * [Window Methods](https://effbot.org/tkinterbook/wm.htm): mixin used by Tk and Toplevel 
        * .resizable(width=True, height=True) -- defaults to True
        * .wm_*() -- same as .*(); avoids name collisions when used as a mixin
        * 'aspect', 'attributes', 'client', 'colormapwindows', 'command',
            'deiconify', 'focusmodel', 'frame', 'geometry', 'grid', 'group',
            'iconbitmap', 'iconify', 'iconmask', 'iconname', 'iconposition', 'iconwindow',
            'maxsize', 'minsize', 'overrideredirect', 'positionfrom', 'protocol',
            'sizefrom', 'state', 'title', 'transient', 'withdraw',
    * TBD: 'anchor',
        'forget',
        'getdouble', 'getint', 'grid_anchor', 'grid_bbox', 'grid_columnconfigure',
        'grid_location', 'grid_propagate', 'grid_rowconfigure', 'grid_size', 'grid_slaves',
        'iconphoto',
        'loadtk', 'manage',
        'readprofile',
        'report_callback_exception',

### tk.Frame
* Contructor: super().\_\_init__(parent)
* Config(): 'bd', 'borderwidth', 'class', 'relief', 'background', 'bg', 'colormap', 'container',
  'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady',
  'takefocus', 'visual', 'width'
 