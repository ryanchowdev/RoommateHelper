def places(args):
    """
    replies to the user with the queried places
    """
    if args == None or len(args) == 0:
        return "Please enter a query by `=places <query>`, ex: =places coffee shop"
    if len(args) > 1:
        query = "%20".join(args)
    else:
        query = args[0]
    if query == '':
        return "Please enter a query by `=places <query>`, ex: =places coffee shop"
    else:
        return f"https://www.google.com/maps/search/?api=1&query={query}"
