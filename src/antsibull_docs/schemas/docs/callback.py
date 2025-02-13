# Author: Toshio Kuratomi <tkuratom@redhat.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020, Ansible Project
"""Schemas for the plugin DOCUMENTATION data."""

import pydantic as p

from .base import BaseModel
from .plugin import InnerDocSchema, PluginExamplesSchema, PluginMetadataSchema, PluginReturnSchema

REQUIRED_CALLBACK_TYPE_F = p.Field(..., regex='^(aggregate|notification|stdout)$')


class InnerCallbackDocSchema(InnerDocSchema):
    """
    Schema describing the structure of callback documentation.

    Differs from other plugins because callbacks have subtypes documented in ``type`` rather than
    having separate types.
    """

    type: str = REQUIRED_CALLBACK_TYPE_F


# Ignore Uninitialized attribute error as BaseModel works some magic to initialize the
# attributes when data is loaded into them.
# pyre-ignore[13]
class CallbackDocSchema(BaseModel):
    doc: InnerCallbackDocSchema


class CallbackSchema(CallbackDocSchema, PluginExamplesSchema, PluginMetadataSchema,
                     PluginReturnSchema, BaseModel):
    """Documentation of callback plugins."""
