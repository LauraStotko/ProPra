# Gruppe 13

# Overview
-------


# Entity–relationship model
![ER-Diagramm.png](https://gitlab2.cip.ifi.lmu.de/bio/propra_ws23/stotko/gruppe-13/-/raw/main/Resources/ER-Diagramm.png?ref_type=heads)

Homestrad: Jede Familie hat eine a_id (von 2 bis n Sequenzen möglich), in Alignments haben alle Sequenzen dieser Familie die gleiche a_id; nicht jedes Alignment ist eine Familie, nur die Alignments aus Homestrad

Alignments: alle Einträge mit der gleichen a_id gehören zu einem Alignment, eine Sequenz kann in verschiedenen Alignments vorkommen

Sequences: Type kann DNA, mRNA und protein sequences sein

Bereits erstellt:
CREATE TABLE Sequences( id VARCHAR(250) PRIMARY KEY, sequence TEXT, type TEXT, pdb_id TEXT);

CREATE TABLE Homestrad( family_name VARCHAR(250) PRIMARY KEY, a_id INTEGER);

CREATE TABLE Swissprot(accession_nr VARCHAR(250) PRIMARY KEY, sequence_id VARCHAR(250), organism VARCHAR(250));

CREATE TABLE Keywords(function VARCHAR(250) PRIMARY KEY);

CREATE TABLE Sources( accession_nr VARCHAR(250) PRIMARY KEY, name VARCHAR(250));

CREATE TABLE has_alignment( sequence_id VARCHAR(250), a_id VARCHAR(250));

CREATE TABLE is_fam( a_id VARCHAR(250), family_name VARCHAR(250));

CREATE TABLE is_in( id VARCHAR(250), accession_nr VARCHAR(250));

CREATE TABLE has_function(accession_nr VARCHAR(250), function VARCHAR(250));

CREATE TABLE has_ac_numbers(sequence_id VARCHAR(250),accession_nr VARCHAR(250));

CREATE TABLE Alignments(entry INTEGER AUTO_INCREMENT PRIMARY KEY, a_id INTEGER, sequence_id VARCHAR(250));


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

