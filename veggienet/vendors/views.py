from .models import Vendor
from .forms import AddVendorForm
from veggienet.db import save_to_database
from flask import Blueprint, render_template

vendors_views_bp = Blueprint("vendors_views", __name__)

@vendors_views_bp.route("/add-vendor", methods=["GET", "POST"])
def add_vendor():
    form = AddVendorForm()
    if form.validate_on_submit():
        vendor = Vendor(form.name.data, form.address.data)
        vendor.vendor_type = form.vendor_type.data
        save_to_database(vendor)
    return render_template("pages/vendors/add-vendor.html", form=form)
