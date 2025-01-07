# Home Inventory Management
CRUD app to manage one's home inventory.
Main goal is to manage food in the fridge and pantry. But will also be useful for other inventory.
# Goal / Release Features
- CReate: New items in inventory
	- Has name
	- Has quantity
- Update: Update quantity
- Delete: Delete from inventory
## Front End
- Button to view / hide items with "0" (zero inventory)
# Later Developments
- Add a tagging system for items support filtering
- Add shopping list feature
	- Button "Add to Shopping List"
	- Free field for add to shopping list
- (Frontend) Autocomplete for items which exist in inventory
- Shareable for multiple users:
	- Login
	- Households

# How to run Tailwind live for testing
In the command line run `npx tailwindcss -i app/static/input.css -o app/static/output.css --watch`.
Ensure that the directory for the css source is set to the `output.css` in the html file.

# To test on different devices
Run flask on --host=0.0.0.0
Then create an inbound rule for port 5000 (or whatever port you are using) to allow the connection from your other device.