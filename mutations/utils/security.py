

def enforce_custom_auth_decorator(function):
    def wrapper(*args, **kwargs):
        # Getting the necessary variables
        cls = args[0]
        info = args[2]

        # Validating auth
        auth = cls.custom_auth(cls=cls, context=info.context, **kwargs)

        # If auth failed, returning mutation with errors
        if not auth[0]:
            return cls(completed=False, errors=auth[1])
        print("done")
        # If auth succeeded continuing with the execution
        rt = function(*args, **kwargs)
        return rt
    return wrapper

