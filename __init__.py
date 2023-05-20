from flask import Flask, render_template, redirect, url_for, request, session, Response
import pandas as pd
import numpy as np
import logging
import datetime
import os.path
from flask import Markup
import os
import mediapipe as mp
from main import main
from flask_autoindex import AutoIndex
from classifyChiTiet import classify_detail
from classifyTongQuat import classify_Non_Detail
from statistic import statistic_process

from werkzeug.utils import cached_property
