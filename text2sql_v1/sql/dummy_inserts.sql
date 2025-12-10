-- Hierarchical dummy INSERT statements for POC_UNIT_HIER
-- Generated: 2025-10-28
-- 31 rows: 1 corp, 2 divisions, 4 regions, 8 districts, 16 stores

INSERT INTO POC_UNIT_HIER (
    UNIT_SKEY, DOMAIN_ID, LOCALE_CODE, UNIT_ORG_ATTR_SKEY, UNIT_ORG_LEVEL,
    UNIT_ID, UNIT_NAME, UNIT_LEVEL_DESC, UNIT_STATUS_CODE, UNIT_STATUS,
    CORP_ID, CORP_SKEY, CORP_NAME, CORP_LEVEL_DESC,
    LEVEL_ID_1, LEVEL_SKEY_1, LEVEL_NAME_1, LEVEL_DESC_1,
    LEVEL_ID_2, LEVEL_SKEY_2, LEVEL_NAME_2, LEVEL_DESC_2,
    LEVEL_ID_3, LEVEL_SKEY_3, LEVEL_NAME_3, LEVEL_DESC_3,
    LEVEL_ID_4, LEVEL_SKEY_4, LEVEL_NAME_4, LEVEL_DESC_4,
    LEVEL_ID_5, LEVEL_SKEY_5, LEVEL_NAME_5, LEVEL_DESC_5,
    DISTRICT_ID, DISTRICT_SKEY, DISTRICT_NAME, DISTRICT_DESC,
    STORE_ID, STORE_SKEY, STORE_NAME, STORE_DESC, STORE_LEVEL_FLAG,
    CREATE_DATE_TIME, UPDATE_DATE_TIME
) VALUES

-- Level 1: CORP (1 row)
(1, 1, 'en-US', 1, 1, 'CORP-1', 'Acme Corporation', 'Corp', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, '2025-01-01 00:00:00', '2025-10-01 00:00:00'),

-- Level 2: Divisions (2 rows)
(2, 1, 'en-US', 2, 2, 'DIV-1', 'Division 1', 'Division', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, NULL, NULL, NULL, 0, '2025-02-01 00:00:00', '2025-10-01 00:00:00'),
(3, 1, 'en-US', 3, 2, 'DIV-2', 'Division 2', 'Division', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, NULL, NULL, NULL, 0, '2025-02-02 00:00:00', '2025-10-01 00:00:00'),

-- Level 3: Regions (4 rows) - each division has 2 regions
(4, 1, 'en-US', 4, 3, 'REG-1', 'Region 1', 'Region', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, 0, '2025-03-01 00:00:00', '2025-10-01 00:00:00'),
(5, 1, 'en-US', 5, 3, 'REG-2', 'Region 2', 'Region', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, 0, '2025-03-02 00:00:00', '2025-10-01 00:00:00'),
(6, 1, 'en-US', 6, 3, 'REG-3', 'Region 3', 'Region', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, 0, '2025-03-03 00:00:00', '2025-10-01 00:00:00'),
(7, 1, 'en-US', 7, 3, 'REG-4', 'Region 4', 'Region', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, 0, '2025-03-04 00:00:00', '2025-10-01 00:00:00'),

-- Level 4: Districts (8 rows) - each region has 2 districts
(8, 1, 'en-US', 8, 4, 'DST-1', 'District 1', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-1', 1001, 'District 1', 'District of Region 1', NULL, NULL, NULL, NULL, 'DST-1', 1001, 'District 1', 'District of Region 1', NULL, NULL, NULL, NULL, 0, '2025-04-01 00:00:00', '2025-10-01 00:00:00'),
(9, 1, 'en-US', 9, 4, 'DST-2', 'District 2', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-2', 1002, 'District 2', 'District of Region 2', NULL, NULL, NULL, NULL, 'DST-2', 1002, 'District 2', 'District of Region 2', NULL, NULL, NULL, NULL, 0, '2025-04-02 00:00:00', '2025-10-01 00:00:00'),
(10, 1, 'en-US', 10, 4, 'DST-3', 'District 3', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-3', 1003, 'District 3', 'District of Region 3', NULL, NULL, NULL, NULL, 'DST-3', 1003, 'District 3', 'District of Region 3', NULL, NULL, NULL, NULL, 0, '2025-04-03 00:00:00', '2025-10-01 00:00:00'),
(11, 1, 'en-US', 11, 4, 'DST-4', 'District 4', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-4', 1004, 'District 4', 'District of Region 4', NULL, NULL, NULL, NULL, 'DST-4', 1004, 'District 4', 'District of Region 4', NULL, NULL, NULL, NULL, 0, '2025-04-04 00:00:00', '2025-10-01 00:00:00'),
(12, 1, 'en-US', 12, 4, 'DST-5', 'District 5', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-5', 1005, 'District 5', 'Additional district of Region 1', NULL, NULL, NULL, NULL, 'DST-5', 1005, 'District 5', 'Additional district of Region 1', NULL, NULL, NULL, NULL, 0, '2025-04-05 00:00:00', '2025-10-01 00:00:00'),
(13, 1, 'en-US', 13, 4, 'DST-6', 'District 6', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-6', 1006, 'District 6', 'Additional district of Region 2', NULL, NULL, NULL, NULL, 'DST-6', 1006, 'District 6', 'Additional district of Region 2', NULL, NULL, NULL, NULL, 0, '2025-04-06 00:00:00', '2025-10-01 00:00:00'),
(14, 1, 'en-US', 14, 4, 'DST-7', 'District 7', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-7', 1007, 'District 7', 'Additional district of Region 3', NULL, NULL, NULL, NULL, 'DST-7', 1007, 'District 7', 'Additional district of Region 3', NULL, NULL, NULL, NULL, 0, '2025-04-07 00:00:00', '2025-10-01 00:00:00'),
(15, 1, 'en-US', 15, 4, 'DST-8', 'District 8', 'District', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-8', 1008, 'District 8', 'Additional district of Region 4', NULL, NULL, NULL, NULL, 'DST-8', 1008, 'District 8', 'Additional district of Region 4', NULL, NULL, NULL, NULL, 0, '2025-04-08 00:00:00', '2025-10-01 00:00:00'),


-- Level 5: Stores (16 rows) - each district has 2 stores
(16, 1, 'en-US', 16, 5, 'ST-1', 'Store 1', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-1', 1001, 'District 1', 'District of Region 1', 'ST-1', 5001, 'Store 1', 'Store under District 1','DST-1', 1001, 'District 1', 'District of Region 1', 'ST-1', 5001, 'Store 1', 'Store under District 1', 1, '2025-05-01 08:00:00', '2025-10-01 00:00:00'),
(17, 1, 'en-US', 17, 5, 'ST-2', 'Store 2', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-1', 1001, 'District 1', 'District of Region 1', 'ST-2', 5002, 'Store 2', 'Store under District 1','DST-1', 1001, 'District 1', 'District of Region 1', 'ST-2', 5002, 'Store 2', 'Store under District 1', 1, '2025-05-02 08:10:00', '2025-10-01 00:00:00'),
(18, 1, 'en-US', 18, 5, 'ST-3', 'Store 3', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-2', 1002, 'District 2', 'District of Region 2', 'ST-3', 5003, 'Store 3', 'Store under District 2','DST-2', 1002, 'District 2', 'District of Region 2', 'ST-3', 5003, 'Store 3', 'Store under District 2', 1, '2025-05-03 08:20:00', '2025-10-01 00:00:00'),
(19, 1, 'en-US', 19, 5, 'ST-4', 'Store 4', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-2', 1002, 'District 2', 'District of Region 2', 'ST-4', 5004, 'Store 4', 'Store under District 2', 'DST-2', 1002, 'District 2', 'District of Region 2', 'ST-4', 5004, 'Store 4', 'Store under District 2', 1, '2025-05-04 08:30:00', '2025-10-01 00:00:00'),
(20, 1, 'en-US', 20, 5, 'ST-5', 'Store 5', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-5', 5005, 'Store 5', 'Store under District 3', 'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-5', 5005, 'Store 5', 'Store under District 3', 1, '2025-05-05 08:40:00', '2025-10-01 00:00:00'),
(21, 1, 'en-US', 21, 5, 'ST-6', 'Store 6', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-6', 5006, 'Store 6', 'Store under District 3', 	'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-6', 5006, 'Store 6', 'Store under District 3', 1, '2025-05-06 08:50:00', '2025-10-01 00:00:00'),	
(22, 1, 'en-US', 22, 5, 'ST-7', 'Store 7', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-7', 5007, 'Store 7', 'Store under District 4', 	'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-7', 5007, 'Store 7', 'Store under District 4', 1, '2025-05-07 09:00:00', '2025-10-01 00:00:00'),	
(23, 1, 'en-US', 23, 5, 'ST-8', 'Store 8', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-8', 5008, 'Store 8', 'Store under District 4', 	'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-8', 5008, 'Store 8', 'Store under District 4', 1, '2025-05-08 09:10:00', '2025-10-01 00:00:00'),	
(24, 1, 'en-US', 24, 5, 'ST-9', 'Store 9', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-5', 1005, 'District 5', 'District of Region 1', 'ST-9', 5009, 'Store 9', 'Store under District 5',  	'DST-5', 1005, 'District 5', 'District of Region 1', 'ST-9', 5009, 'Store 9', 'Store under District 5', 1, '2025-05-09 09:20:00', '2025-10-01 00:00:00'), 	
(25, 1, 'en-US', 25, 5, 'ST-10', 'Store 10', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-6', 1006, 'District 6', 'District of Region 2', 'ST-10', 5010, 'Store 10', 'Store under District 6',  'DST-6', 1006, 'District 6', 'District of Region 2', 'ST-10', 5010, 'Store 10', 'Store under District 6', 1, '2025-05-10 09:30:00', '2025-10-01 00:00:00'), 
(26, 1, 'en-US', 26, 5, 'ST-11', 'Store 11', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-7', 1007, 'District 7', 'District of Region 3', 'ST-11', 5011, 'Store 11', 'Store under District 7',  'DST-7', 1007, 'District 7', 'District of Region 3', 'ST-11', 5011, 'Store 11', 'Store under District 7', 1, '2025-05-11 09:40:00', '2025-10-01 00:00:00'),
(27, 1, 'en-US', 27, 5, 'ST-12', 'Store 12', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-8', 1008, 'District 8', 'District of Region 4', 'ST-12', 5012, 'Store 12', 'Store under District 8',  'DST-8', 1008, 'District 8', 'District of Region 4', 'ST-12', 5012, 'Store 12', 'Store under District 8', 1, '2025-05-12 09:50:00', '2025-10-01 00:00:00'),
(28, 1, 'en-US', 28, 5, 'ST-13', 'Store 13', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-1', 101, 'Region 1', 'Region under Division 1', 'DST-1', 1001, 'District 1', 'District of Region 1', 'ST-13', 5013, 'Store 13', 'Store under District 1',   'DST-1', 1001, 'District 1', 'District of Region 1', 'ST-13', 5013, 'Store 13', 'Store under District 1',1, '2025-05-13 10:00:00', '2025-10-01 00:00:00'), 
(29, 1, 'en-US', 29, 5, 'ST-14', 'Store 14', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-1', 11, 'Division 1', 'First division', 'REG-2', 102, 'Region 2', 'Region under Division 1', 'DST-2', 1002, 'District 2', 'District of Region 2', 'ST-14', 5014, 'Store 14', 'Store under District 2',   'DST-2', 1002, 'District 2', 'District of Region 2', 'ST-14', 5014, 'Store 14', 'Store under District 2', 1, '2025-05-14 10:10:00', '2025-10-01 00:00:00'), 
(30, 1, 'en-US', 30, 5, 'ST-15', 'Store 15', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-3', 103, 'Region 3', 'Region under Division 2', 'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-15', 5015, 'Store 15', 'Store under District 3',  'DST-3', 1003, 'District 3', 'District of Region 3', 'ST-15', 5015, 'Store 15', 'Store under District 3', 1, '2025-05-15 10:20:00', '2025-10-01 00:00:00'),
(31, 1, 'en-US', 31, 5, 'ST-16', 'Store 16', 'Store', 'A', 'Active', 'CORP-1', 1, 'Acme Corporation', 'Global HQ', 'CORP-1', 1, 'Acme Corporation', 'Corporate level', 'DIV-2', 12, 'Division 2', 'Second division', 'REG-4', 104, 'Region 4', 'Region under Division 2', 'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-16', 5016, 'Store 16', 'Store under District 4',  'DST-4', 1004, 'District 4', 'District of Region 4', 'ST-16', 5016, 'Store 16', 'Store under District 4', 1, '2025-05-16 10:30:00', '2025-10-01 00:00:00');

-- POC_PROJECT Table - 10 sample projects
INSERT INTO POC_PROJECT (
    PROJECT_SKEY, COMPLETION_DATE_SKEY, DOMAIN_ID, FINISH_DATE_SKEY, START_DATE_SKEY, LAUNCH_DATE_SKEY, CREATE_DATE_SKEY,
    CREATOR_DEPT_SKEY, RES_DEPT_SKEY, RES_ROLE_SKEY, PROJECT_TYPE_SKEY, CREATOR_UNIT_SKEY, CREATOR_SKEY, APPROVER_SKEY, STATUS_SKEY, PARENT_PROJECT_SKEY,
    PROJECT_ID,
    START_DATE_TIMESTAMP, FINISH_DATE_TIMESTAMP, LAUNCH_DATE_TIMESTAMP, CREATE_DATE_TIMESTAMP, COMPLETION_DATE_TIMESTAMP,
    NUM_PROJECTS, NUM_D_PROJECTS, NUM_P_PROJECTS, NUM_R_PROJECTS, NUM_C_PROJECTS, NUM_F_PROJECTS, NUM_O_PROJECTS, STORE_COUNT, AUTO_COMPL_FLAG,
    PROJECT_CATEGORY, PROJECT_SUB_CATEGORY
) VALUES

-- Project 1: Store Renovation Initiative
(1, 20250930, 1, 20250930, 20250101, 20250115, 20241215, 
 101, 102, 201, 301, 1, 501, 601, 701, NULL,
 'PROJ-001',
 '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-01-15 00:00:00', '2024-12-15 00:00:00', '2025-09-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 8, 0,
 'Store Operations', 'Renovation'),

-- Project 2: Marketing Campaign Q1
(2, 20250331, 1, 20250331, 20250101, 20250105, 20241220,
 101, 103, 202, 302, 2, 502, 602, 702, NULL,
 'PROJ-002',
 '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-01-05 00:00:00', '2024-12-20 00:00:00', '2025-03-31 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 16, 0,
 'Marketing', 'Campaign'),

-- Project 3: Staff Training Program
(3, 20250630, 1, 20250630, 20250201, 20250210, 20250101,
 102, 104, 203, 303, 3, 503, 603, 703, NULL,
 'PROJ-003',
 '2025-02-01 00:00:00', '2025-06-30 00:00:00', '2025-02-10 00:00:00', '2025-01-01 00:00:00', '2025-06-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 4, 0,
 'HR Operations', 'Training'),

-- Project 4: Technology Upgrade
(4, 20250930, 1, 20250930, 20250301, 20250315, 20250201,
 103, 105, 204, 304, 4, 504, 604, 704, NULL,
 'PROJ-004',
 '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-03-15 00:00:00', '2025-02-01 00:00:00', '2025-09-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 12, 0,
 'IT Operations', 'Technology Upgrade'),

-- Project 5: Inventory Management System
(5, 20251031, 1, 20251031, 20250401, 20250420, 20250301,
 104, 106, 205, 305, 5, 505, 605, 705, NULL,
 'PROJ-005',
 '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-04-20 00:00:00', '2025-03-01 00:00:00', '2025-10-31 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 16, 0,
 'Supply Chain', 'System Implementation'),

-- Project 6: Customer Experience Enhancement
(6, 20250630, 1, 20250630, 20250501, 20250510, 20250401,
 101, 107, 206, 306, 1, 506, 606, 706, NULL,
 'PROJ-006',
 '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-05-10 00:00:00', '2025-04-01 00:00:00', '2025-06-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 8, 0,
 'Customer Service', 'Experience Design'),

-- Project 7: Sustainability Initiative
(7, 20251130, 1, 20251130, 20250601, 20250615, 20250501,
 102, 108, 207, 307, 2, 507, 607, 707, NULL,
 'PROJ-007',
 '2025-06-01 00:00:00', '2025-11-30 00:00:00', '2025-06-15 00:00:00', '2025-05-01 00:00:00', '2025-11-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 16, 0,
 'Corporate Sustainability', 'Green Initiative'),

-- Project 8: Sales Process Optimization
(8, 20250930, 1, 20250930, 20250701, 20250710, 20250601,
 103, 109, 208, 308, 3, 508, 608, 708, NULL,
 'PROJ-008',
 '2025-07-01 00:00:00', '2025-09-30 00:00:00', '2025-07-10 00:00:00', '2025-06-01 00:00:00', '2025-09-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 12, 0,
 'Sales Operations', 'Process Optimization'),

-- Project 9: Distribution Center Expansion
(9, 20251231, 1, 20251231, 20250801, 20250820, 20250701,
 104, 110, 209, 309, 4, 509, 609, 709, NULL,
 'PROJ-009',
 '2025-08-01 00:00:00', '2025-12-31 00:00:00', '2025-08-20 00:00:00', '2025-07-01 00:00:00', '2025-12-31 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 2, 0,
 'Logistics', 'Infrastructure Expansion'),

-- Project 10: Digital Transformation
(10, 20260630, 1, 20260630, 20250901, 20250915, 20250801,
 101, 111, 210, 310, 5, 510, 610, 710, NULL,
 'PROJ-010',
 '2025-09-01 00:00:00', '2026-06-30 00:00:00', '2025-09-15 00:00:00', '2025-08-01 00:00:00', '2026-06-30 00:00:00',
 1, 0, 1, 0, 1, 0, 0, 16, 0,
 'Digital Transformation', 'Full Stack Implementation');
-- Recreate the POC_PROJECT_EXECUTION INSERT with all 33 columns properly populated

-- POC_PROJECT_EXECUTION Table - Multiple entries per project per store
-- Status Codes: 1=Not Started, 2=In Progress, 3=Completed On Time, 4=Completed Late, 5=Overdue, 6=Force Completed, 7=Review Required
INSERT INTO POC_PROJECT_EXECUTION (
    EXECUTION_SKEY, COMPLETION_DATE_SKEY, DOMAIN_ID, FINISH_DATE_SKEY, START_DATE_SKEY, LAUNCH_DATE_SKEY, CREATE_DATE_SKEY,
    UNIT_SKEY, PROJECT_SKEY, UNIT_ID, PROJECT_ID,
    EXEC_COMPLETION_DATE_SKEY, EXEC_START_DATE_SKEY, EXEC_FINISH_DATE_SKEY,
    CREATOR_DEPT_SKEY, RES_DEPT_SKEY, RES_ROLE_SKEY, ASSIGNED_USER_SKEY, PROJECT_TYPE_SKEY, STATUS_SKEY, CREATOR_UNIT_SKEY,
    NUM_TOT_PROJECTS, NUM_N_PROJECTS, NUM_P_PROJECTS, NUM_R_PROJECTS, NUM_C_PROJECTS, NUM_F_PROJECTS, NUM_O_PROJECTS, NUM_CO_PROJECTS, AUTO_COMPL_FLAG,
    EXEC_START_DATE_TIMESTAMP, EXEC_FINISH_DATE_TIMESTAMP, EXEC_COMPLETION_DATE_TIMESTAMP
) VALUES

-- PROJ-001: Store Renovation - 8 stores with mixed statuses
(1, 20250930, 1, 20250930, 20250101, 20250115, 20241215, 1, 1, 'CORP-1', 'PROJ-001', 20250930, 20250101, 20250930, 101, 102, 201, 501, 301, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),
(2, 20250915, 1, 20250930, 20250101, 20250115, 20241215, 16, 1, 'ST-1', 'PROJ-001', 20250915, 20250101, 20250930, 101, 102, 201, 501, 301, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-15 00:00:00'),
(3, 20250920, 1, 20250930, 20250101, 20250115, 20241215, 17, 1, 'ST-2', 'PROJ-001', 20250920, 20250101, 20250930, 101, 102, 201, 501, 301, 4, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-20 00:00:00'),
(4, 20251010, 1, 20250930, 20250101, 20250115, 20241215, 18, 1, 'ST-3', 'PROJ-001', 20251010, 20250101, 20250930, 101, 102, 201, 501, 301, 5, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-10-10 00:00:00'),
(5, 20250930, 1, 20250930, 20250101, 20250115, 20241215, 19, 1, 'ST-4', 'PROJ-001', 20250925, 20250101, 20250930, 101, 102, 201, 501, 301, 6, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-25 00:00:00'),
(6, 20250905, 1, 20250930, 20250101, 20250115, 20241215, 20, 1, 'ST-5', 'PROJ-001', 20250905, 20250101, 20250930, 101, 102, 201, 501, 301, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-05 00:00:00'),
(7, 20250908, 1, 20250930, 20250101, 20250115, 20241215, 21, 1, 'ST-6', 'PROJ-001', 20250908, 20250101, 20250930, 101, 102, 201, 501, 301, 7, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, '2025-01-01 00:00:00', '2025-09-30 00:00:00', '2025-09-08 00:00:00'),
(8, 20250902, 1, 20250930, 20250101, 20250115, 20241215, 22, 1, 'ST-7', 'PROJ-001', 20250902, 20250101, 20250930, 101, 102, 201, 501, 301, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-09-30 00:00:00', NULL),

-- PROJ-002: Marketing Campaign Q1 - 16 stores with various statuses
(9, 20250331, 1, 20250331, 20250101, 20250105, 20241220, 16, 2, 'ST-1', 'PROJ-002', 20250330, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-30 00:00:00'),
(10, 20250328, 1, 20250331, 20250101, 20250105, 20241220, 17, 2, 'ST-2', 'PROJ-002', 20250328, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-28 00:00:00'),
(11, 20250325, 1, 20250331, 20250101, 20250105, 20241220, 18, 2, 'ST-3', 'PROJ-002', 20250325, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-25 00:00:00'),
(12, 20250410, 1, 20250331, 20250101, 20250105, 20241220, 19, 2, 'ST-4', 'PROJ-002', 20250410, 20250101, 20250331, 101, 103, 202, 502, 302, 5, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-04-10 00:00:00'),
(13, 20250329, 1, 20250331, 20250101, 20250105, 20241220, 20, 2, 'ST-5', 'PROJ-002', 20250329, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-29 00:00:00'),
(14, 20250405, 1, 20250331, 20250101, 20250105, 20241220, 21, 2, 'ST-6', 'PROJ-002', 20250405, 20250101, 20250331, 101, 103, 202, 502, 302, 4, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-04-05 00:00:00'),
(15, 20250331, 1, 20250331, 20250101, 20250105, 20241220, 22, 2, 'ST-7', 'PROJ-002', 20250331, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-31 00:00:00'),
(16, 20250320, 1, 20250331, 20250101, 20250105, 20241220, 23, 2, 'ST-8', 'PROJ-002', 20250320, 20250101, 20250331, 101, 103, 202, 502, 302, 6, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-20 00:00:00'),
(17, 20250403, 1, 20250331, 20250101, 20250105, 20241220, 24, 2, 'ST-9', 'PROJ-002', 20250403, 20250101, 20250331, 101, 103, 202, 502, 302, 5, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-04-03 00:00:00'),
(18, 20250327, 1, 20250331, 20250101, 20250105, 20241220, 25, 2, 'ST-10', 'PROJ-002', 20250327, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-27 00:00:00'),
(19, 20250330, 1, 20250331, 20250101, 20250105, 20241220, 26, 2, 'ST-11', 'PROJ-002', 20250330, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-30 00:00:00'),
(20, 20250331, 1, 20250331, 20250101, 20250105, 20241220, 27, 2, 'ST-12', 'PROJ-002', 20250331, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-31 00:00:00'),
(21, 20250315, 1, 20250331, 20250101, 20250105, 20241220, 28, 2, 'ST-13', 'PROJ-002', 20250315, 20250101, 20250331, 101, 103, 202, 502, 302, 7, 2, 1, 0, 0, 0, 0, 0, 1, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-15 00:00:00'),
(22, 20250401, 1, 20250331, 20250101, 20250105, 20241220, 29, 2, 'ST-14', 'PROJ-002', 20250401, 20250101, 20250331, 101, 103, 202, 502, 302, 4, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-04-01 00:00:00'),
(23, 20250325, 1, 20250331, 20250101, 20250105, 20241220, 30, 2, 'ST-15', 'PROJ-002', 20250325, 20250101, 20250331, 101, 103, 202, 502, 302, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-03-25 00:00:00'),
(24, 20250410, 1, 20250331, 20250101, 20250105, 20241220, 31, 2, 'ST-16', 'PROJ-002', 20250410, 20250101, 20250331, 101, 103, 202, 502, 302, 5, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-01-01 00:00:00', '2025-03-31 00:00:00', '2025-04-10 00:00:00'),

-- PROJ-003: Staff Training - 4 stores (regions 1 & 2)
(25, 20250630, 1, 20250630, 20250201, 20250210, 20250101, 16, 3, 'ST-1', 'PROJ-003', 20250625, 20250201, 20250630, 102, 104, 203, 503, 303, 3, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-02-01 00:00:00', '2025-06-30 00:00:00', '2025-06-25 00:00:00'),
(26, 20250630, 1, 20250630, 20250201, 20250210, 20250101, 17, 3, 'ST-2', 'PROJ-003', 20250630, 20250201, 20250630, 102, 104, 203, 503, 303, 3, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-02-01 00:00:00', '2025-06-30 00:00:00', '2025-06-30 00:00:00'),
(27, 20250620, 1, 20250630, 20250201, 20250210, 20250101, 18, 3, 'ST-3', 'PROJ-003', 20250620, 20250201, 20250630, 102, 104, 203, 503, 303, 3, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-02-01 00:00:00', '2025-06-30 00:00:00', '2025-06-20 00:00:00'),
(28, 20250715, 1, 20250630, 20250201, 20250210, 20250101, 19, 3, 'ST-4', 'PROJ-003', 20250715, 20250201, 20250630, 102, 104, 203, 503, 303, 4, 3, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-02-01 00:00:00', '2025-06-30 00:00:00', '2025-07-15 00:00:00'),

-- PROJ-004: Technology Upgrade - 12 stores (sample)
(29, 20250930, 1, 20250930, 20250301, 20250315, 20250201, 16, 4, 'ST-1', 'PROJ-004', 20250928, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-28 00:00:00'),
(30, 20250930, 1, 20250930, 20250301, 20250315, 20250201, 17, 4, 'ST-2', 'PROJ-004', 20250930, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),
(31, 20251005, 1, 20250930, 20250301, 20250315, 20250201, 18, 4, 'ST-3', 'PROJ-004', 20251005, 20250301, 20250930, 103, 105, 204, 504, 304, 5, 4, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-10-05 00:00:00'),
(32, 20250925, 1, 20250930, 20250301, 20250315, 20250201, 19, 4, 'ST-4', 'PROJ-004', 20250925, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-25 00:00:00'),
(33, 20250930, 1, 20250930, 20250301, 20250315, 20250201, 20, 4, 'ST-5', 'PROJ-004', 20250930, 20250301, 20250930, 103, 105, 204, 504, 304, 6, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),
(34, 20250920, 1, 20250930, 20250301, 20250315, 20250201, 21, 4, 'ST-6', 'PROJ-004', 20250920, 20250301, 20250930, 103, 105, 204, 504, 304, 7, 4, 1, 0, 0, 0, 0, 0, 1, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-20 00:00:00'),
(35, 20250930, 1, 20250930, 20250301, 20250315, 20250201, 22, 4, 'ST-7', 'PROJ-004', 20250930, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),
(36, 20250915, 1, 20250930, 20250301, 20250315, 20250201, 23, 4, 'ST-8', 'PROJ-004', 20250915, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-15 00:00:00'),
(37, 20251010, 1, 20250930, 20250301, 20250315, 20250201, 24, 4, 'ST-9', 'PROJ-004', 20251010, 20250301, 20250930, 103, 105, 204, 504, 304, 5, 4, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-10-10 00:00:00'),
(38, 20250928, 1, 20250930, 20250301, 20250315, 20250201, 25, 4, 'ST-10', 'PROJ-004', 20250928, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-28 00:00:00'),
(39, 20251001, 1, 20250930, 20250301, 20250315, 20250201, 26, 4, 'ST-11', 'PROJ-004', 20251001, 20250301, 20250930, 103, 105, 204, 504, 304, 4, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-10-01 00:00:00'),
(40, 20250930, 1, 20250930, 20250301, 20250315, 20250201, 27, 4, 'ST-12', 'PROJ-004', 20250930, 20250301, 20250930, 103, 105, 204, 504, 304, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-03-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),

-- PROJ-005: Inventory Management - 16 stores
(41, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 16, 5, 'ST-1', 'PROJ-005', 20251025, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-25 00:00:00'),
(42, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 17, 5, 'ST-2', 'PROJ-005', 20251031, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-31 00:00:00'),
(43, 20251105, 1, 20251031, 20250401, 20250420, 20250301, 18, 5, 'ST-3', 'PROJ-005', 20251105, 20250401, 20251031, 104, 106, 205, 505, 305, 4, 5, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-11-05 00:00:00'),
(44, 20251030, 1, 20251031, 20250401, 20250420, 20250301, 19, 5, 'ST-4', 'PROJ-005', 20251030, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-30 00:00:00'),
(45, 20251110, 1, 20251031, 20250401, 20250420, 20250301, 20, 5, 'ST-5', 'PROJ-005', 20251110, 20250401, 20251031, 104, 106, 205, 505, 305, 5, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-11-10 00:00:00'),
(46, 20251028, 1, 20251031, 20250401, 20250420, 20250301, 21, 5, 'ST-6', 'PROJ-005', 20251028, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-28 00:00:00'),
(47, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 22, 5, 'ST-7', 'PROJ-005', 20251031, 20250401, 20251031, 104, 106, 205, 505, 305, 6, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-31 00:00:00'),
(48, 20251015, 1, 20251031, 20250401, 20250420, 20250301, 23, 5, 'ST-8', 'PROJ-005', 20251015, 20250401, 20251031, 104, 106, 205, 505, 305, 7, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-15 00:00:00'),
(49, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 24, 5, 'ST-9', 'PROJ-005', 20251030, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-30 00:00:00'),
(50, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 25, 5, 'ST-10', 'PROJ-005', 20251031, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-31 00:00:00'),
(51, 20251029, 1, 20251031, 20250401, 20250420, 20250301, 26, 5, 'ST-11', 'PROJ-005', 20251029, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-29 00:00:00'),
(52, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 27, 5, 'ST-12', 'PROJ-005', 20251031, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-31 00:00:00'),
(53, 20251020, 1, 20251031, 20250401, 20250420, 20250301, 28, 5, 'ST-13', 'PROJ-005', 20251020, 20250401, 20251031, 104, 106, 205, 505, 305, 1, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', NULL),
(54, 20251031, 1, 20251031, 20250401, 20250420, 20250301, 29, 5, 'ST-14', 'PROJ-005', 20251031, 20250401, 20251031, 104, 106, 205, 505, 305, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-10-31 00:00:00'),
(55, 20251108, 1, 20251031, 20250401, 20250420, 20250301, 30, 5, 'ST-15', 'PROJ-005', 20251108, 20250401, 20251031, 104, 106, 205, 505, 305, 4, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-11-08 00:00:00'),
(56, 20251115, 1, 20251031, 20250401, 20250420, 20250301, 31, 5, 'ST-16', 'PROJ-005', 20251115, 20250401, 20251031, 104, 106, 205, 505, 305, 5, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-04-01 00:00:00', '2025-10-31 00:00:00', '2025-11-15 00:00:00'),

-- PROJ-006: Customer Experience - 8 stores (sample)
(57, 20250630, 1, 20250630, 20250501, 20250510, 20250401, 16, 6, 'ST-1', 'PROJ-006', 20250628, 20250501, 20250630, 101, 107, 206, 506, 306, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-28 00:00:00'),
(58, 20250630, 1, 20250630, 20250501, 20250510, 20250401, 17, 6, 'ST-2', 'PROJ-006', 20250630, 20250501, 20250630, 101, 107, 206, 506, 306, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-30 00:00:00'),
(59, 20250710, 1, 20250630, 20250501, 20250510, 20250401, 18, 6, 'ST-3', 'PROJ-006', 20250710, 20250501, 20250630, 101, 107, 206, 506, 306, 4, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-07-10 00:00:00'),
(60, 20250630, 1, 20250630, 20250501, 20250510, 20250401, 19, 6, 'ST-4', 'PROJ-006', 20250630, 20250501, 20250630, 101, 107, 206, 506, 306, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-30 00:00:00'),
(61, 20250625, 1, 20250630, 20250501, 20250510, 20250401, 20, 6, 'ST-5', 'PROJ-006', 20250625, 20250501, 20250630, 101, 107, 206, 506, 306, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-25 00:00:00'),
(62, 20250715, 1, 20250630, 20250501, 20250510, 20250401, 21, 6, 'ST-6', 'PROJ-006', 20250715, 20250501, 20250630, 101, 107, 206, 506, 306, 5, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-07-15 00:00:00'),
(63, 20250630, 1, 20250630, 20250501, 20250510, 20250401, 22, 6, 'ST-7', 'PROJ-006', 20250630, 20250501, 20250630, 101, 107, 206, 506, 306, 6, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-30 00:00:00'),
(64, 20250620, 1, 20250630, 20250501, 20250510, 20250401, 23, 6, 'ST-8', 'PROJ-006', 20250620, 20250501, 20250630, 101, 107, 206, 506, 306, 7, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, '2025-05-01 00:00:00', '2025-06-30 00:00:00', '2025-06-20 00:00:00'),

-- Additional projects (PROJ-007 through PROJ-010) - partial entries for brevity
(65, 20251130, 1, 20251130, 20250601, 20250615, 20250501, 16, 7, 'ST-1', 'PROJ-007', 20251128, 20250601, 20251130, 102, 108, 207, 507, 307, 3, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-06-01 00:00:00', '2025-11-30 00:00:00', '2025-11-28 00:00:00'),
(66, 20250930, 1, 20250930, 20250701, 20250710, 20250601, 17, 8, 'ST-2', 'PROJ-008', 20250930, 20250701, 20250930, 103, 109, 208, 508, 308, 3, 3, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-07-01 00:00:00', '2025-09-30 00:00:00', '2025-09-30 00:00:00'),
(67, 20251231, 1, 20251231, 20250801, 20250820, 20250701, 18, 9, 'ST-3', 'PROJ-009', 20251225, 20250801, 20251231, 104, 110, 209, 509, 309, 3, 4, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-08-01 00:00:00', '2025-12-31 00:00:00', '2025-12-25 00:00:00'),
(68, 20260630, 1, 20260630, 20250901, 20250915, 20250801, 19, 10, 'ST-4', 'PROJ-010', 20260615, 20250901, 20260630, 101, 111, 210, 510, 310, 3, 5, 1, 0, 0, 1, 1, 0, 0, 0, 0, '2025-09-01 00:00:00', '2026-06-30 00:00:00', '2026-06-15 00:00:00');

-- ============================================================================
-- POC_STATUS_D - Status Dimension Table
-- ============================================================================
-- Status codes used in POC_PROJECT_EXECUTION
-- STATUS_SKEY values: 1=NOT STARTED, 3=IN PROGRESS, 4=REVIEW, 5=COMPLETED, 7=OVERDUE

INSERT INTO POC_STATUS_D (
    LOCALE_CODE,
    STATUS_SKEY,
    DOMAIN_ID,
    STATUS_CODE,
    STATUS_DESC
) VALUES

-- NOT STARTED - Execution not yet started
('en-US', 1, 1, 'NOT_STARTED', 'Not Started'),

-- IN PROGRESS - Execution is currently in progress
('en-US', 3, 1, 'IN_PROGRESS', 'In Progress'),

-- REVIEW - Execution is under review
('en-US', 4, 1, 'REVIEW', 'Review'),

-- COMPLETED - Execution has been successfully completed
('en-US', 5, 1, 'COMPLETED', 'Completed'),

-- OVERDUE - Execution has exceeded the scheduled finish date
('en-US', 7, 1, 'OVERDUE', 'Overdue'),

-- FORCED_COMPLETE - Execution was force completed before scheduled finish date
('en-US', 6, 1, 'FORCED_COMPLETE', 'Forced Complete');
