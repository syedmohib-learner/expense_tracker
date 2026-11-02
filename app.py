import datetime
import streamlit as st


def main():
  # Page Configuration
  st.set_page_config(
      page_title="Personal Expense Tracker", page_icon="💰", layout="wide"
  )

  st.title("💰 Personal Expense Tracker")
  st.markdown(
      "Manage your daily expenses efficiently using Python and Streamlit."
  )

  # Initialize session state for storing expenses
  if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

  # ==========================================
  # SIDEBAR: SEARCH & FILTERS (Task 4)
  # ==========================================
  st.sidebar.header("🔍 Search & Filters")

  # A. Search Expense by Name
  search_query = st.sidebar.text_input(
      "Search Expense by Name", ""
  ).lower()

  # B. Category Filter
  categories = ["All", "Food", "Travel", "Shopping", "Bills", "Other"]
  selected_category = st.sidebar.selectbox("Filter by Category", categories)

  # C. Amount Filter using Slider
  max_amt_default = 10000.0
  if st.session_state["expenses"]:
    amounts = [float(exp["Amount"]) for exp in st.session_state["expenses"]]
    if amounts:
      max_amt_default = max(amounts) * 2

  max_amount_filter = st.sidebar.slider(
      "Max Amount Filter ($)", 0.0, float(max_amt_default), float(max_amt_default)
  )

  # ==========================================
  # TASK 1: ADD EXPENSE FORM
  # ==========================================
  st.header("➕ Add New Expense")
  with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      expense_name = st.text_input("Expense Name")
      amount = st.number_input("Amount ($)", min_value=0.0, step=1.0)
    with col2:
      category = st.selectbox(
          "Category", ["Food", "Travel", "Shopping", "Bills", "Other"]
      )
      date = st.date_input("Date", datetime.date.today())

    submitted = st.form_submit_button("Add Expense")
    if submitted:
      if expense_name.strip() == "":
        st.error("Expense name cannot be empty.")
      elif amount <= 0:
        st.error("Amount must be greater than zero.")
      else:
        new_expense = {
            "Name": expense_name.strip(),
            "Amount": float(amount),
            "Category": category,
            "Date": str(date),
        }
        st.session_state["expenses"].append(new_expense)
        st.success(
            f"Successfully added expense: **{expense_name}** (${amount:.2f})"
        )

  st.markdown("---")

  # ==========================================
  # TASK 2 & 6: DASHBOARD SUMMARY
  # ==========================================
  st.header("📊 Dashboard Summary")

  expenses = st.session_state["expenses"]
  total_transactions = len(expenses)
  total_expenses = sum(exp["Amount"] for exp in expenses)

  highest_expense_name = "N/A"
  highest_expense_amount = 0.0
  if expenses:
    highest_exp = max(expenses, key=lambda x: x["Amount"])
    highest_expense_name = highest_exp["Name"]
    highest_expense_amount = highest_exp["Amount"]

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")
  with col2:
    st.metric(label="Total Transactions", value=str(total_transactions))
  with col3:
    if total_transactions > 0:
      st.metric(
          label="Highest Expense",
          value=f"${highest_expense_amount:,.2f}",
          delta=highest_expense_name,
      )
    else:
      st.metric(label="Highest Expense", value="$0.00", delta="N/A")

  st.markdown("---")

  # Filter Logic Implementation
  filtered_expenses = []
  for idx, exp in enumerate(expenses):
    exp_copy = exp.copy()
    exp_copy["_id"] = idx  # Keep track of original index for deletion

    # Apply search filter
    if search_query and search_query not in exp["Name"].lower():
      continue
    # Apply category filter
    if (
        selected_category != "All"
        and exp["Category"] != selected_category
    ):
      continue
    # Apply amount filter
    if exp["Amount"] > max_amount_filter:
      continue

    filtered_expenses.append(exp_copy)

  # ==========================================
  # TASK 3 & 5: EXPENSE RECORDS & DELETE
  # ==========================================
  st.header("📋 Expense Records")

  if not expenses:
    st.warning(
        "No expense records available. Use the form above to add your first"
        " expense!"
    )
  elif not filtered_expenses:
    st.warning("No expenses match your search or filter criteria.")
  else:
    # Prepare data for display (excluding internal ID)
    display_data = []
    for exp in filtered_expenses:
      display_data.append(
          {
              "Name": exp["Name"],
              "Amount ($)": f"${exp['Amount']:,.2f}",
              "Category": exp["Category"],
              "Date": exp["Date"],
          }
      )
    st.dataframe(display_data, use_container_width=True)

    # Task 5: Delete Expense Functionality
    st.subheader("🗑️ Delete Expense")
    delete_options = {
        f"{exp['Name']} - ${exp['Amount']} ({exp['Category']} on {exp['Date']}) [ID: {exp['_id']}]": exp[
            "_id"
        ]
        for exp in filtered_expenses
    }

    selected_delete_key = st.selectbox(
        "Select an expense to delete", list(delete_options.keys())
    )

    if st.button("Delete Selected Expense"):
      target_id = delete_options[selected_delete_key]
      removed_item = st.session_state["expenses"].pop(target_id)
      st.success(f"Successfully deleted: **{removed_item['Name']}**")
      st.rerun()

  st.markdown("---")

  # ==========================================
  # TASK 6: CATEGORY-WISE SUMMARY
  # ==========================================
  st.header("🏷️ Category-wise Expense Summary")
  if expenses:
    category_totals = {
        "Food": 0.0,
        "Travel": 0.0,
        "Shopping": 0.0,
        "Bills": 0.0,
        "Other": 0.0,
    }
    for exp in expenses:
      cat = exp["Category"]
      if cat in category_totals:
        category_totals[cat] += exp["Amount"]

    cat_cols = st.columns(5)
    cat_items = list(category_totals.items())
    for i, col in enumerate(cat_cols):
      cat_name, cat_amt = cat_items[i]
      with col:
        st.metric(label=cat_name, value=f"${cat_amt:,.2f}")
  else:
    st.info("Add expenses to view category-wise breakdown.")


if __name__ == "__main__":
  main()