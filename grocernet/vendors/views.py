from .models import Vendor, Rating
from .forms import AddVendorForm
from grocernet.users.models import User
from grocernet.db import save_to_database
from grocernet.util.geo import geocode_address, get_mapbox_static_url
from flask import Blueprint, render_template, url_for, redirect, session
from geoalchemy2.shape import to_shape

vendors_views_bp = Blueprint("vendors_views", __name__)


@vendors_views_bp.route("/add-vendor", methods=["GET", "POST"])
def add_vendor():
    form = AddVendorForm()
    if form.validate_on_submit():
        # get latitude and longitude of address
        geocode_data = geocode_address(form.address.data)

        # create WKT point out of latitude and longitude
        latlon = "POINT(" + str(geocode_data[1][0]) + \
                 " " + str(geocode_data[1][1]) + ")"

        vendor = Vendor(form.name.data, form.address.data, latlon)
        save_to_database(vendor)
        return redirect(url_for("vendors_views.add_vendor_success"))
    return render_template("pages/vendors/add-vendor.html", form=form)


@vendors_views_bp.route("/add-vendor/success")
def add_vendor_success():
    return render_template("pages/vendors/add-vendor-success.html")


@vendors_views_bp.route("/vendor/<vendor_id>")
def view_vendor(vendor_id):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    point = to_shape(vendor.latitude_longitude)
    mapbox_static_url = get_mapbox_static_url(point.x, point.y)
    
    user_rating = None
    authenticated = False
    if "user" in session:
        authenticated = True
        user = User.query.filter_by(username=session["user"]).first()
        user_rating = Rating.query.filter_by(user_id=user.id,
                                             vendor_id=vendor.id).first()
    
    return render_template("pages/vendors/view-vendor.html", vendor=vendor,
                           mapbox_static_url=mapbox_static_url,
                           authenticated=authenticated,
                           user_rating=user_rating)
