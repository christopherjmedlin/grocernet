from .models import Vendor
from .forms import AddVendorForm
from veggienet.db import save_to_database
from veggienet.util.geo import geocode_address
from flask import Blueprint, render_template, url_for, redirect

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

        vendor = Vendor(form.name.data, form.address.data,
                        form.vendor_type.data, latlon)
        save_to_database(vendor)
        return redirect(url_for("vendors_views.add_vendor_success"))
    return render_template("pages/vendors/add-vendor.html", form=form)

@vendors_views_bp.route("/add-vendor/success")
def add_vendor_success():
    return render_template("pages/vendors/add-vendor-success.html")
