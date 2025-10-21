from app import app, db
from models import User, Character, Planet

with app.app_context():
    # Create planets
    tatooine = Planet(name="Tatooine", climate="arid", terrain="desert", population="200000")
    naboo = Planet(name="Naboo", climate="temperate", terrain="grassy hills, swamps, forests, mountains", population="4500000000")
    korriban = Planet(name="Korriban", climate="hot", terrain="mountains, valleys, deserts", population="Unknown")
    mustafar = Planet(name="Mustafar", climate="hot", terrain="volcanoes, lava rivers, mountains, caves", population="20000")
    
    db.session.add_all([tatooine, naboo, korriban, mustafar])
    db.session.commit()
    
    
    darth_vader = Character(
        name="Darth Vader", 
        gender="male", 
        birth_year="41.9BBY", 
        species="Human (cyborg)", 
        homeworld_id=tatooine.id
    )
    
    darth_maul = Character(
        name="Darth Maul", 
        gender="male", 
        birth_year="54BBY", 
        species="Zabrak", 
        homeworld_id=None
    )
    
    darth_sidious = Character(
        name="Darth Sidious", 
        gender="male", 
        birth_year="82BBY", 
        species="Human", 
        homeworld_id=naboo.id
    )
    
    darth_tyranus = Character(
        name="Darth Tyranus", 
        gender="male", 
        birth_year="102BBY", 
        species="Human", 
        homeworld_id=None
    )
    
    darth_plagueis = Character(
        name="Darth Plagueis", 
        gender="male", 
        birth_year="Unknown", 
        species="Muun", 
        homeworld_id=None
    )
    
    darth_bane = Character(
        name="Darth Bane", 
        gender="male", 
        birth_year="1026BBY", 
        species="Human", 
        homeworld_id=None
    )
    
    darth_revan = Character(
        name="Darth Revan", 
        gender="male", 
        birth_year="Unknown", 
        species="Human", 
        homeworld_id=None
    )
    
    db.session.add_all([darth_vader, darth_maul, darth_sidious, darth_tyranus, darth_plagueis, darth_bane, darth_revan])
    db.session.commit()
    
    # Create a test user
    user = User(username="testuser", email="test@example.com", password="password123")
    db.session.add(user)
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print(f"✅ Added {Character.query.count()} characters")
    print(f"✅ Added {Planet.query.count()} planets")
    print(f"✅ Added {User.query.count()} users")
