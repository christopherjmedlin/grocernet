from .models import Vendor
from flask_restful import Api, Resource, reqparse, abort
from flask import Blueprint
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_Distance

vendors_api_bp = Blueprint('vendors_api', __name__,
                           url_prefix='/api/v1/vendors')
api = Api(vendors_api_bp)


def get_vendor_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('points_only', type=bool, location="args")
    parser.add_argument('near_x', type=float, location='args')
    parser.add_argument('near_y', type=float, location='args')
    parser.add_argument("start", type=int, location="args")
    parser.add_argument("end", type=int, location="args")
    return parser


@api.resource('/<int:model_id>')
class VendorRetrieveResource(Resource):
    def query_vendor(self, model_id):
        vendor = Vendor.query.filter_by(id=model_id).first()
        if vendor is not None:
            return vendor
        abort(404,
              message="Could not find vendor object with id: "
                      + str(model_id))

    def get(self, model_id):
        return self.query_vendor(model_id).to_dict()


@api.resource('/')
class VendorListResource(Resource):
    def get(self):
        args = get_vendor_list_parser().parse_args()
        query = Vendor.query

        if args["near_x"] and args["near_y"]:
            wkt_point = "SRID=4326;POINT(" + str(args["near_y"]) + \
                        " " + str(args["near_x"]) + ")"
            query = query.order_by(
                ST_Distance(Vendor.latitude_longitude, wkt_point)
            )

        vendors = query.all()
        vendor_list = []

        if args["points_only"]:
            for vendor in vendors:
                point = to_shape(vendor.latitude_longitude)
                vendor_list.append([point.x, point.y])
        else:
            for vendor in vendors:
                vendor_list.append(vendor.to_dict())

        if args["start"] is None:
            args["start"] = 0
        if args["end"] is None:
            args["end"] = len(vendor_list)

        return {"vendors": vendor_list[args["start"]:args["end"]]}