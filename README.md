# Jurassic Park Security System

## Project Overview

InGen envisions a thriving $2.4 billion annual revenue stream from its Isla Nublar Jurassic Park, a renowned tourist destination showcasing genetically engineered dinosaurs. While the ambition to bring dinosaurs back from extinction is awe-inspiring, InGen recognized that ensuring the safety of visitors and safeguarding against corporate espionage would be paramount. To meet these challenges, they've developed a cutting-edge security system that not only monitors the park but also assists in managing its unique inhabitants.

### Security and Safety

Our state-of-the-art security system employs a sophisticated network of cameras covering every inch of Isla Nublar. This comprehensive surveillance system ensures the safety and security of both visitors and the extraordinary dinosaurs residing within the park. By continuously monitoring the location and activities of all animals and humans on the island, our security system achieves three essential objectives:

1. **Visitor Safety:** With real-time tracking and monitoring, we guarantee the safety of our park's visitors. This includes ensuring that visitors are kept at a safe distance from potentially dangerous dinosaurs and responding swiftly to any emergencies.

2. **Corporate Espionage Prevention:** To protect our proprietary technology and the integrity of our dinosaur creations, our security system is equipped to detect and thwart any attempts at corporate espionage or unauthorized access to sensitive areas.

3. **Park Management:** Managing a diverse and dynamic population of genetically engineered dinosaurs is no small task. Our system provides invaluable assistance in tracking and managing each dinosaur's location, species, and status. This enables park staff to make informed decisions regarding the well-being and care of these extraordinary creatures.

### Database-Driven Management

To achieve these goals we've implemented a robust and reliable MySQL database-driven website that serves as the backbone of our security and park management system. Key features of this database include:

- **Dinosaur Records:** Our database meticulously records each dinosaur's vital information, including species, current location, and status. This comprehensive dataset ensures that every dinosaur's well-being and safety are closely monitored and maintained.

- **Employee Management:** We also manage our dedicated team of employees through the database. Tracking their locations, job titles, and employment status enables efficient staffing and allocation of resources across the park.

- **Structure Management:** Each of the structures within the park, including dinosaur enclosures and visitor centers, are carefully monitored for electrical grid status and security fence integrity.

The Jurassic Park Security System represents a pioneering effort to marry cutting-edge technology with the wonder of genetic engineering. As we continue to explore the boundaries of what's possible, we remain committed to providing a safe, unforgettable, and awe-inspiring experience for our visitors while safeguarding the incredible living beings that call Isla Nublar home. Welcome to the future of entertainment and conservation.

## Database Overview: Jurassic Park Management Database

The Jurassic Park Management Database is a comprehensive database designed to ensure the safe and efficient operation of InGen's Isla Nublar Jurassic Park. It encompasses critical aspects of the park's functionality, including the monitoring and management of dinosaurs, species information, employee assignments, visitor records, and location-specific data.

### Tables:

**Dinosaurs:**
- This table records essential details about each unique dinosaur, including genetic makeup, location, and health status.
- Attributes include dinosaurID, speciesID, locationID, name, and health_status.
- Relationships: Many-to-one with location, many-to-one with species, and many-to-many with employees.

**Species:**
- The Species table provides insights into the name and dietary characteristics of dinosaur species present in the park.
- Attributes include speciesID, species_name, diet, and locationID.
- Relationships: One-to-many with Dinosaurs and many-to-many with Locations, aiding staff in identifying species within specific park areas.

**Employees:**
- This table manages park employees, including their job titles, salaries, assigned dinosaurs, and dinosaur health status.
- Attributes include employeeID, job_title, job_salary, locationID, dinosaurID, and health_status.
- Relationships: Many-to-one with location and many-to-many with dinosaurs, representing employees' roles in handling and treating dinosaurs.

**Visitors:**
- The Visitors table maintains records of notable park visitors, capturing their names, locations within the park, and health statuses.
- Attributes include visitorID, name, location, and health_status.
- Relationships: Many-to-one with location, providing insight into visitors' well-being during their stay.

**Locations:**
- This table represents specific zones within the park, tracking all aspects of these areas, including employees, guests, animals, and security features.
- Attributes include locationID, location_name, electric_grid_status, and speciesID.
- Relationships: Many-to-one with employees, visitors, and dinosaurs, as well as many-to-many with species, aiding in comprehensive zone management.

### CRUD Interface: 

A basic CRUD interface was implemented utilizing Jinja to enable the embedding of Python code in a simple HTML frontend. The result enables security personnel to intuitively engage in basic create, read, update, and delete database operations.

![Image 12-5-22 at 9 57 PM](https://github.com/osborneandrewj/jurassic-crud/assets/7835650/b340129b-ef23-44cc-9f41-b7e016c74251)
