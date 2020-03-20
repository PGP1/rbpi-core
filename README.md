# RBPI-Core

Basic Data capturing using Sense Hat.

- Each raspberry pi will have an unique id.
- On first run:
	- Hash token is saved in local sqlite3 under rbpi-rmit-iot.db
	- New folder data is created
- Data files are saved as format: ID-day-month-year-hour-min-sec.csv

Todo:
- [ ] Modify to work with other sensors.
- [ ] Arduino database serialise
