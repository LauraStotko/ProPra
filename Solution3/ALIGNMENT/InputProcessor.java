package Solution3.ALIGNMENT;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class InputProcessor {
    String pairsFilePath;
    String seqLibFilePath;
    SubstitutionMatrix substitutionMatrix;

    private List<PdbSequence> sequences = new ArrayList<>();
    private List<PdbPair> alignments = new ArrayList<>();

    public InputProcessor(String pairFilePath, String seqLibFilePath, String substitutionFilePath) {
        this.pairsFilePath = pairFilePath;
        this.seqLibFilePath = seqLibFilePath;
        this.substitutionMatrix = new SubstitutionMatrix(substitutionFilePath);
    }

    public List<PdbSequence> getSequences() {
        parseSeqLibFile();
        return sequences;
    }

    public List<PdbPair> getAlignments() {
        parsePairsFile();
        return alignments;
    }

    public void parsePairsFile() {
        try (BufferedReader reader = new BufferedReader(new FileReader(pairsFilePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // "\\s+" Splits the string line into an array of substrings
                // wherever one or more whitespace characters are found.
                String[] substr = line.split("\\s+");
                if (substr.length >= 2) {
                    // Create a new PdbPair and add it to the list
                    alignments.add(new PdbPair(substr[0], substr[1]));
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading pairs file: " + e.getMessage());
        }
    }

    public void parseSeqLibFile() {
        try (BufferedReader reader = new BufferedReader(new FileReader(seqLibFilePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] substr = line.split(":", 2);
                if (substr.length == 2) {
                    String id = substr[0].trim();
                    String sequence = substr[1].trim();
                    sequences.add(new PdbSequence(id, sequence));
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading sequence library file: " + e.getMessage());
        }
    }


}
