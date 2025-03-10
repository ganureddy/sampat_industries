from . import __version__ as app_version

app_name = "sampat_industries"
app_title = "Sampat Industries"
app_publisher = "Niraj"
app_description = "Custom App For Sampat Industries"
app_email = "niraj@sampat.co.in"
app_license = "sampatindustries"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sampat_industries/css/sampat_industries.css"
# app_include_js = "/assets/sampat_industries/js/sampat_industries.js"

# include js, css files in header of web template
# web_include_css = "/assets/sampat_industries/css/sampat_industries.css"
# web_include_js = "/assets/sampat_industries/js/sampat_industries.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sampat_industries/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# doc_events = {
#     "Daily Attendance" :{
#         "before_save"
#     }
# }


# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Salary Slip" : "public/js/doctype_plugin/salary_slip/salary_slip.js",
    "BOM" : "public/js/doctype_plugin/BOM/bom.js",
    "Stock Enrty" : "public/js/doctype_plugin/stock_entry/stock_entry.js",
    "Employee" : "public/js/doctype_plugin/Employee/Employee.js",
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]


has_website_permission = {
	"Job Card": "erpnext.controllers.website_list_for_contact.has_website_permission"
}



# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "sampat_industries.utils.jinja_methods",
# }

# Installation
# ------------

# before_install = "sampat_industries.install.before_install"
# after_install = "sampat_industries.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sampat_industries.uninstall.before_uninstall"
# after_uninstall = "sampat_industries.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sampat_industries.utils.before_app_install"
# after_app_install = "sampat_industries.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sampat_industries.utils.before_app_uninstall"
# after_app_uninstall = "sampat_industries.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sampat_industries.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Purchase Order":{
        "on_submit":"sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.update_check_of_po_created"
    },
    "Stock Entry":{
        "on_submit":"sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.update_check_of_stock_entry_created",
        # "on_cancel":"sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.on_cancle_update_record"
    },
    "Yearly Increment Entry":{
        "on_submit":"sampat_industries.curd_event.update_employee_salary"
    }

}
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"sampat_industries.tasks.all"
#	],
#	"daily": [
#		"sampat_industries.tasks.daily"
#	],
#	"hourly": [
#		"sampat_industries.tasks.hourly"
#	],
#	"weekly": [
#		"sampat_industries.tasks.weekly"
#	],
#	"monthly": [
#		"sampat_industries.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "sampat_industries.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "sampat_industries.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "sampat_industries.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sampat_industries.utils.before_request"]
# after_request = ["sampat_industries.utils.after_request"]

# Job Events
# ----------
# before_job = ["sampat_industries.utils.before_job"]
# after_job = ["sampat_industries.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"sampat_industries.auth.validate"
# ]

fixtures = [
    {
        "dt":
            "Custom Field",
            "filters":[[
                "name",
                "in",
                {
                    "Stock Entry-custom_subcontracting_id",
                    "Purchase Order-custom_subcontracting_id",
                    "Stock Entry-custom_supplier_id",
                    "Stock Entry-custom_address",
                    "Stock Entry-custom_fg_item",
                    "Stock Entry-custom_total_weight",
                    "Stock Entry-custom_item_name",
                    "Supplier-custom_supplier_warehouse",
                    "Stock Entry-custom_item_value",
                    "Stock Entry-custom_expected_return_date",
                    "Item-custom_raw_malarials",
                    "Item-custom_strip_width",
                    "Item-custom_strip_thickness",
                    "Item-custom_rm_type",
                    "Item-custom_gross_weight",
                    "Item-custom_net_weight",
                    "Item-custom_yield_per_sheet",
                    "Item-custom_no_of_cavity_per_strip",
                    "Item-custom_column_break_xzyrp",
                    "Item-custom_item_details",
                    "Item Customer Detail-custom_item_description_",
                    "Item Customer Detail-custom_drg_no",
                    "Item Customer Detail-custom_erp_code",
                    "Item Customer Detail-custom_part_no",
                    "Item Customer Detail-custom_drg_document",
                    "Subcontracting Order Supplied Item-custom_bom_uom",
                    "Subcontracting Order Supplied Item-custom_bom_qty",
                    "Stock Entry Detail-custom_hsnsac",
                    "Subcontracting Order Supplied Item-custom_hsnsac",
                    "Stock Entry Detail-custom_subcontracting_uom",
                    "Subcontracting Order Supplied Item-custom_bom_unit",
                    "Stock Entry-custom_party_delivery_number",
                    "Stock Entry-custom_transaction_type_",
                    "Purchase Receipt-custom_supplier_invoice",
                    "Purchase Receipt-custom_supplier_invoice_no",
                    "Purchase Receipt-custom_column_break_mnnoh",
                    "Purchase Receipt-custom_supplier_invoice_date",
                    "Purchase Receipt-custom_entered_in_tally__",
                    "Stock Entry-custom_uom",
                    "Item-custom_drawing_no",
                    "Item-custom_job_work",
                    "Item-custom_itc_04_value",
                    "Item-custom_column_break_junu5",
                    "Item-custom_itc_04_uom",
                    "Stock Entry-custom_total_amount_itc_04",
                    "Stock Entry-custom_returned_qty",
                    "Stock Entry-custom_balance_qty",
                    "Stock Entry-custom_vehicle",
                    "Stock Entry-custom_vehicle_type"
                },    
            ]]
    }
]
