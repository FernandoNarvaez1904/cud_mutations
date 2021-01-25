from graphene import Scalar
from graphene.types.structures import Structure


class MutationArgument():
    def __init__(
        self,
        display_name: str,
        graphene_scalar: Scalar,
        is_required: bool = False,
        is_property: bool = True,
        is_relationship: bool = False,
    ) -> None:

        self.set_display_name(display_name)
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

    def set_of_type(self, graphene_scalar: Scalar) -> None:
        if not isinstance(graphene_scalar, Scalar):
             if not isinstance(graphene_scalar, Structure):
                raise Exception("of_type, has to be an instance of Scalar")
        self.of_type: Scalar = graphene_scalar
