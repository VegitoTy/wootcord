async def dispatch(data):
    type = data.get("event", "none")

    if type == "none":
        print("Data did not contain an event type, skipping.")
        return
    else:
        print(f"Received an event of type: {type}")
        # TODO: dispatch to specific handlers based on event type