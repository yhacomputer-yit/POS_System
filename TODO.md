# POS System Improvements TODO

## 1. Improve Dashboard UI
- [x] Redesign dashboard_frame.py with grid layout and better styling
- [x] Add "POS Sales" button to access the new sales interface
- [x] Arrange buttons in a more professional layout

## 2. Redesign Safe Page as POS Sales Screen
- [x] Rename safe_page_frame.py to pos_sales_frame.py
- [x] Implement item selection via list or barcode search
- [x] Add cart functionality with quantity management
- [x] Calculate and display total amount
- [x] Implement checkout process that saves to sales table
- [x] Add staff selection for sales

## 3. Update Main Application
- [x] Update pos_system.py to use POSSalesFrame instead of SafePageFrame
- [x] Add POSSalesFrame to frames dictionary
- [x] Update show_frame logic for POS

## 4. Testing
- [x] Test dashboard navigation
- [x] Test POS sales functionality (add items, calculate total, checkout)
- [x] Verify database saves sales correctly

## 5. UI Improvements
- [x] Improve Category CRUD UI with grid layout, fonts, colors, and scrollbars
- [x] Improve Item CRUD UI with grid layout, fonts, colors, and scrollbars
- [x] Improve Staff CRUD UI with grid layout, fonts, colors, and scrollbars
- [x] Improve Safe Page UI with better layout and styling
- [x] Improve Safe List UI with scrollbars and better layout
- [x] Ensure all pages have consistent "Back to Dashboard" buttons

## 6. Additional Feedback Implementation
- [x] After safe page transaction, show data in safe list with product and amount, and who performed the safe transaction
- [x] Add back to dashboard button to all pages (already ensured)
- [x] Remove emojis from UI
