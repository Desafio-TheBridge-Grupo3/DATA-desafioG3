
CREATE TABLE advisor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(250) NULL,
    username VARCHAR(250) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NULL
);

CREATE TABLE client_erp (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NULL,
    date_last_modify DATE NULL,
    id_address INTEGER NULL,
    id_advisor INTEGER NULL
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NULL,
    cp INTEGER NULL,
    province VARCHAR(50) NULL,
    city VARCHAR(50) NULL,
    address_type VARCHAR(1) NULL,
    zone VARCHAR(1) NULL
);

CREATE TABLE agreement (
    id SERIAL PRIMARY KEY NOT NULL,
    cups20 VARCHAR(20) NOT NULL,
    consumption FLOAT NULL,
    cnae VARCHAR(30) NULL,
    electric_meter VARCHAR(20) NULL,
    vtension_code INTEGER,
    cau VARCHAR(30),
    id_address INTEGER NULL,
    id_client_erp INTEGER NULL,
    id_cia_client INTEGER NULL
);

CREATE TABLE cia_con_several (
    id SERIAL PRIMARY KEY NOT NULL,
    cia TEXT NOT NULL,
    zone VARCHAR(1) NOT NULL,
    rate VARCHAR(5) NOT NULL,
    indexed_date DATE NULL,
    fee VARCHAR(250) NULL,
    product_cia VARCHAR(250) NULL,
    market VARCHAR(1) NULL,
    con_price_P1 FLOAT NULL,
    con_price_P2 FLOAT NULL,
    con_price_P3 FLOAT NULL,
    con_price_P4 FLOAT NULL,
    con_price_P5 FLOAT NULL,
    con_price_P6 FLOAT NULL
);

CREATE TABLE cia_pow_several (
    id SERIAL PRIMARY KEY NOT NULL,
    cia TEXT NOT NULL,
    zone VARCHAR(1) NOT NULL,
    rate VARCHAR(5) NOT NULL,
    product_cia TEXT NULL,
    market VARCHAR(1) NULL,
    pow_price_P1 FLOAT NULL,
    pow_price_P2 FLOAT NULL,
    pow_price_P3 FLOAT NULL,
    pow_price_P4 FLOAT NULL,
    pow_price_P5 FLOAT NULL,
    pow_price_P6 FLOAT NULL
);


CREATE TABLE prize (
    id SERIAL PRIMARY KEY NOT NULL,
    con_P1 FLOAT NULL,
    con_P2 FLOAT NULL,
    con_P3 FLOAT NULL,
    con_P4 FLOAT NULL,
    con_P6 FLOAT NULL,
    con_P5 FLOAT NULL,
    pow_P1 FLOAT NULL,
    pow_P2 FLOAT NULL,
    pow_P3 FLOAT NULL,
    pow_P4 FLOAT NULL,
    pow_P5 FLOAT NULL,
    pow_P6 FLOAT NULL
);

CREATE TABLE cia_client (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NULL,
    issue_date DATE NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    billing_days INTEGER NULL,
    discount_energy FLOAT NULL,
    discount_power FLOAT NULL,
    iva FLOAT NOT NULL,
    tax FLOAT NULL,
    other_tax FLOAT NULL,
    maintenance FLOAT NULL,
    id_prize INTEGER NULL
);

CREATE TABLE consumption (
    id SERIAL PRIMARY KEY NOT NULL,
    code VARCHAR(2) NOT NULL,
    con_P1 FLOAT NULL,
    con_P2 FLOAT NULL,
    con_P3 FLOAT NULL,
    con_P4 FLOAT NULL,
    con_P6 FLOAT NULL,
    con_P5 FLOAT NULL,
    pow_P1 FLOAT NULL,
    pow_P2 FLOAT NULL,
    pow_P3 FLOAT NULL,
    pow_P4 FLOAT NULL,
    pow_P5 FLOAT NULL,
    pow_P6 FLOAT NULL,
    reactive_power FLOAT NULL,
    id_cia_client INTEGER NULL
);

CREATE TABLE total_consumption (
    id SERIAL PRIMARY KEY NOT NULL,
    type_code VARCHAR(2) NOT NULL,
    result_con_P1 FLOAT NULL,
    result_con_P2 FLOAT NULL,
    result_con_P3 FLOAT NULL,
    result_con_P4 FLOAT NULL,
    result_con_P6 FLOAT NULL,
    result_con_P5 FLOAT NULL,
    result_pow_P1 FLOAT NULL,
    result_pow_P2 FLOAT NULL,
    result_pow_P3 FLOAT NULL,
    result_pow_P4 FLOAT NULL,
    result_pow_P5 FLOAT NULL,
    result_pow_P6 FLOAT NULL,
    id_consumption INTEGER NULL
);

CREATE TABLE proposal (
    id SERIAL PRIMARY KEY NOT NULL,
    type VARCHAR(2) NOT NULL,  
    concept VARCHAR NULL,
    date DATE NULL,
    savings FLOAT NULL,
    percent_savings FLOAT NULL,
    cia_several TEXT NULL,
    id_agreement INTEGER NULL
);

CREATE TABLE type_proposal (
    id INTEGER PRIMARY KEY NOT NULL,
    id_consumption INTEGER NULL,
    id_proposal INTEGER NULL
);

-- CLIENT_ERP CONSTRAINTS
ALTER TABLE client_erp
ADD CONSTRAINT fk_client_advisor
FOREIGN KEY (id_advisor)
REFERENCES advisor(id);

ALTER TABLE client_erp
ADD CONSTRAINT fk_client_address
FOREIGN KEY (id_address)
REFERENCES address(id);

--AGREEMENT
ALTER TABLE agreement
ADD CONSTRAINT fk_agree_address
FOREIGN KEY (id_address)
REFERENCES address(id);

ALTER TABLE agreement
ADD CONSTRAINT fk_agree_client_erp
FOREIGN KEY (id_client_erp)
REFERENCES client_erp(id);

ALTER TABLE agreement
ADD CONSTRAINT fk_agree_cia_client
FOREIGN KEY (id_cia_client)
REFERENCES cia_client(id);

-- CIA Client
ALTER TABLE cia_client
ADD CONSTRAINT fk_cia_client_prize
FOREIGN KEY (id_prize)
REFERENCES prize(id);

-- CONSUMPTION CONSTRAINT
ALTER TABLE consumption
ADD CONSTRAINT fk_consumption_cia_client
FOREIGN KEY (id_cia_client)
REFERENCES cia_client(id);

-- CONSUMPTION TOTAL CONSTRAINT
ALTER TABLE total_consumption
ADD CONSTRAINT fk_consumption_total_comp
FOREIGN KEY (id_consumption)
REFERENCES consumption(id);

--PROPOSAL CONSTRAINT
ALTER TABLE proposal
ADD CONSTRAINT fk_proposal_agree
FOREIGN KEY (id_agreement)
REFERENCES agreement(id);

--TYPE PROPOSAL CONSTRAINT
ALTER TABLE type_proposal
ADD CONSTRAINT fk_pro_type_pro
FOREIGN KEY (id_proposal)
REFERENCES proposal(id);

ALTER TABLE type_proposal
ADD CONSTRAINT fk_proposal_type_comp
FOREIGN KEY (id_consumption)
REFERENCES consumption(id);