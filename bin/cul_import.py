#!/usr/bin/env python

from django.core.management import setup_environ
from coinage import settings
setup_environ(settings)

from coinage.conjure.models import Item,Tag,ItemTag
