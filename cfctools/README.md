
# CFC Tools

## Separation of Concerns

* app_gui or app_cmd
    * Knows only about Models, Services.
    * Handles the UI for its environment (graphical or command line).
    * May contain controllers (C in MVC) if needed.
* models
    * Knows only about other Models (data, validations)
* datamappers
    * Knows only about Models and all data stores
    (database, files, Windows registry, caches, in-memory stores, ...)
* services
    * Knows only about Models, Data Mappers
    