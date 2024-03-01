# Gruppe 13

# Overview
-------


## Entity–relationship model
![ER-Diagramm.png](https://gitlab2.cip.ifi.lmu.de/bio/propra_ws23/stotko/gruppe-13/-/raw/main/Resources/ER-Diagramm.png?ref_type=heads)

Homestrad: Jede Familie hat eine a_id (von 2 bis n Sequenzen möglich), in Alignments haben alle Sequenzen dieser Familie die gleiche a_id; nicht jedes Alignment ist eine Familie, nur die Alignments aus Homestrad

Alignments: alle Einträge mit der gleichen a_id gehören zu einem Alignment, eine Sequenz kann in verschiedenen Alignments vorkommen

Sequences: Type kann DNA, mRNA und protein sequences sein

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

