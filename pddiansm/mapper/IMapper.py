from pddiansm.thesaurus.IThesaurusEntries import IThesaurusEntries


class IMapper:
    def search_moc(self, string: str) -> IThesaurusEntries:
        """
        :param string: a molecule, drug_class, or identifier
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        pass
