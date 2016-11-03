"""Crawling Repositories

These repositories crawl the web after their data.

"""

# Author: Lucas David -- <ld492@drexel.edu>
# License: GPL 3.0

from .courses_repository import CoursesRepository
from .enrollments_repository import EnrollmentsRepository
from .institutes_repository import InstitutesRepository
from .offerings_repository import OfferingsRepository

__all__ = ['CoursesRepository', 'EnrollmentsRepository',
           'InstitutesRepository', 'OfferingsRepository']
