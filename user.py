class User:
    def __init__(self, id, name, genero, phone,email):
        self.name = name
        self.id =  id
        self.genero = genero
        self.email = email
        self.phone = phone

    def toDBCollection(self):
        return{
            'id': self.id,
            'name': self.name,
            'genero': self.genero,
            'email': self.email,
            'phone':self.phone
        }