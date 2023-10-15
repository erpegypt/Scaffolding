from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import date_diff


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass

@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if not doc.stock_entry and doc.disabled == 1:
        sales_invoice = frappe.get_doc("Sales Invoice",doc.reference_document)
        new_doc = frappe.get_doc({
				'doctype': 'Stock Entry',
				'transaction_date' : doc.end_date,
                'stock_entry_type':'Material Transfer',
				'reference_doctype': 'Auto Repeat',
				'reference_name' :doc.name,
                'from_warehouse': sales_invoice.to_warehouse,
				'to_warehouse': sales_invoice.from_warehouse,
			})
        for d in sales_invoice.items:
            new = new_doc.append("items", {})
            new.item_code = d.item_code
            new.item_name = d.item_name
            new.qty= d.qty
        new_doc.insert(ignore_permissions=True)
        new_doc.submit()



@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
