import wsr_connector

def main():
    wsr_connector.init()
    while True:
        if not wsr_connector.loop():
            break
    wsr_connector.destroy()

if __name__ == "__main__":
    from os import path

    home = path.expanduser('~')
    config_dir = path.join(home, "dragonfly_loader")
    print config_dir
