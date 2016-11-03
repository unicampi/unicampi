"""Enrollments Repository"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0

from .offerings_repository import OfferingsRepository


class EnrollmentsRepository(OfferingsRepository):
    """Enrollments Repository.

    Enrollments are always associated to a class (the offering of a course).
    Because OfferingsRepository already parses and provides us with the
    enrollments when searching for a given class, we need only to sub-class
    it and filter for said enrollments.

    """

    def all(self):
        if 'offering' not in self.matching:
            raise NotImplementedError(
                'Enrollments repository does not support global fetching '
                'just yet. Please specify {offering} using the '
                '"EnrollmentsRepository.filter" method.')

        return (super(EnrollmentsRepository, self)
                .find(id=self.matching['offering'])['alunos'])

    def find(self, id):
        id = str(id)

        for enrollment in self.all():
            if enrollment['ra'] == id:
                return enrollment

        raise KeyError
