SOURCE_CHANNELS = os.getenv("SOURCE_CHANNELS")
if SOURCE_CHANNELS:
    SOURCE_CHANNELS = SOURCE_CHANNELS.split(",")
else:
    raise ValueError("Environment variable 'SOURCE_CHANNELS' is not set!")