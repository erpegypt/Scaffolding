# Copyright (c) 2023, ECS and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
import datetime
import json

class Rent(Document):
	@frappe.whitelist()
	def before_validate(doc):
		pass

	
	@frappe.whitelist()
	def validate(doc):
		if doc.rent_type == "Daily":
			for x in doc.time_logs:
				x.rate = frappe.db.get_value('Item Price', {"item_code": x.item_code, "selling" : 1,"price_list": "Daily"}, 'price_list_rate')
				x.income_account = frappe.db.get_single_value('Company', 'default_income_account')
		else:
			for x in doc.time_logs:
				x.rate = frappe.db.get_value('Item Price', {"item_code": x.item_code, "selling" : 1,"price_list": "Monthly"}, 'price_list_rate')
				x.income_account = frappe.db.get_single_value('Company', 'default_income_account')

	
	@frappe.whitelist()
	def on_submit(doc):
		new_doc = frappe.get_doc({
				'doctype': 'Stock Entry',
				'transaction_date' : doc.date,
				'stock_entry_type':'Material Transfer',
				'customer': doc.customer,
				'rent' :doc.name,
				'from_warehouse': doc.source_warehouse,
				'to_warehouse': doc.target_warehouse,

			})
		for d in doc.time_logs:
			new = new_doc.append("items", {})
			new.item_code = d.item_code
			new.item_name = d.item_name
			new.qty= d.qty
		new_doc.insert(ignore_permissions=True)
		new_doc.submit()
		frappe.db.sql(f"""
			update tabRent set stock_entry ='{new_doc.name}' where name ='{doc.name}'
		""")
	def on_cancel(doc, method=None):
		doc.ignore_linked_doctypes = ["Stock Entry"]