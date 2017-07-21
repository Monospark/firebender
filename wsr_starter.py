import wsr_connector

if __name__ == "__main__":
    wsr_connector.init()
    while True:
        if not wsr_connector.loop():
            break
    wsr_connector.destroy()
