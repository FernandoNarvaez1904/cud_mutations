from .delete_mutations import DeleteMutations
from .create_mutations import  CreateMutations
from .update_mutations import UpdateMutations


class Mutations(
    DeleteMutations,
    CreateMutations,
    UpdateMutations,
):
    pass
