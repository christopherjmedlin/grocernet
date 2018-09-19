from .models import Vendor
from flask_restful import Api
from flask import Blueprint

vendors_api_bp = Blueprint('vendors_api', __name__,
                           url_prefix='/api/v1/vendors')
api = Api(vendors_api_bp)
