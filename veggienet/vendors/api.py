from .models import Vendor
from flask_restful import Api, Resource
from flask import Blueprint

vendors_api_bp = Blueprint('vendors_api', __name__,
                           url_prefix='/api/v1/vendors')
api = Api(vendors_api_bp)


@api.resource('/<int:model_id>')
class VendorRetrieveResource(Resource):
    def query_vendor(self, model_id):
        vendor = Vendor.query.filter_by(id=model_id).first()
        if vendor is not None:
            return vendor
        abort(404,
              message="Could not find vendor object with id: " \
                      + str(model_id))
        
    def get(self, model_id):
        return self.query_vendor(model_id).to_dict()
