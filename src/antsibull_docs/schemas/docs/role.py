# Author: Toshio Kuratomi <tkuratom@redhat.com>
# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021, Ansible Project
"""Schemas for the role documentation data."""

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]

import typing as t

import pydantic as p

from .base import (
    COLLECTION_NAME_F,
    BaseModel,
    DeprecationSchema,
    OptionsSchema,
    SeeAlsoLinkSchema,
    SeeAlsoModSchema,
    SeeAlsoRefSchema,
)


class InnerRoleOptionsSchema(OptionsSchema):
    options: t.Dict[str, 'InnerRoleOptionsSchema'] = {}

    @p.root_validator(pre=True)
    # pylint:disable=no-self-argument,no-self-use
    def allow_description_to_be_optional(cls, values):
        # Doing this in a validator so that the json-schema will still flag it as an error
        if 'description' not in values:
            values['description'] = []
        return values


InnerRoleOptionsSchema.update_forward_refs()


class RoleOptionsSchema(OptionsSchema):
    options: t.Dict[str, 'InnerRoleOptionsSchema'] = {}


class RoleEntrypointSchema(BaseModel):
    """Documentation for role entrypoints."""
    description: t.List[str]
    short_description: str
    author: t.List[str] = []
    deprecated: DeprecationSchema = p.Field({})
    notes: t.List[str] = []
    requirements: t.List[str] = []
    seealso: t.List[t.Union[SeeAlsoModSchema, SeeAlsoRefSchema, SeeAlsoLinkSchema]] = []
    todo: t.List[str] = []
    version_added: str = 'historical'

    options: t.Dict[str, RoleOptionsSchema] = {}


class RoleSchema(BaseModel):
    """Documentation for roles."""
    collection: str = COLLECTION_NAME_F
    entry_points: t.Dict[str, RoleEntrypointSchema]
    path: str
