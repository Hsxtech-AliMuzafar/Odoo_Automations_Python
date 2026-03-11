🛠️ Odoo Automation Scripts

This repository contains Python scripts intended for use with **Scheduled Actions** in **Odoo**, enabling automation of business logic, notifications, data updates, and more without the need for custom modules.

📌 About

These scripts are designed to be executed directly within Odoo’s **“Automated Actions” → “Execute Python Code”** feature, making it easy to automate workflows, maintain data integrity, and trigger time-based events.


> Each script is standalone and documented with usage instructions and dependencies (if any).

---

✅ Features

- 🔄 Automate record updates based on conditions
- 📨 Trigger emails or notifications
- 📅 Handle date-based events (e.g., overdue, expiry, follow-ups)
- 📊 Ensure data consistency across models
- ⚙️ Lightweight and plug-and-play

---

## 📜 Scripts

### **Create_Projects_from_crm.py**
Automatically converts CRM Opportunities into structured Projects. Feature-rich and optimized for Odoo 19, including:
- **Activity Automation**: Creates a "To-Do" activity for the Project Manager.
- **Smart Mapping**: Transfers Customer, Tags, and Description.
- **Odoo 19 UI**: Features sticky success notifications with an "Open Project" button and robust internal links.
- **Duplicate Prevention**: Prevents creating multiple projects for the same Lead.

### **Move_CRM_Stage_on_Quote_Sent.py**
Automates the sales-to-lead workflow by moving an Opportunity to the **"Quote Issued"** stage as soon as a related quotation is sent to the customer. includes clickable links in the chatter for easy navigation.

### **Stock_Quant_User_Validation.py**
Restricts specific users from adding new product lines in the Stock Quant (Inventory Adjustment) window. Only whitelisted users can add or modify products.

### **Sales_Order_Assign_Current_User.py**
Automatically assigns the current user to the "Sales Person" field when creating or updating sales orders.

### **Invoice_Auto_Confirm_PIDistribution.py**
Automatically confirms invoices created in the company "PI Distribution SRL" (ID = 12).

### **Odoo_Survey_to_CRM.py**
Converts survey responses into CRM leads with customizable field mappings.

### **Odoo_Event_to_Calender.py**
Syncs Odoo events to external calendar systems.

### **Odoo_Survey_to_Contact.py**
Creates or updates contacts based on survey responses.

### **Product_Price_Sync.py**
Synchronizes product prices across multiple companies or pricelists.

### **Product_Default_Code_Lock.py**
Prevents editing of the Internal Reference (default_code) field after product creation. Raises a validation error if anyone attempts to modify it, ensuring product codes remain consistent.

### **Survey to Tickets with Email and Priority.py**
Converts survey responses into helpdesk tickets with email notifications and priority assignment.

### **Product_Barcode_Validation.py**
Prevents duplicate barcodes in the `product.template.barcode` model by checking against both `product.template` (barcode and default_code) and other barcode lines. Ensures cross-model uniqueness.

### **Product_Template_Validation.py**
Validates uniqueness of both `barcode` and `default_code` (Internal Reference) fields in `product.template` by cross-checking with `product.template.barcode` records. Prevents conflicts across all product identifiers.

### **CRM_Stage_Update_on_Project_Done.py**
Automatically moves a CRM Opportunity to the **"Job Complete"** stage when its related Project is moved to the **"Done"** stage. Uses the `x_studio_linked` field to identify the connection and includes downgrade prevention to ensure stages only move forward.

### **Purchase_Order_Team_Assignment.py**
Automatically assigns a specific Purchase Representative to a Purchase Order upon creation based on the creator's Sales Team. Mapping:
- Commercial (4) -> Rohan (9)
- CCS (5) -> Chintan (8)
- SWEP (15) -> Nagi (30)
- ITES OPEN Mkt Bid (16, 17, 19) -> Ben (32)

### **Product_Tax_Assignment_on_Creation.py**
Automatically adds a specific Sales Tax (ID: 302) to new or updated products if they belong to Company ID: 12. Uses SQL bypass to handle Odoo multi-company "top-secret records" permission errors and sandbox environment limitations.


---

🚀 Usage

1. Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**.
2. Click **Create** and set your:
   - **Model** (e.g., `crm.lead`, `project.task`, etc.)
   - **Interval Number** and **Unit of Time**
   - **Action To Do**: Select `Execute Python Code`
3. Paste the desired Python script from this repo into the **Python Code** field.
4. Click **Save** and **Activate** the action.

---

## 🔒 Security

Always validate your scripts before applying them in production environments. Scheduled Actions run with **superuser permissions**, so make sure:

- You validate filters and domain logic.
- You handle exceptions properly.
- You test on a staging environment first.

---
## 🤝 Contributing

Feel free to submit issues or open pull requests with improvements, new automation use cases, or bug fixes.

### **Repository Structure**  
```
📂 Odoo_Automations_Python/  
├── README.md
├── Create_Projects_from_crm.py
├── Move_CRM_Stage_on_Quote_Sent.py
├── Odoo_Survey_to_CRM.py  
├── Odoo_Event_to_Calender.py
├── Odoo_Survey_to_Contact.py  
├── Product_Price_Sync.py
├── Product_Default_Code_Lock.py
├── Product_Barcode_Validation.py
├── Product_Template_Validation.py
├── Stock_Quant_User_Validation.py
├── Sales_Order_Assign_Current_User.py
├── Invoice_Auto_Confirm_PIDistribution.py
├── CRM_Stage_Update_on_Project_Done.py
├── Purchase_Order_Team_Assignment.py
├── Product_Tax_Assignment_on_Creation.py
└── Survey to Tickets with Email and Priority.py  
```  

### **License**  
MIT License – Free to use and modify.  

---  
**Contribute or Report Issues**  
Feel free to fork, improve, or suggest enhancements!  


**Powered by Hsx TECH** – *Collaborate, Lead, Innovate* 
