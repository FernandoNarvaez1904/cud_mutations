from .delete_mutations import DeleteMutations
from .create_mutations import  CreateMutations


class Mutations(
    DeleteMutations,
    CreateMutations,
):
    pass
