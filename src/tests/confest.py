from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

#  Включить внутренний каталог в sys.path для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


