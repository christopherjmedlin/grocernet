from wtforms import StringField, SelectField, validators
from flask_wtf import FlaskForm


class AddVendorForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(),
                                validators.Length(max=70)])
    address = StringField("Address", [validators.InputRequired(),
                                      validators.Length(max=200)])
    vendor_type = SelectField("Vendor Type", choices=[("store", "Store"),
                                                      ("market", "Market"),
                                                      ("farm", "Farm"),
                                                      ("other", "Other")])
