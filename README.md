# RInformer

CLI project for now. Needs to:
1. give information about temperature and forecast (both weather and pollution)
2. give me a list of YouTube videos from creators that I follow. goal is for me to reduce youtube consumption 
by simply avoiding just aimlessly wandering on YouTube.
3. later it can incorporate the calendar application that I was writing before.

## Architecture

* each service should initialize itself, 
* each service should know about its own API, key, and urls if applicable.
* each service should be able to query .

Thus, the natural shape of the program is around the idea of a `Service`.


