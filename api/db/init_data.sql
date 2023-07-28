truncate table workspace_member restart identity cascade;
truncate table workspace restart identity cascade;
truncate table user_role restart identity cascade;
truncate table roles restart identity cascade;
truncate table users restart identity cascade;
-- Insert Role
insert into roles(name) values ('USER');
insert into roles(name) values ('ADMIN');
insert into roles(name) values ('MODERATOR');
-- Insert User
insert into users(email, first_name, last_name, password) values ('mike@email.com', 'Mike', 'Silver', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('jessica@email.com', 'Jessica', 'Gold', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('sara@email.com', 'Sara', 'Platinum', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('henry@email.com', 'Henry', 'Iron', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('ramona@email.com', 'Ramona', 'Copper', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('karel@email.com', 'Karel', 'Sulfur', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('amanda@email.com', 'Amanda', 'Lithium', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('david@email.com', 'David', 'Rubidium', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('lara@email.com', 'Lara', 'Neptunium', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
insert into users(email, first_name, last_name, password) values ('derik@email.com', 'Derik', 'Potassium', '$2b$12$zRUsZWN3KQHqUOVLcvVoeeUwPQEV3TcZrqqt9n11maOBtAjcTKQhS');
-- Insert association user_role
insert into user_role(user_id, role_id) values (1, 1);
insert into user_role(user_id, role_id) values (1, 2);
insert into user_role(user_id, role_id) values (1, 3);
insert into user_role(user_id, role_id) values (2, 1);
insert into user_role(user_id, role_id) values (2, 2);
insert into user_role(user_id, role_id) values (3, 1);
insert into user_role(user_id, role_id) values (4, 1);
insert into user_role(user_id, role_id) values (5, 1);
insert into user_role(user_id, role_id) values (6, 1);
insert into user_role(user_id, role_id) values (7, 1);
insert into user_role(user_id, role_id) values (8, 1);
insert into user_role(user_id, role_id) values (9, 1);
insert into user_role(user_id, role_id) values (10, 1);
-- Insert workspace
insert into workspace(title, owner_id) values ('Mike''s Workspace Java Project', 1);
insert into workspace(title, owner_id) values ('Mike''s Workspace Android Project', 1);
insert into workspace(title, owner_id) values ('Mike''s Workspace Python Project', 1);
insert into workspace(title, owner_id) values ('Jessica''s Workspace Ruby Project', 2);
insert into workspace(title, owner_id) values ('Jessica''s Workspace JavaScript Project', 2);
insert into workspace(title, owner_id) values ('Sara''s Workspace React Project', 3);
-- Insert association workspace_member
-- Mike's workspace Java Project
insert into workspace_member(user_id, workspace_id) values (1, 1);
insert into workspace_member(user_id, workspace_id) values (2, 1);
insert into workspace_member(user_id, workspace_id) values (3, 1);
insert into workspace_member(user_id, workspace_id) values (4, 1);
insert into workspace_member(user_id, workspace_id) values (5, 1);
insert into workspace_member(user_id, workspace_id) values (6, 1);
insert into workspace_member(user_id, workspace_id) values (7, 1);
-- Mike's workspace Android Project
insert into workspace_member(user_id, workspace_id) values (1, 2);
insert into workspace_member(user_id, workspace_id) values (4, 2);
insert into workspace_member(user_id, workspace_id) values (5, 2);
insert into workspace_member(user_id, workspace_id) values (8, 2);
-- Mike's workspace Python Project
insert into workspace_member(user_id, workspace_id) values (1, 3);
insert into workspace_member(user_id, workspace_id) values (9, 3);
-- Jessica's workspace Ruby Project
insert into workspace_member(user_id, workspace_id) values (2, 4);
insert into workspace_member(user_id, workspace_id) values (4, 4);
insert into workspace_member(user_id, workspace_id) values (5, 4);
-- Jessica's workspace JavaScript Project
insert into workspace_member(user_id, workspace_id) values (2, 5);
insert into workspace_member(user_id, workspace_id) values (10, 5);
-- Sara's workspace React Project
insert into workspace_member(user_id, workspace_id) values (3, 6);