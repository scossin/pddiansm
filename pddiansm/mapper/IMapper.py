from pddiansm.thesaurus.ThesaurusEntries import ThesaurusEntries


class IMapper:
    def search_moc(self, string: str) -> ThesaurusEntries:
        """
        :param string: a molecule, drug_class, or identifier
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        pass
