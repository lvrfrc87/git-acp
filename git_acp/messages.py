
def failing_message(rc, command, output, error) -> None:
    return {"rc": rc, "command":command, "output":str(output, 'UTF-8'), "error": str(error, 'UTF-8')}

        
