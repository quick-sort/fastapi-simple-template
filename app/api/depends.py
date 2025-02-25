from __future__ import annotations
from typing import Annotated
import logging
from fastapi import Depends, status, HTTPException, Request

logger = logging.getLogger(__name__)
