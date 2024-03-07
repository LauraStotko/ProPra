package Solution3.ALIGNMENT;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


public class SubstitutionMatrix {
    // The matrix holding substitution scores between amino acid pairs
    private double[][] substitutionMatrix;
    // Maps each amino acid character to an index in the substitutionMatrix
    private Map<Character, Integer> aminoAcidToMatrixIndex = new HashMap<>();


    public SubstitutionMatrix(String substitutionFilePath) {
        parseSubstitutionMatrixFile(substitutionFilePath);
    }


    private void parseSubstitutionMatrixFile(String substitutionFilePath) {
        try (BufferedReader br = new BufferedReader(new FileReader(substitutionFilePath))) {
            String line;
            // Temporary storage for amino acids in order as given in the file
            String[] aminoAcidIndices = null;

            while ((line = br.readLine()) != null) {
                // Detect and process the row with amino acids order
                if (line.startsWith("ROWINDEX")) {
                    String rowIndexesString = line.split("\\s+")[1];
                    aminoAcidIndices = rowIndexesString.trim().split("");
                    // Initialize the matrix with the size based on the number of amino acids
                    substitutionMatrix = new double[aminoAcidIndices.length][aminoAcidIndices.length];
                    // Map each amino acid to its corresponding index in the matrix
                    for (int i = 0; i < aminoAcidIndices.length; i++) {
                        aminoAcidToMatrixIndex.put(aminoAcidIndices[i].charAt(0), i);
                    }
                }
                // Fill in the substitution scores for each amino acid pair
                else if (line.startsWith("MATRIX") && aminoAcidIndices != null) {
                    fillSubstitutionMatrix(line, aminoAcidIndices);
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading substitution matrix file: " + e.getMessage());
        }
    }

    private void fillSubstitutionMatrix(String matrixLine, String[] rowIndices) {
        String[] parts = matrixLine.trim().split("\\s+");
        int rowIndex = parts.length - 2; // Adjust for the "MATRIX" label and zero-based indexing
        for (int i = 1; i < parts.length; i++) {
            double score = Double.parseDouble(parts[i]);
            substitutionMatrix[rowIndex][i - 1] = score;
            if (rowIndex != i - 1) { // Ensure the matrix is symmetric for non-diagonal elements
                substitutionMatrix[i - 1][rowIndex] = score;
            }
        }
    }

    public double getScore(char a, char b) {
        Integer row = aminoAcidToMatrixIndex.get(a);
        Integer col = aminoAcidToMatrixIndex.get(b);
        // Validate both amino acids are present in the rowIndexMap
        if (row == null || col == null) {
            throw new IllegalArgumentException("Invalid amino acid characters: " + a + ", " + b);
        }
        // Retrieve and return the score from the matrix
        return substitutionMatrix[row][col];
    }
}
