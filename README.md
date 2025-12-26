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

### **Survey to Tickets with Email and Priority.py**
Converts survey responses into helpdesk tickets with email notifications and priority assignment.

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
├── Odoo_Survey_to_CRM.py  
├── Odoo_Event_to_Calender.py
├── Odoo_Survey_to_Contact.py  
├── Product_Price_Sync.py
├── Stock_Quant_User_Validation.py
├── Sales_Order_Assign_Current_User.py
├── Invoice_Auto_Confirm_PIDistribution.py
└── Survey to Tickets with Email and Priority.py  
```  

### **License**  
MIT License – Free to use and modify.  

---  
**Contribute or Report Issues**  
Feel free to fork, improve, or suggest enhancements!  


**Powered by Hsx TECH** – *Collaborate, Lead, Innovate* 
