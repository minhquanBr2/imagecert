
from fastapi import FastAPI, Depends, Query
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import math


class Image(BaseModel):
    imageID: int
    userUID: int
    url: str
    timestamp: str
    caption: str
    location: str
    deviceName: str
    signature: str


class Hash(BaseModel):
    hashID: int
    imageID: int
    type: str
    value: str


class VerificationStatus(BaseModel):
    statusID: int
    imageID: int
    adminUID: int
    result: int
    verificationTimestamp: str
