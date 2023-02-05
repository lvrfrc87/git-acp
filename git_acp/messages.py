
def failing_message(rc, command, output, error) -> None:
    return {"rc": rc, "command":command, "output": str(output), "error": str(error)}

        
