## FGT Purchase Order/Agreement Project 

### Testing: Run API Requests Via Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/19653561-2ae87b1a-da6c-44b8-8b79-9f2ada1efb01?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19653561-2ae87b1a-da6c-44b8-8b79-9f2ada1efb01%26entityType%3Dcollection%26workspaceId%3D748fe69a-f43a-4136-951a-9f1d1244ba40)

1. Please make sure to run the Create Vendor and Create PlantType Requests FIRST to seed the DB
2. Please run requests in order from top to bottom (Vendor, PlantType, PA, PO, PO w/ PA, Update PO)
3. You can connect to the DB with the following credentials via a DB IDE (like DBeaver) to validate the data is propagated correctly.
   1. host: localhost
   2. port: 5432
   3. username: postgres
   4. password: postgres
   5. database: postgres

I did not have time to setup the boilerplate for automated unit tests, so I relied on manual tests of happy paths

### Python/Flask with PostgreSQL database

Project structure:
```
.
├── compose.yaml
└── flask
    ├── Dockerfile
    ├── requirements.txt
    └── server.py

```

[_compose.yaml_](compose.yaml)
```
services:
  flask_app:
    build: .
    ...
  flask_db:
    image: postgres:12
    ...
```
The compose file defines an application with two services `backend` and `db`.
When deploying the application, docker compose maps port 4000 of the proxy service container to port 4000 of the host as specified in the file.
Make sure port 4000 on the host is not already being in use.

## Running locally with docker compose

```
$ docker compose up -d
Building 1.0s (11/11) FINISHED
...
...
WARNING: Image for service proxy was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
 ✔ Network fgt-project_default  Created
 ✔ Container flask_db           Started
 ✔ Container flask_app          Started
```

## Expected result

Listing containers should show three containers running and the port mapping as below:
```
$ docker compose ps
NAME                IMAGE                                  COMMAND                  SERVICE             CREATED             STATUS              PORTS
flask_app           andreasmodsquad/flask_live_app:1.0.0   "flask run --host=0.…"   flask_app           3 minutes ago       Up 3 minutes        0.0.0.0:4000->4000/tcp
flask_db            postgres:12                            "docker-entrypoint.s…"   flask_db            3 minutes ago       Up 3 minutes        0.0.0.0:5432->5432/tcp
```

After the application starts, navigate to `http://localhost:4000` in your web browser or run to see its running:
```
$ curl localhost:4000
{ "message": "hello world" }
```

Stop and remove the containers
```
$ docker compose down
```

## Project Planning

### 1. Given Requirements & Assumptions
Requirements
- Create a PA
- Create a PO
- Create a PO related to a PA
- Receive a standard PO
- Receive a PO that is related to a PA

Assumptions
- Plants always healthy 
- We receive the sizes we ordered 
- 1(PA) to many (PO) relationship

### 2. Endpoints

POST /purchase_agreement
- params: { total_quantity: int, end_date: date, plant_type_id: uuid, vendor_id: uuid }
- return success

POST /purchase_order/agreement/<int:id>
- params: { quantity: int }
- return success
- errors:
  - if agreement out of date
  - if purchase order too big
  - if agreement filled
  - if agreement not found

POST /purchase_order
- params: { quantity: int, plant_type_id: uuid, vendor_id: uuid }
- return success

PUT /purchase_order/<int:id>
- params: { received: True }
- logic: update purchase_order received & create new plants
- return success

(Seed endpoints)
POST /vendor
- params: { name: string }
POST /plant_type
- params: { name: string }

### 3. Data Model

Vendor
- id: bigint
- name: String

PurchaseAgreement
- id: bigint
- total_quantity: int
- end_date: DateTime
- updated_at: DateTime
- created_at: DateTime
- plant_type_id: int
- vendor_id: bigint

PurchaseOrder
- id: bigint
- quantity: int
- is_received: boolean
- updated_at: DateTime
- created_at: DateTime
- plant_type_id: int
- vendor_id: bigint
- purchase_agreement_id: bigint (Optional) 

PlantType
- id: int
- name: String

Plant
- id: bigint
- created_at: DateTime
- plant_type_id: int

### 4. Considerations/Assumptions for Implementation Simplicity:
- We don't need to keep track of POs <-> Plants relationship (we assume Plant creation time is the only critical field once they reach our Inventory)
- There is no User model and no access control. This is accessible only by admins.
- We will seed the Vendors and PlantTypes rather than allowing creation.
- 1(Vendor) to many (PA) relationship
- 1(Vendor) to many (PO) relationship
- 1(PlantType) to many (PA) relationship
- 1(PlantType) to many (PO) relationship
- Won't add denormalized fields on PurchaseAgreement in implementation due to complexity and time constraints
  - purchase_orders_quantity_total: int (Denormalized)
  - is_complete: boolean (Denormalized = Date.now() > end_date OR purchase_orders_quantity_total == total_quantity)
- Did not have time to setup boilerplate for automated unit tests, so relied on manual tests of happy paths