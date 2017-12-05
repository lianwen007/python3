class Restaurant():
	def __init__(self,restaurant_name,cuisine_type):
		self.restaurant_name=restaurant_name
		self.cuisine_type=cuisine_type
		self.number_served=0
	def describe_restaurant(self):
		print("This restaurant's name is "+self.restaurant_name.title()+"!")
		print("\nCuisine type is "+self.cuisine_type.title())
	def open_restaurant(self):
		print(self.restaurant_name.title()+" is openning!")
	def people_number(self):
		print("The restaurant served number : "+str(self.number_served))
	def update_people(self, newnum):
		self.number_served = newnum
