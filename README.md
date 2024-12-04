## About the Data
The data used to train the model is securely stored by City, University of London and subject to a data sharing agreement between the VISION consortium and a UK police force.

### Accessing the data
Access to the data (subject to sufficient permissions) is managed through the `.env` and `file_manager.py` files. These can be accessed via the following arguments:
- `make check` checks whether a master data location has been set.
- `make duplicate` creates a local version of the master data within the repository. 
- `make delete` deletes all local versions of the master data to prevent data redundancy.

### Using your own data
You can retrain the model using your own data by defining a separate `.env` file, specifying a new **MASTER_DATA_FILE** path. Make sure to include the `.env` file at the root.