

def load_config(filename: str):
    filename = os.path.join(self.root_path, filename)
    
    d.__file__ = filename
    try:
        with open(filename, mode="rb") as config_file:
            exec(compile(config_file.read(), filename, "exec"), d.__dict__)
    except IOError as e:
        e.strerror = "Unable to load configuration file (%s)" % e.strerror
        raise
    return True