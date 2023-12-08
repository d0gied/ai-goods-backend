class RecurentTaskNamingMixin(type):
    """Meta class for naming recurent tasks.
    It taskes path from parent class and from child class, and
    combines them into name.
    """

    def __new__(cls, name, bases, attrs):
        is_abstract = False
        for base in bases:
            if base.__name__ == "ABC":
                is_abstract = True
                break

        if not is_abstract or name == "BaseTask":
            return super().__new__(cls, name, bases, attrs)

        path = attrs["name"]
        parent_path = bases[0].name
        attrs["name"] = f"{parent_path}.{path}"
        return super().__new__(cls, name, bases, attrs)
