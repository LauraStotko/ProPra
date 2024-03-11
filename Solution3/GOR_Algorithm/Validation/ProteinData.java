import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class ProteinData {

    private String sequence; // Aminosäuresequenz
    private String structure; // Tatsächliche Sekundärstruktur
    private String predictedStructure; // Vorhergesagte Sekundärstruktur
    private String pdb;
    private double[] probabilityH;
    private double[] probabilityE;
    private double[] probabilityC;

    private double sovScoreH;
    private double sovScoreE;
    private double sovScoreC;


    private Map<Character, Double> q3Scores = new HashMap<>(); // For storing Q3 scores for H, E, and C
    private Map<Character, Double> sovScores = new HashMap<>();

    public ProteinData(String pdb, String sequence, String structure) {
        this.pdb = pdb;
        this.sequence = sequence;
        this.structure = structure;
        this.probabilityH = new double[sequence.length()];
        this.probabilityE = new double[sequence.length()];
        this.probabilityC = new double[sequence.length()];
    }

    public String getPdb() {
        return pdb;
    }

    public String getSequence() {
        return sequence;
    }

    public String getStructure() {
        return structure;
    }

    public void setPredictedStructure(String predictedStructure) {
        this.predictedStructure = predictedStructure;
    }

    public void setQ3Scores(Map<Character, Double> q3Scores) {
        this.q3Scores = q3Scores;
    }

    public void setSOVScores(Map<Character, Double> sovScores) {
        this.sovScores = sovScores;
    }

    public String getPredictedSecondaryStructure() {
        return predictedStructure;
    }

    public String getActualSecondaryStructure() {
        return structure;
    }

    public Map<Character, Double> getQ3Scores() {
        return this.q3Scores;
    }

    public Map<Character, Double> getSOVScores() {
        return this.sovScores;
    }


    // Methode zur Berechnung der SOV-Scores für alle Strukturtypen
    public void calculateAndSetSOVScores(String actualStructure, String predictedStructure) {
        this.sovScoreH = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'H');
        this.sovScoreE = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'E');
        this.sovScoreC = SOVScore.calculateSOVScore(actualStructure, predictedStructure, 'C');

        // Speichern der berechneten SOV-Scores in einer Map, falls benötigt
        sovScores.put('H', sovScoreH);
        sovScores.put('E', sovScoreE);
        sovScores.put('C', sovScoreC);
    }


    // Getter für die individuellen SOV-Scores
    public double getSovScoreH() {
        return sovScoreH;
    }

    public double getSovScoreE() {
        return sovScoreE;
    }

    public double getSovScoreC() {
        return sovScoreC;
    }
}
