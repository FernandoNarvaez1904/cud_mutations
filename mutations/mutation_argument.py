from graphene import Scalar


class MutationArgument():
    def __init__(
        self,
        display_name: str,
        property_name: str,
        graphene_scalar: Scalar,
        is_required: bool = False,
        is_property: bool = True,
        is_relationship: bool = False,
    ) -> None:

        self.set_display_name(display_name)
        self.set_property_name(property_name)
        self.set_of_type(graphene_scalar)

        self.is_required = is_required
        self.is_property = is_property
        self.is_relationship = is_relationship

    def set_display_name(self, display_name: str) -> None:
        if display_name is None:
            raise Exception("display_name cannot be None")
        elif display_name.strip() == "":
            raise Exception("display_name cant be an empty string")
        self.display_name = display_name

    def set_property_name(self, property_name: str) -> None:
        if property_name is None:
            raise Exception("property_name cannot be None")
        elif property_name.strip() == "":
            raise Exception("property_name cant be an empty string")
        self.property_name = property_name

    def set_of_type(self, graphene_scalar: Scalar) -> None:
        if not isinstance(graphene_scalar, Scalar):
            raise Exception("of_type, has to be an instance of Scalar")
        self.of_type: Scalar = graphene_scalar