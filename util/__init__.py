def prompt(query: str) -> bool:
    options = ["y", "n"]
    check = input(f"{query} ").lower()
    if check not in options:
        return ValueError
    elif check == "y":
        return True
    else:
        return False
