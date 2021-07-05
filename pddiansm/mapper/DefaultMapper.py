from typing import List

from pddiansm.mapper.IMapper import IMapper


class DefaultMapper(IMapper):
    """
    No mapping by default. The identifier is the name of molecule or class to be found
    """
    def get_mocs_mapped(self, identifier: str) -> List[str]:
        """ Overrides """
        moc = identifier
        return [moc]
