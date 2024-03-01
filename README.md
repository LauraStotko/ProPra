# Gruppe 13

# Overview
-------


## Entity–relationship model
![ER-Diagramm.png](https://gitlab2.cip.ifi.lmu.de/bio/propra_ws23/stotko/gruppe-13/-/raw/main/Resources/ER-Diagramm.png?ref_type=heads)

Homestrad: Jede Familie hat eine a_id (von 2 bis n Sequenzen möglich), in Alignments haben alle Sequenzen dieser Familie die gleiche a_id; nicht jedes Alignment ist eine Familie, nur die Alignments aus Homestrad

Alignments: alle Einträge mit der gleichen a_id gehören zu einem Alignment, eine Sequenz kann in verschiedenen Alignments vorkommen

Sequences: Type kann DNA, mRNA und protein sequences sein

###TABLES
`+----------------------+
| Tables_in_bioprakt13 |
+----------------------+
| Alignments           |
| Homestrad            |
| Keywords             |
| Sequences            |
| Sources              |
| Swissprot            |
| has_ac_numbers       |
| has_alignment        |
| has_function         |
| is_fam               |
| is_in                |
+----------------------+`

###Entities

`describe Alignments;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| entry       | int(11)      | NO   | PRI | NULL    | auto_increment |
| a_id        | int(11)      | YES  |     | NULL    |                |
| sequence_id | varchar(250) | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+`

`describe Homestrad;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| fam_id      | int(11)      | NO   | PRI | NULL    | auto_increment |
| family_name | varchar(250) | NO   |     | NULL    |                |
| a_id        | int(11)      | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+`

`describe Keywords;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| func_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
| function | varchar(250) | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+`

'describe Sequences;
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| seq_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| header_id | varchar(250) | YES  |     | NULL    |                |
| sequence  | text         | YES  |     | NULL    |                |
| type      | text         | YES  |     | NULL    |                |
| pdb_id    | text         | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+'

`describe Sources;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| source_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| accession_nr | varchar(250) | NO   |     | NULL    |                |
| name         | varchar(250) | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+`

`describe Swissprot;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| swiss_id     | int(11)      | NO   | PRI | NULL    | auto_increment |
| accession_nr | varchar(250) | NO   |     | NULL    |                |
| sequence_id  | varchar(250) | YES  |     | NULL    |                |
| organism     | varchar(250) | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+`

-------

# Folder Structure
Our folder structure is designed to align with the organization of the submission server, promoting uniformity and clarity. Below is an overview of the main directories:

Solution1/: Contains scripts related to tasks from Assignment Sheets 1.

Solution2/: Contains scripts related to tasks from Assignment Sheets 2.

Solution3/: Integrate your Alignment or GOR implementation here.

additional_features/: For any additional features or experiments, create separate branches.


# Version Control
We use Git for version control following these practices:

The main branch reflects the submission-ready state.

Create new branches for developing new features or experiments.

