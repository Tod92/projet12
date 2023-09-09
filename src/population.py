
USER_POPULATION = [
    {
        "id":1,
        "firstName":"Omer",
        "lastName":"Simpson",
        "login":"osim",
        "email":"osimpson@gmail.com",
        "password":"1234",
        "role_id":1
    },
    {
        "id":2,
        "firstName":"Marge",
        "lastName":"Simpson",
        "login":"msim",
        "email":"msimpson@gmail.com",
        "password":"AZERTY",
        "role_id":2
    }
]

ROLE_POPULATION = [
    {
        "id":1,
        "name":"Gestion"
    },
    {
        "id":2,
        "name":"Support"
    },
    {
        "id":3,
        "name":"Commercial"
    }    
]

LOCATION_POPULATION = [
    {
        "id":1,
        "address":"12, rue des bois"
    },
    {
        "id":2,
        "address":"221b Baker Street"  
    },
    {
        "id":3,
        "address":"0, avenue du Big Bang"
    },
]

COMPANY_POPULATION = [
    {
        "id":1,
        "name":"POKEMON INC",
        "location_id":1
    },
    {
        "id":2,
        "name":"AVENGERS INC",
        "location_id":2
    }
]

CLIENT_POPULATION = [
    {
        "id":1,
        "firstName":"Pika",
        "lastName":"Chu",
        "email":"pika.chu@gmail.com",
        "phone":"0100000000",
        "company_id":1
    },
    {
        "id":2,
        "firstName":"Bulbi",
        "lastName":"Zare",
        "email":"bulbi.zare@gmail.com",
        "phone":"01111111",
        "company_id":1
    },
    {
        "id":3,
        "firstName":"Iron",
        "lastName":"Man",
        "email":"iron.man@gmail.com",
        "phone":"0123456789",
        "company_id":2
    },
]

STATUS_POPULATION = [
    {
        "id":1,
        "name":"En cours"
    },
    {
        "id":2,
        "name":"Terminé"
    }
]

CONTRACT_POPULATION = [
    {
        "id":1,
        "description":"Contract de maintenance éléctrique avec le client PIKA CHU (POKEMON INC)",
        "totalAmount":1560,
        "remainingAmount":1560,
        "client_id":1

    },
    {
        "id":2,
        "description":"Contract bancaire avec Tony Stark",
        "totalAmount":999999,
        "remainingAmount":999999,
        "client_id":3

    },
    {
        "id":3,
        "description":"Contrat pour un stand Avengers à la Comic Con",
        "totalAmount":12,
        "remainingAmount":16,
        "client_id":3

    }
]

EVENT_POPULATION = [
    {
        "id":1,
        "name":"Comic con",
        "attendees":5000,
        "notes":"cosplay à gogo !",
        "contract_id":3,
        "location_id":2

    },
    {
        "id":2,
        "name":"Combat de Pokemon type feu",
        "attendees":200,
        "notes":"Penser à amener un extincteur",
        "contract_id":1,
        "location_id":3

    }
]