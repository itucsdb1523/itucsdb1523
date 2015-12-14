class Compounder:
    def __init__(self, ID, Name, LastName, BirthYear, CountryID):
        self.ID=ID
        self.Name=Name
        self.LastName=LastName
        self.BirthYear=BirthYear
        self.CountryID=CountryID

class CompoundTeam:
    def __init__(self, id, name, contact):
        self.id=id
        self.compound_team=name
        self.compound_contact=contact