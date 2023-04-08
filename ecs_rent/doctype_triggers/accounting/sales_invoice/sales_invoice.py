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
def get_rent_details(doc, method=None):
    #doc = frappe.get_doc("Sales Invoice", name)
    pass

@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    new_doc = frappe.get_doc({
				'doctype': 'Stock Entry',
				'transaction_date' : doc.posting_date,
                'stock_entry_type':'Material Transfer',
				'reference_doctype': 'Sales Invoice',
				'reference_name' :doc.name,
                'from_warehouse': doc.from_warehouse,
				'to_warehouse': doc.to_warehouse,
			})
    for d in doc.items:
        frappe.db.sql(f"""update `tabRent Detail` set returned = 1  where name = '{d.rent_detail}'""")
        frappe.db.sql(f"""update `tabRent Detail` set returen_date = '{doc.posting_date}'  where name = '{d.rent_detail}'""")
        frappe.db.sql(f"""update `tabRent Detail` set sales_invoice = '{doc.name}' where name = '{d.rent_detail}'""")
        frappe.db.sql(f"""update `tabRent Detail` set base_billing_amount = '{doc.grand_total}' where name = '{d.rent_detail}'""")
        frappe.db.sql(f"""update `tabRent Detail` set total_days = '{d.qty}' where name = '{d.rent_detail}'""")
        frappe.db.sql(f"""update tabRent join `tabRent Detail` on tabRent.name =`tabRent Detail`.parent 
        set tabRent.total_billed_amount = ((select total_billed_amount from tabRent where name = '{doc.rent}') + '{doc.grand_total}')""")
        new = new_doc.append("items", {})
        new.item_code = d.item_code
        new.item_name = d.item_name
        new.qty= d.qty
    new_doc.insert(ignore_permissions=True)
    new_doc.submit()
    #doc.status = "Submitted"
    
@frappe.whitelist()
def on_cancel(doc, method=None):
    for d in doc.item:
        frappe.db.sql(f"""
            update `tabRent Detail` set returned = 0 and returen_date = '' and sales_invoice = '' where name = '{d.rent_detail}'
        """)
    links = frappe.get_all(
    "Dynamic Link",
    filters={"link_doctype": doc.doctype, "link_name": doc.name},
    fields=["parent", "parenttype"],
    )
    for link in links:
        linked_doc = frappe.get_doc(link["parenttype"], link["parent"])

        if len(linked_doc.get("links")) == 1:
            linked_doc.delete(ignore_permissions=True)
        else:
            to_remove = None
        for d in linked_doc.get("links"):
            if d.link_doctype == doc.doctype and d.link_name == doc.name:
                to_remove = d
            if to_remove:
                linked_doc.remove(to_remove)
                linked_doc.save(ignore_permissions=True)


@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
