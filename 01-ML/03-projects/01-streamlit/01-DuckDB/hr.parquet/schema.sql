


CREATE TABLE jobs(job_id INTEGER PRIMARY KEY, job_title VARCHAR NOT NULL, min_salary DOUBLE NOT NULL, max_salary DOUBLE NOT NULL);
CREATE TABLE regions(region_id INTEGER PRIMARY KEY, region_name VARCHAR NOT NULL);
CREATE TABLE countries(country_id VARCHAR, country_name VARCHAR NOT NULL, region_id INTEGER NOT NULL, PRIMARY KEY(country_id), FOREIGN KEY (region_id) REFERENCES regions(region_id));
CREATE TABLE locations(location_id INTEGER PRIMARY KEY, street_address VARCHAR, postal_code VARCHAR, city VARCHAR NOT NULL, state_province VARCHAR, country_id VARCHAR NOT NULL, FOREIGN KEY (country_id) REFERENCES countries(country_id));
CREATE TABLE departments(department_id INTEGER PRIMARY KEY, department_name VARCHAR NOT NULL, location_id INTEGER DEFAULT(NULL), FOREIGN KEY (location_id) REFERENCES locations(location_id));
CREATE TABLE employees(employee_id INTEGER PRIMARY KEY, first_name VARCHAR, last_name VARCHAR NOT NULL, email VARCHAR NOT NULL, phone_number VARCHAR, hire_date VARCHAR NOT NULL, job_id INTEGER NOT NULL, salary DOUBLE NOT NULL, manager_id INTEGER, department_id INTEGER NOT NULL, FOREIGN KEY (job_id) REFERENCES jobs(job_id), FOREIGN KEY (department_id) REFERENCES departments(department_id), );




